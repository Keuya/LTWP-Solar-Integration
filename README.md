# LTWP Solar Hybrid: investment and grid-deliverability screen

An independent screening study of whether a co-located solar PV project at Lake Turkana Wind Power (LTWP) could create financeable incremental value. This is a decision framework and reproducible dispatch screen, not an LTWP proposal, grid-connection study, yield assessment or investment recommendation.

## Decision question

Would solar at the LTWP site generate enough additional, deliverable and contractable value to justify its development, connection and financing costs under Kenya's actual dispatch conditions and a credible offtake structure?

The investment chain is: resource → grid acceptance → contracted energy → cash flow → debt capacity → equity return. A benefit at one link does not prove value at the next. A nearby line or substation does not itself prove spare capacity, low connection cost or a right to sell power.

## Evidence that changes the original framing

- EPRA reported no wind energy curtailed in FY2024/25. In its July–December 2025 report, it recorded 11.28 GWh of wind curtailment within 245.35 GWh of combined wind and geothermal curtailment. The report says curtailment typically occurs during low-demand overnight hours. These system-level figures do not establish LTWP-specific hourly exposure.
- KETRACO announced the 400 kV Lessos–Loosuk project as an alternative evacuation route intended to carry up to 300 MW of LTWP wind. Treat it as a future grid scenario until its in-service date, operating limits and dispatch effect are evidenced.
- LTWP's public FAQ says the existing PPA permits sales to KPLC. A separate solar project's offtake route, contract terms and payment rights require confirmation.

Important units: 400 kV describes voltage. It is not a 400 MW transfer limit. Export-limit cases in the model are sensitivities only; use a grid study or connection agreement for a real limit.

## Established and unestablished

| Item | Status |
|---|---|
| PVsyst annual solar energy: 199.3 GWh for 77.5 MWp | Reported simulation output in the existing CSV; resource provenance, loss assumptions and independent yield review need documentation. |
| Solar resource and interannual uncertainty | Not lender-certified; a simple haircut is not a P90 assessment. |
| Wind annual and hourly shape | No verified metered time series included. Earlier wind shapes were stylised and are unsuitable for an investment conclusion. |
| Export capacity and curtailment allocation | Unknown pending grid evidence and contractual review. |
| PPA price, tenor, payment security and solar eligibility | Unknown for a standalone solar asset. |
| Project returns and debt capacity | Not established. No bankable CFADS, DSCR, LLCR or equity-return result is claimed. |

## Contents

- hybrid_analysis.py: chronological dispatch-screening model; it requires analyst-supplied time series.
- data/hourly_profile_template.csv: schema for timestamped wind, solar and export-limit data.
- docs/investment_case.md: diligence plan, commercial structures and project-finance model requirements.
- docs/evidence_register.csv: source-backed claims, limitations and evidence requests.
- data/PVsyst_Simulation_Results.csv: existing PVsyst output retained from the earlier study.

## Run the dispatch screen

Requires Python 3.10 or later; no third-party package is needed.

    python hybrid_analysis.py --input data/hourly_profile_template.csv --output-dir outputs

The template contains headings only, so the command stops with an input-data error until actual profiles are supplied. For a populated, source-documented file:

    python hybrid_analysis.py --input /path/to/verified_hourly_profiles.csv --output-dir outputs --scenario-caps-mw 100,200,300,400

Required columns: timestamp (ISO-8601 with timezone), wind_available_mw, solar_available_mw, export_limit_mw. Optional: energy_price_usd_mwh. Revenue is calculated only when supplied and is an illustrative uniform-price case, not a PPA forecast.

The model compares wind-only with wind-plus-solar under solar priority, wind priority and pro-rata allocation. These are sensitivities, not assertions about dispatch rules or contractual curtailment order. Scenario caps apply an additional cap to the supplied export limit. Results are only as reliable as their inputs.

Outputs are hourly dispatch and scenario summary CSV files. The tool reports delivered energy and curtailment by technology and incremental hybrid exports versus wind-only. It is a screening tool, not a power-system production-cost model, grid study or lender model.

## Decision gates

1. Obtain time-aligned LTWP metered availability/generation, solar yield, system dispatch/curtailment and connection evidence.
2. Establish the connection point, thermal and stability limits, outage conditions, connection works and the status of the Lessos–Loosuk route.
3. Confirm the asset owner, lawful offtake route, tariff, payment security, curtailment/deemed-energy allocation and shared-facility charges.
4. Only then build a tax and debt cash-flow model with CFADS, debt sizing, DSCR, LLCR, reserves and equity returns.
5. Proceed only if incremental contracted cash flow supports lender covenants and sponsor returns in downside cases.

## Sources

See docs/evidence_register.csv for dates, precise claims and limitations.

- EPRA FY ended 30 June 2025: https://epra.go.ke/sites/default/files/2025-09/Statistics-Report-June-2025-Web.pdf
- EPRA July–December 2025: https://epra.go.ke/sites/default/files/2026-03/Biannual%20Statistics%20Report%202025-2026.pdf
- KETRACO Lessos–Loosuk announcement: https://www.ketraco.co.ke/information-center/media-center/news/ketraco-signs-landmark-public-private-partnership-africa50-and
- LTWP FAQ: https://ltwp.co.ke/frequently-asked-questions/

Independent analysis for learning and professional demonstration. Public information does not substitute for sponsor, operator, lender, legal or system-operator diligence.
