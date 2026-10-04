# LTWP solar hybrid: evidence at a glance

> **Screening case, not an investment conclusion.** The sample dispatch profile is generated proxy data for model demonstration. It is not LTWP metering, an ERA5/PVGIS download, an operator dispatch record, a grid study, a yield assessment or a PPA.

**Current decision:** the concept is worth screening, but no bankable incremental value or project return is established. The binding questions are what can be exported, who is paid for the solar energy, and on what terms.

## Four investment gates

| Workstream | What we can say today | What is still missing | Status |
|---|---|---|---|
| Wind availability and curtailment | EPRA publishes national curtailment totals. The cited Jul–Dec 2025 report records 11.28 GWh of wind curtailment nationally; it does not identify LTWP's hourly curtailment. | At least 12 months of aligned LTWP available generation, actual generation, outage/availability, curtailment instructions and settlement, reconciled to operator data. | **Missing for LTWP** |
| Grid studies and connection limit | KETRACO announced a planned 400 kV Lessos–Loosuk route, described as intended to evacuate up to 300 MW of LTWP wind. 400 kV is voltage; it is not a 400 MW limit. | Connection agreement, point-of-connection ratings, load-flow and stability studies, N-1/contingency limits, outage assumptions, upgrade scope/cost and route commissioning status. | **Unverified** |
| Solar yield and provenance | The repository's existing PVsyst CSV reports 199.3 GWh/year for 77.5 MWp. | PVsyst project and version, coordinates, weather file/source and period, loss diagram, degradation, P50/P90 uncertainty report and independent review. | **Reported; provenance incomplete** |
| PPA and offtake | LTWP's public FAQ describes its existing PPA with KPLC. That alone does not show a separate solar plant can sell under it. | Written legal/commercial route for solar, tariff, term, dispatch and curtailment allocation, deemed energy, payment security, consent, metering and shared-facility charges. | **Unconfirmed for solar** |

Sources and limitations are in [the evidence register](evidence_register.csv) and [investment diligence plan](investment_case.md).

## What the proxy case shows

Open [the seven-day sample profile](../data/illustrative_proxy_week.csv). It contains hourly values for a **310 MW assumed wind nameplate**, a **60 MW assumed solar output ceiling** representing a hypothetical 77.5 MWp DC plant, and a **310 MW assumed export ceiling**. The curves are generated for demonstration and the 310 MW export ceiling is an arbitrary sensitivity input, not a known grid limit. No price is supplied because no evidenced solar tariff is available.

Run it with:

```bash
python hybrid_analysis.py --input data/illustrative_proxy_week.csv --output-dir outputs --scenario-caps-mw 200,310,400
```

Then inspect `outputs/dispatch_scenarios.csv` for wind-only exports, hybrid exports, incremental energy and curtailment under three dispatch allocation sensitivities. Inspect `outputs/hourly_dispatch.csv` to see each hour. The 200/310/400 MW values are **illustrative sensitivities**, not approved grid cases or connection advice.

This is a one-week teaching example. It cannot estimate annual generation, curtailment probability, P50/P90 yield, revenue or debt capacity. Replace the proxy with time-aligned, source-documented data before using results in an investment memo.

## Evidence request sequence

1. **LTWP / operator:** interval generation, availability, curtailment and settlement data with timestamps and definitions.
2. **KETRACO / system operator:** connection point, approved transfer limits, grid studies, outages, upgrade scope and Lessos–Loosuk status.
3. **Yield consultant / PVsyst owner:** native model, weather provenance, losses and uncertainty assessment.
4. **LTWP / KPLC / counsel:** confirm the legal route and complete commercial terms for solar.
5. **Only after those gates:** build the revenue case, CFADS, debt sizing, DSCR/LLCR and downside returns.
