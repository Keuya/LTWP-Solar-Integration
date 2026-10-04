# Investment case and diligence plan

## Core hypothesis

Co-located solar may create value through shared site infrastructure, additional low-carbon generation and a different production profile. Those are hypotheses. They become investable only when grid acceptance, a lawful offtake route, contractual allocation and resulting cash flows are evidenced.

## Red-team of the earlier case

| Earlier proposition | What evidence permits | What would validate it |
|---|---|---|
| Solar reduces LTWP wind curtailment | Possible, not demonstrated. EPRA reported no wind curtailment in FY2024/25 and 11.28 GWh system-wide in Jul–Dec 2025. | LTWP interval availability and dispatch reconciled to system-operator instructions. |
| Wind is strongest at night and solar fills the day | Qualitatively plausible; the old repository wind curve is stylised. | Multi-year, time-aligned measured or validated wind and solar profiles. |
| Existing line capacity can carry the hybrid plant | Unknown. Voltage and transfer capacity are different; 400 kV does not imply 400 MW. | Connection agreement, network model, load-flow/stability studies, contingency limits and dispatch records. |
| Shared infrastructure makes integration cheap | Possible, not quantified. Bays, protection, metering, transformers, system upgrades, land and legal changes may be required. | Itemised connection scope and written cost allocation. |
| Solar LCOE proves commercial attractiveness | No. LCOE does not prove sale price, deliverability, payment, debt capacity or equity return. | Contract route, tariff, complete costs and financing model. |
| A battery improves the case | Unproven until shifting value, cycle frequency, losses, degradation, replacement and payment route are modelled. | Dispatch optimisation against validated data and accepted revenue terms. |

## Gate 1: evidence and data rights

Request, under appropriate confidentiality, at least 12 months and preferably multiple years of interval data:

- LTWP gross/net generation, availability, outages, curtailment instructions and settlement.
- Solar resource and PVsyst model files, met-data source, loss diagram, degradation and uncertainty report.
- Point-of-connection single-line diagram, transformer and bay ratings, export limit, protection, outage/N-1 constraints and grid studies.
- System demand, dispatch, geothermal minimum stable generation and renewable curtailment by interval.
- Current and proposed LTWP transmission-route status, operating responsibility and commissioning assumptions.
- Existing PPA term, tariff, deemed-energy provisions, dispatch rights, consent and assignment provisions, as far as disclosure permits.
- Land, environmental/social, permitting and shared-facility rights; proposed ownership and operating responsibilities.

Classify each item as verified, reported, inferred or missing, with source date, owner, access permission and decision impact.

## Gate 2: technical deliverability

Use chronological data at the finest reliable interval. Compare wind-only with wind-plus-solar and calculate:

- available and exported MWh by technology;
- energy curtailed by technology and cause;
- incremental hybrid exports versus wind-only;
- point-of-connection peaks, ramps and utilisation;
- results under actual and contingency export limits;
- dispatch-allocation sensitivities;
- annual and seasonal results and resource-year sensitivity.

Treat Lessos–Loosuk as a future grid scenario until operating status and limits are verified. Run storage only after defining its dispatch objective and possible revenue source. The included Python tool is a first-pass screen, not a grid simulation or substitute for operator studies.

## Gate 3: commercial structure

Compare only structures counsel and counterparties confirm are legally and practically available:

1. Solar added under an amendment to LTWP's current offtake arrangement.
2. A separate solar project with a separate KPLC PPA.
3. Another authorised route, only if current law, licences, wheeling and settlement arrangements support it.

For each, define ownership, PPA tariff and tenor, dispatch priority, curtailment/deemed-energy rules, payment security, shared-asset charges, land/access, construction interface, metering, change-in-law and termination payments. Do not assume the existing LTWP PPA automatically covers another generating asset.

## Gate 4: project finance

Build a separate annual cash-flow model only after credible revenue and connection routes exist. Include:

- EPC, modules, inverters, balance of plant, owner's costs, development, land, connection, taxes/duties and contingency;
- operating costs, insurance, land, asset management, major maintenance and inverter replacement;
- yield cases from a competent energy-yield assessment, with documented P50/P90 and degradation;
- contracted energy after losses, availability, curtailment and settlement rules;
- PPA price/indexation, payment timing, taxes, working capital and FX;
- debt/equity, construction interest, fees, tenor, grace, repayment sculpting, DSRA and covenant lock-up;
- project IRR, equity IRR, CFADS, minimum DSCR, LLCR and debt sizing.

Show tariff break-even, debt capacity and returns in base, downside and severe downside cases. Stress delayed connection, lower export capacity/yield, CAPEX overrun, FX, payment delay and curtailment. P90 must come from uncertainty analysis, not a fixed haircut.

## Gate 5: decision

Proceed to full development only if the connection route and export rights are credible; offtake covers the solar asset with acceptable payment protections; downside cash flow supports covenants and hurdle returns; shared-infrastructure value survives integration costs; and each unresolved risk has an owner, mitigation, budget and closing condition.

A technically feasible plant without a route to contracted revenue is not bankable.

## Suggested outputs

1. Two-page investment committee note: decision, value driver, required conditions, returns, downside and recommendation.
2. Reproducible dispatch model with input provenance log.
3. Project-finance model with assumptions and debt sizing.
4. Grid and PPA diligence tracker with evidence gaps and responsible parties.
5. Public case study clearly labelled independent analysis and limitations.

## Career value

The strongest portfolio signal is the chain from engineering evidence to financing decision: quantify what can be delivered, establish who pays, then show how the contract supports debt and equity. This demonstrates technical-commercial judgement, downside discipline and source traceability relevant to project-finance analyst and developer roles. Do not imply LTWP endorsement, confidential data access or a live mandate unless true.
