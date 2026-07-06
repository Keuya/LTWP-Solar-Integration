"""LTWP + solar hybrid analysis.

Uses the actual PVsyst monthly simulation results (data/PVsyst_Simulation_Results.csv,
77.5 MWp / 199.3 GWh/yr / PR 86.2%) and adds the layers a developer or lender
would ask for next:

1. Hybrid complementarity - solar vs LTWP wind through the day and year.
2. Curtailment exposure vs the evacuation limit (parameter, not a datum).
3. An honest LCOE with discounting and degradation, plus P50/P90, CAPEX
   overrun and curtailment scenarios.

Wind shape note: LTWP publishes annual output (~1.5-1.7 TWh from 310 MW); the
monthly/diurnal shapes here are STYLISED from the known behaviour of the
Turkana low-level jet (stronger at night and in the SE-monsoon months) and are
labelled as such. Replace with metered data if available.

Usage: python hybrid_analysis.py   (writes charts + CSVs to outputs/)
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = "outputs"

# --- Solar: actual PVsyst results -----------------------------------------
def load_pvsyst(path="data/PVsyst_Simulation_Results.csv") -> pd.DataFrame:
    df = pd.read_csv(path, skiprows=2, encoding="latin-1")
    df = df.rename(columns={df.columns[0]: "month"})
    df = df[df["month"].notna() & (df["month"] != "Year")]  # units row has no month
    df["solar_gwh"] = pd.to_numeric(df["E_Grid"]) / 1e6
    df["pr"] = pd.to_numeric(df["PR"])
    return df[["month", "solar_gwh", "pr"]].reset_index(drop=True)


# --- Wind: stylised LTWP shape ---------------------------------------------
WIND_MW = 310.0
WIND_ANNUAL_GWH = 1_600.0     # public LTWP reporting range 1.5-1.7 TWh
# Stylised monthly weighting (Turkana jet strongest ~Jun-Sep, weaker Nov-Dec)
WIND_MONTHLY_SHAPE = np.array([0.9, 0.9, 0.85, 0.8, 1.0, 1.15, 1.25, 1.25,
                               1.15, 1.0, 0.75, 0.8])

# Stylised diurnal capacity factors (night jet) and solar bell curve
HOURS = np.arange(24)
# mean 0.59 matches the ~1.6 TWh/yr annual figure (310 MW, CF ~59%)
WIND_DIURNAL_CF = 0.59 + 0.27 * np.cos((HOURS - 2) / 24 * 2 * np.pi)
SOLAR_DIURNAL = np.exp(-((HOURS - 12.2) ** 2) / (2 * 2.6 ** 2))
SOLAR_DIURNAL[(HOURS < 6.5) | (HOURS > 18.5)] = 0.0

SOLAR_MWP = 77.5
EVACUATION_LIMIT_MW = 400.0   # assumption to test, not a datum


# --- Solar economics ---------------------------------------------------------
CAPEX_USD_W = 0.75
OPEX_USD_KW_YR = 10.0
DISCOUNT_REAL = 0.10
LIFE = 25
DEGRADATION = 0.005


def lcoe(annual_gwh_yr1: float, capex_mult=1.0, curtailment=0.0) -> float:
    """Real LCOE in USD/kWh with discounting and degradation."""
    capex = SOLAR_MWP * 1e6 * CAPEX_USD_W * capex_mult
    yrs = np.arange(1, LIFE + 1)
    disc = (1 + DISCOUNT_REAL) ** -yrs
    energy = annual_gwh_yr1 * 1e6 * (1 - DEGRADATION) ** (yrs - 1) * (1 - curtailment)
    opex = SOLAR_MWP * 1e3 * OPEX_USD_KW_YR
    return (capex + (opex * disc).sum()) / (energy * disc).sum()


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    sol = load_pvsyst()
    annual_solar = sol["solar_gwh"].sum()

    wind_monthly = WIND_ANNUAL_GWH * WIND_MONTHLY_SHAPE / WIND_MONTHLY_SHAPE.sum()

    # Chart 1: monthly complementarity
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(12)
    ax.bar(x - 0.2, wind_monthly, 0.4, label="LTWP wind 310 MW (stylised shape)", color="#2b6cb0")
    ax.bar(x + 0.2, sol["solar_gwh"], 0.4, label="Solar 77.5 MWp (PVsyst actuals)", color="#f4b942")
    ax.set_xticks(x), ax.set_xticklabels([m[:3] for m in sol["month"]])
    ax.set_ylabel("GWh / month")
    ax.set_title("Monthly generation: solar firms the wind farm's weak months (Nov-Apr)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "monthly_complementarity.png"), dpi=150)

    # Chart 2: stylised diurnal profile + evacuation limit
    wind_mw = WIND_MW * WIND_DIURNAL_CF
    solar_mw = SOLAR_MWP * 0.965 * SOLAR_DIURNAL      # inverter/ac ratio approx
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.stackplot(HOURS, wind_mw, solar_mw, labels=["Wind (stylised diurnal)", "Solar"],
                 colors=["#2b6cb0", "#f4b942"], alpha=0.85)
    ax.axhline(EVACUATION_LIMIT_MW, color="red", ls="--", lw=1.2,
               label=f"Evacuation limit assumption ({EVACUATION_LIMIT_MW:.0f} MW)")
    ax.set_xlabel("Hour of day"), ax.set_ylabel("MW")
    ax.set_title("Diurnal complementarity: Turkana jet peaks at night, solar fills the day")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "diurnal_profile.png"), dpi=150)

    combined_peak = float((wind_mw + solar_mw).max())

    # Scenario table
    p90 = 0.95   # PVsyst P90/P50 for low interannual variability sites
    scen = pd.DataFrame({
        "Base (P50)": [annual_solar, lcoe(annual_solar)],
        "P90 yield": [annual_solar * p90, lcoe(annual_solar * p90)],
        "CAPEX +20%": [annual_solar, lcoe(annual_solar, capex_mult=1.2)],
        "Curtailment 10%": [annual_solar * 0.9, lcoe(annual_solar, curtailment=0.10)],
        "Combined downside": [annual_solar * p90 * 0.9,
                              lcoe(annual_solar * p90, capex_mult=1.2, curtailment=0.10)],
    }, index=["Energy sold (GWh/yr)", "LCOE (USD/kWh)"]).T
    scen["LCOE (USD/kWh)"] = scen["LCOE (USD/kWh)"].round(4)
    scen["Energy sold (GWh/yr)"] = scen["Energy sold (GWh/yr)"].round(1)
    scen.to_csv(os.path.join(OUT, "lcoe_scenarios.csv"))

    print(f"Solar annual energy (PVsyst): {annual_solar:.1f} GWh, avg PR {sol['pr'].mean():.3f}")
    print(f"Stylised combined peak: {combined_peak:.0f} MW vs limit {EVACUATION_LIMIT_MW:.0f} MW")
    print(scen.to_string())


if __name__ == "__main__":
    main()
