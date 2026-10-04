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

- [Evidence dashboard](docs/evidence_dashboard.md): one-page view of the four investment gates, proxy results and next requests.
- [Required input pack](docs/required_input_pack.md): field-level definitions, periods, quality checks and evidence gates.
- [Evidence request tracker](data/evidence_request_tracker.csv): downloadable checklist of specific requests, likely holders, priority and decision use.
- hybrid_analysis.py: chronological dispatch-screening model; it requires time-series inputs.
- data/hourly_profile_template.csv: intake schema for dispatch inputs and operational validation fields.
- [Illustrative proxy week](data/illustrative_proxy_week.csv): NASA POWER-based seven-day proxy, with clearly labelled turbine/PV conversion assumptions.
- docs/investment_case.md: diligence plan, commercial structures and project-finance model requirements.
- docs/evidence_register.csv: source-backed claims, limitations and evidence requests.
- data/PVsyst_Simulation_Results.csv: existing PVsyst output retained from the earlier study.

## Run the dispatch screen

Requires Python 3.10 or later; no third-party package is needed.

    python hybrid_analysis.py --input data/hourly_profile_template.csv --output-dir outputs

The template contains headings only, so the command stops with an input-data error until actual profiles are supplied. For the illustrative sample:

    python hybrid_analysis.py --input data/illustrative_proxy_week.csv --output-dir outputs --scenario-caps-mw 200,310,400

Model-required columns: timestamp (ISO-8601 with timezone), wind_available_mw, solar_available_mw and export_limit_mw. Optional validation fields in the template retain metered export, curtailment, availability, event IDs, source IDs and quality flags; the current script does not use these extras in dispatch calculations. Optional energy_price_usd_mwh applies one illustrative uniform price to total hybrid exports and is not a PPA forecast.

The sample profile uses NASA POWER hourly 50 m wind and all-sky irradiance for a point near LTWP (2–8 March 2024, UTC), converted using a generic 80 m shear adjustment/turbine power curve and a simple GHI-to-PV output derate. It is a weather-based proxy, not LTWP turbine output or a PVsyst yield assessment. The 310 MW export ceiling is arbitrary and is not a known connection limit. One week cannot support annual yield, curtailment, revenue or financing conclusions. See the [dashboard](docs/evidence_dashboard.md) for methodology, limits and evidence requests.

The model compares wind-only with wind-plus-solar under solar priority, wind priority and pro-rata allocation. These are sensitivities, not assertions about dispatch rules or contractual curtailment order. Scenario caps apply an additional cap to the supplied export limit. Results are only as reliable as their inputs; inspect the hourly output as well as the scenario summary.

## Decision gates

1. Obtain time-aligned LTWP metered availability/generation, solar yield, system dispatch/curtailment and connection evidence.
2. Establish the connection point, thermal and stability limits, outage conditions, connection works and the status of the Lessos–Loosuk route.
3. Confirm the asset owner, lawful offtake route, tariff, payment security, curtailment/deemed-energy allocation and shared-facility charges.
4. Only then build a tax and debt cash-flow model with CFADS, DSCR, LLCR, reserves and equity returns.
5. Proceed only if incremental contracted cash flow supports lender covenants and sponsor returns in downside cases.

## Sources

See docs/evidence_register.csv for dates, precise claims and limitations.

- EPRA FY ended 30 June 2025: https://epra.go.ke/sites/default/files/2025-09/Statistics-Report-June-2025-Web.pdf
- EPRA July–December 2025: https://epra.go.ke/sites/default/files/2026-03/Biannual%20Statistics%20Report%202025-2026.pdf
- KETRACO Lessos–Loosuk announcement: https://www.ketraco.co.ke/information-center/media-center/news/ketraco-signs-landmark-public-private-partnership-africa50-and
- LTWP FAQ: https://ltwp.co.ke/frequently-asked-questions/

Independent analysis for learning and professional demonstration. Public information does not substitute for sponsor, operator, lender, legal or system-operator diligence.
