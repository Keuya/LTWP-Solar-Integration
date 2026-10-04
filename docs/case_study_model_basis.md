# Complete case-study model basis

## Status and use

This package is a **reproducible teaching case**, not LTWP telemetry, an LTWP forecast, a grid study, a PPA offer or an investment recommendation. Public facts, public reanalysis and analyst-generated assumptions are identified separately. Do not describe the generated hourly rows as LTWP's actual interval generation, availability or curtailment.

## Evidence inputs

- LTWP's 2024 Sustainability Report states 310.25 MW installed capacity, 1,367 GWh annual net generation and a 50.17% net capacity factor for 2024. This supplies an annual calibration anchor only; it does not provide the model with LTWP's hourly profile.
- NASA POWER v2.10.2 hourly data for 2024 supplies regional `WS50M` and `ALLSKY_SFC_SW_DWN` series at 2.5°N, 36.8°E (reported elevation 873.14 m). These are gridded weather/reanalysis values near the project area, not a site mast, turbine SCADA or bankable energy assessment.
- The earlier repository PVsyst results CSV reports 199.336 GWh, PR 0.862, `GlobHor` 2,231.3 kWh/m² and `GlobInc` 2,985.1 kWh/m². The native PVsyst project and weather file are not in the repository, so this output is reported but unverified.

Source details are in `data/nasa_power_weather_2024_metadata.json`, `docs/evidence_register.csv` and [the PV yield provenance note](pvsyst_model_provenance.md).

## Generated interval model

`data/case_study_hourly_2024.csv` contains 8,784 UTC hourly records. Each row is generated, not observed.

### Wind

1. Convert NASA 50 m wind speed to an assumed 80 m hub height using a 0.14 power-law shear exponent.
2. Apply a generic power curve: 3.5 m/s cut-in, 12 m/s rated, 25 m/s cut-out.
3. Apply 98.5% constant plant availability (assumption).
4. Apply a 5.616379 scalar to the generic hourly capacity-factor shape, with output capped at 310.25 MW, so the annual modelled wind energy equals LTWP's published 2024 annual net generation of 1,367 GWh.

The scalar deliberately exposes a major limitation: the regional NASA/generic turbine profile does not independently reproduce LTWP's wind regime. Matching the annual total does **not** validate the hourly, diurnal, seasonal or availability shape. Interval output and curtailment remain synthetic.

### Solar

1. Use the existing study's assumed 77.5 MWp DC / 74.62 MWac capacity.
2. Convert NASA hourly horizontal irradiance using `77.5 × GHI/1000 × 0.82`, cap at 74.62 MWac and apply 99.0% constant availability.
3. Use wind-priority dispatch at the assumed 310 MW base export cap to derive solar export and curtailment.

This is a simple GHI proxy, not a PVsyst model: it does not transpose GHI to plane-of-array, resolve component irradiance, calculate module temperature, model equipment-specific losses or establish P50/P90 yield.

## Modeled annual outputs

The existing dispatch script was run over all 8,784 records with export-limit sensitivities of 250, 310 and 400 MW:

| Assumed cap | Wind-only export | Hybrid export, wind priority | Incremental hybrid energy | Solar curtailed |
|---:|---:|---:|---:|---:|
| 250 MW | 1,217.2 GWh | 1,294.7 GWh | 77.5 GWh | 65.4 GWh |
| 310 MW | 1,367.0 GWh | 1,459.4 GWh | 92.4 GWh | 50.5 GWh |
| 400 MW | 1,367.0 GWh | 1,509.9 GWh | 142.8 GWh | 0.0 GWh |

The 400 MW case is a non-binding upper-envelope sensitivity in the data file, not an evidenced connection limit. At 310 MW, the 50.5 GWh solar curtailment follows directly from the assumed wind-priority dispatch at a shared 310 MW export cap. It is not observed LTWP curtailment.

The earlier PVsyst output is 56.5 GWh (28.3%) above this simple proxy's 142.8 GWh annual solar availability. These values are not directly comparable: the proxy uses horizontal GHI and generic losses, while the PVsyst native model/weather file is unavailable. The gap is a validation item, not evidence that either estimate is correct.

## Reproduce

From the repository root:

```bash
python scripts/build_case_study_data.py --fetch
python hybrid_analysis.py --input data/case_study_hourly_2024.csv --output-dir outputs --scenario-caps-mw 250,310,400
```

The first command downloads the public NASA POWER series and rebuilds the generated case data. The second writes interval dispatch and annual scenario summaries. It does not produce a grid study, PPA, P90 case or lender model.

## How to make the case genuinely project-specific

Replace each proxy with licensed, source-controlled evidence: LTWP SCADA and availability; operator curtailment and settlement; approved export limits and grid studies; native PVsyst project plus weather file and uncertainty report; and executed or formally proposed solar offtake terms. Preserve the same evidence labels and timestamp definitions.
