# LTWP solar hybrid: evidence at a glance

> **Screening case, not an investment conclusion.** The sample uses NASA POWER hourly weather reanalysis for a point near LTWP, converted into generic wind and PV output proxies. It is not LTWP metering, a validated project yield assessment, an operator dispatch record, a grid study or a PPA.

**Current decision:** the concept is worth screening, but no bankable incremental value or project return is established. The binding questions are what can be exported, who is paid for the solar energy, and on what terms.

## Four investment gates

| Workstream | What we can say today | What is still missing | Status |
|---|---|---|---|
| Wind availability and curtailment | EPRA publishes national curtailment totals. The cited Jul–Dec 2025 report records 11.28 GWh of wind curtailment nationally; it does not identify LTWP's hourly curtailment. NASA POWER gives regional 50 m reanalysis wind, not LTWP turbine output. | At least 12 months of aligned LTWP available generation, actual generation, outage/availability, curtailment instructions and settlement, reconciled to operator data. | **Missing for LTWP** |
| Grid studies and connection limit | KETRACO announced a planned 400 kV Lessos–Loosuk route, described as intended to evacuate up to 300 MW of LTWP wind. 400 kV is voltage; it is not a 400 MW limit. | Connection agreement, point-of-connection ratings, load-flow and stability studies, N-1/contingency limits, outage assumptions, upgrade scope/cost and route commissioning status. | **Unverified** |
| Solar yield and provenance | The repository's existing PVsyst CSV reports 199.3 GWh/year for 77.5 MWp. NASA POWER gives regional horizontal irradiance for the demo week, not plane-of-array project yield. | PVsyst project and version, coordinates, weather file/source and period, loss diagram, degradation, P50/P90 uncertainty report and independent review. | **Reported; provenance incomplete** |
| PPA and offtake | LTWP's public FAQ describes its existing PPA with KPLC. That alone does not show a separate solar plant can sell under it. | Written legal/commercial route for solar, tariff, term, dispatch and curtailment allocation, deemed energy, payment security, consent, metering and shared-facility charges. | **Unconfirmed for solar** |

Sources and limitations are in [the evidence register](evidence_register.csv) and [investment diligence plan](investment_case.md).

## What the proxy case shows

Open [the seven-day sample profile](../data/illustrative_proxy_week.csv). NASA POWER v2.10.2 supplies hourly `WS50M` wind speed and `ALLSKY_SFC_SW_DWN` irradiance for 2.5°N, 36.8°E on 2–8 March 2024 (UTC). A generic shear adjustment and turbine power curve convert wind speed to MW; a simple GHI-to-output derate converts irradiance to solar MW. The file assumes 310 MW wind nameplate, 77.5 MWp solar and a 310 MW export ceiling. The export ceiling is an arbitrary sensitivity input, not a known grid limit. No price is supplied because no evidenced solar tariff is available.

### Seven-day dispatch result

| Export-ceiling sensitivity | Wind-only exported | Hybrid exported | Incremental hybrid energy |
|---:|---:|---:|---:|
| 200 MW | 8,717.9 MWh | 11,408.7 MWh | 2,690.8 MWh |
| 310 MW | 8,982.8 MWh | 12,067.5 MWh | 3,084.7 MWh |
| 400 MW | 8,982.8 MWh | 12,067.5 MWh | 3,084.7 MWh |

These are outputs from the seven-day proxy and the model, not a forecast. The 400 MW case equals the 310 MW case because the input file itself applies a 310 MW export ceiling. Do not annualise these numbers or interpret incremental MWh as saleable energy until LTWP dispatch and solar offtake are evidenced.

The power conversions are teaching assumptions, not turbine-specific or PVsyst results. See [the data notes](../data/README.md) for equations, source links and limits.

Run it with:

```bash
python hybrid_analysis.py --input data/illustrative_proxy_week.csv --output-dir outputs --scenario-caps-mw 200,310,400
```

Then inspect `outputs/dispatch_scenarios.csv` for wind-only exports, hybrid exports, incremental energy and curtailment under three dispatch allocation sensitivities. Inspect `outputs/hourly_dispatch.csv` to see each hour. The 200/310/400 MW values are **illustrative sensitivities**, not approved grid cases or connection advice.

This is a one-week weather proxy. It cannot estimate annual generation, curtailment probability, P50/P90 yield, revenue or debt capacity. Replace it with multi-year site-validated and operator data before using results in an investment memo.

## Evidence request sequence

1. **LTWP / operator:** interval generation, availability, curtailment and settlement data with timestamps and definitions.
2. **KETRACO / system operator:** connection point, approved transfer limits, grid studies, outages, upgrade scope and Lessos–Loosuk status.
3. **Yield consultant / PVsyst owner:** native model, weather provenance, losses and uncertainty assessment.
4. **LTWP / KPLC / counsel:** confirm the legal route and complete commercial terms for solar.
5. **Only after those gates:** build the revenue case, CFADS, debt sizing, DSCR/LLCR and downside returns.
