# Required data pack: LTWP co-located solar screen

This note defines the inputs needed to replace the illustrative proxy with an evidence-led dispatch and project-finance case. A machine-readable request list is in [evidence_request_tracker.csv](../data/evidence_request_tracker.csv), and the hourly intake schema is in [hourly_profile_template.csv](../data/hourly_profile_template.csv).

## Decision standard

Separate four evidence classes:

- **Measured/project record:** LTWP meter, operator dispatch, outage and settlement records.
- **Grid-approved:** connection agreement, grid study, operating instruction or signed capacity allocation.
- **Modelled:** solar/wind resource or engineering output with model version, input data and validation.
- **Assumed:** analyst sensitivity only. Keep assumptions visible; do not relabel them as project evidence.

For confidential or licensed material, request permission for analysis and keep raw files outside the public repository. Publish only material cleared for public release.

## 1. Time-aligned wind, solar and dispatch data — first priority

Request at least 12 continuous months; three to five years is preferable for seasonal and interannual sensitivity. Use 15-minute intervals if available; hourly is the minimum for this screening model. Supply timestamps in UTC with an explicit interval convention (interval start or end).

Required model fields:

| Field | Meaning | Unit |
|---|---|---|
| `timestamp` | UTC interval timestamp | ISO-8601 |
| `wind_available_mw` | Wind power available before grid curtailment, preferably calculated from validated SCADA and turbine availability | MW |
| `solar_available_mw` | Solar power available before grid curtailment from a documented yield model for the same weather period | MW |
| `export_limit_mw` | Approved active export limit at the point of connection for that interval; if time-invariant, record the governing document | MW |
| `energy_price_usd_mwh` | Optional price only when one evidenced price applies to the energy represented | USD/MWh |

Operational validation fields to retain alongside the model inputs, even though the current script does not use them in dispatch calculations:

- metered wind export and, if applicable, gross generation;
- curtailment amount, cause, instruction ID and start/end time;
- turbine/plant availability, forced outages, planned maintenance and missing SCADA periods;
- solar modelled availability and, once built, actual solar meter output;
- point-of-connection export meter and settlement meter values;
- grid outage, constraint or dispatch instruction, with source/identifier.

Do not infer wind availability from metered export alone: metered export can already reflect curtailment. Reconcile gross/available power, actual export and curtailment against operator instructions and settlement.

## 2. Grid and connection evidence — investment gate

Obtain from LTWP, KETRACO and/or the system operator, as applicable:

- point-of-connection single-line diagram, voltage, transformer, bay and conductor ratings;
- executed connection agreement and any export/import or shared-capacity allocation;
- approved load-flow, stability, fault-level and protection studies for wind-only and hybrid operation;
- normal and contingency/N-1 transfer limits, seasonal limits, outage history and planned outages;
- dispatch instructions and curtailment priority/rules at the connection point;
- required connection works, upgrade scope, estimate, schedule, cost owner and approvals;
- commissioning status and expected operating limits of the Lessos–Loosuk route.

A nominal line voltage or public project announcement is not a transfer-capacity study. Use a time-varying `export_limit_mw` only when an approved operating limit is available; otherwise scenario caps must be clearly marked assumptions.

## 3. Solar-yield evidence — lender-quality energy case

Request the native PVsyst project and report, not only annual outputs or screenshots:

- exact site coordinates, elevation, layout, DC/AC capacity and inverter clipping;
- weather provider, station/grid point, period, file format and quality checks;
- GHI/DNI/DHI, ambient temperature and wind series; plane-of-array transposition method;
- module/inverter make and model, orientation/tilt, shading, soiling, availability and electrical losses;
- degradation, availability, mismatch, clipping and auxiliary-consumption assumptions;
- monthly and hourly output for the same weather years as the wind series;
- P50/P90 or exceedance analysis, long-term correction and uncertainty breakdown;
- independent energy-yield review and confirmation of model version.

The existing repository PVsyst CSV reports 199.3 GWh/year for 77.5 MWp, but its provenance and uncertainty are not documented in that output. Do not call it bankable P50/P90 until the native files and supporting evidence are reviewed.

## 4. PPA, offtake and revenue terms — revenue gate

Obtain the existing LTWP PPA and any relevant amendments, plus the proposed legal/commercial route for the solar asset. Confirm with counsel and counterparties:

- seller, buyer, asset coverage, required consents/licences and ability to contract solar separately;
- tariff, currency, indexation, term, start date and contracted energy definition;
- metering, losses, settlement period, invoicing and payment timing;
- dispatch rights, curtailment allocation, deemed-energy conditions and exclusions;
- payment security, LC/escrow/guarantee, late-payment remedies and buyer credit support;
- shared-facility, land, O&M, transmission and balancing charges;
- termination, change-in-law, force majeure, political/convertibility and dispute provisions.

A public statement that LTWP sells to KPLC under an existing PPA does not establish solar eligibility or terms. Do not use a price in the current screen unless it applies to the energy in the model. If wind and solar have different contracts, calculate revenues separately in a dedicated cash-flow model.

## 5. Cost, schedule and financing inputs — only after technical and revenue gates

For an initial project-finance case request:

- EPC and major equipment pricing, scope split, contingency, owner/development costs and taxes;
- connection and grid-upgrade cost, land, permitting, environmental/social and legal costs;
- fixed/variable O&M, insurance, asset management, replacements and shared-site charges;
- construction schedule, COD, delay LDs, performance guarantees and interface risk;
- debt/equity mix, currency, rate, fees, tenor, grace period, amortisation and hedging;
- reserve requirements, working capital, tax, FX conversion and payment delay assumptions.

Use quotes and executed terms where available. Clearly label budget estimates and analyst assumptions.

## Data quality checks before running

1. One unique, strictly increasing UTC timestamp per interval; regular interval length and no silent gaps.
2. Units confirmed and no negative MW values; capacity and export readings stay within documented physical bounds.
3. All series use the same timestamps, daylight-saving convention and period; record time-zone conversion.
4. Missing intervals and imputation are reported. Suggested screening target: at least 98% complete intervals per series, with gaps disclosed and sensitivity-tested; this is a project QA rule, not a lender standard.
5. Reconcile interval energy sums to monthly/annual meter and settlement totals; explain material differences.
6. Record source owner, retrieval date, data version, definitions, rights to use, confidentiality class and transformation steps.

## Stop/go sequence

1. Validate time-aligned resource and operating data.
2. Obtain approved export limits and grid/connection scope.
3. Confirm an enforceable solar offtake route and revenue terms.
4. Calculate incremental contracted energy and net cash flow after losses, curtailment and costs.
5. Build CFADS, debt sizing, DSCR, LLCR and downside returns.

Until gates 1–3 are evidenced, the screen is a learning and diligence tool—not a bankability conclusion.
