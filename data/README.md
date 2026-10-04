This directory contains two different things:

- `hourly_profile_template.csv` is a blank schema. Replace it only with time-aligned, source-documented observations or model outputs.
- `illustrative_proxy_week.csv` is a seven-day, generated proxy for demonstrating the dispatch model. It is not measured LTWP wind, a solar-yield forecast, a grid limit or a historical dispatch record.

The proxy uses an assumed 310 MW wind nameplate, a hypothetical 77.5 MWp DC solar project represented by a 60 MW hourly output ceiling, and an arbitrary 310 MW export ceiling. Wind and solar hourly curves are generated for demonstration. The export ceiling is a scenario assumption, not an approved transfer limit. No power price is included because a separate solar PPA/offtake tariff is not evidenced.

The sample is deliberately short so a reader can inspect the hourly logic. It cannot support annual generation, curtailment probability, revenue, P50/P90 yield, project returns or debt sizing. Do not label it an LTWP forecast or use it as evidence of LTWP-specific curtailment.

See [the evidence dashboard](../docs/evidence_dashboard.md) for what is known, missing, and needed next. Replace the proxy with time-aligned LTWP availability/generation and curtailment, solar data with documented provenance, and grid/export limits from connection documents or studies before drawing project conclusions.
