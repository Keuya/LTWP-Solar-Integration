This directory contains three different things:

- `hourly_profile_template.csv` is a blank schema. Replace it only with time-aligned, source-documented observations or model outputs.
- `illustrative_proxy_week.csv` is a seven-day **weather-based proxy** for demonstrating the dispatch model. NASA POWER hourly reanalysis provides the weather series; the wind-to-power and irradiance-to-PV conversions are generic assumptions. It is not LTWP metering, a yield forecast or an approved grid limit.
- `PVsyst_Simulation_Results.csv` is the earlier study's PVsyst output; its model/weather provenance and loss assumptions remain to be obtained and reviewed.

## Proxy provenance and conversion

NASA POWER v2.10.2 hourly API, point 2.5°N, 36.8°E (reported elevation 873.14 m), 2–8 March 2024, UTC:
- `WS50M`: MERRA-2 reanalysis wind speed at 50 m.
- `ALLSKY_SFC_SW_DWN`: all-sky shortwave irradiance on a horizontal surface (Wh/m² per hourly interval; sources include MERRA-2 and SYN1DEG).

The repository profile converts these weather series to available MW using transparent generic assumptions:
- Wind: scale 50 m to 80 m using a 0.14 power-law shear exponent; apply a generic turbine power curve with 3.5 m/s cut-in, 12 m/s rated and 25 m/s cut-out; multiply capacity factor by an assumed 310 MW nameplate.
- Solar: assume a 77.5 MWp DC plant; convert horizontal irradiation using `77.5 × min(GHI/1000, 1) × 0.80`, where 0.80 is a generic aggregate derate. This is not plane-of-array transposition, temperature modelling, inverter modelling or a PVsyst simulation.
- Export: 310 MW in the input file is an arbitrary screening assumption, not an evidenced point-of-connection limit. No tariff is supplied.

NASA POWER weather values make the timing and variation more realistic than a hand-drawn profile, but spatial resolution, reanalysis error, turbine hub-height adjustment, turbine power curve and PV conversion assumptions are not validated for LTWP. The week is not representative of annual or seasonal conditions and cannot support annual generation, curtailment probability, P50/P90 yield, revenue, project returns or debt sizing.

See [the evidence dashboard](../docs/evidence_dashboard.md) and source register for evidence status. Replace the proxy with multi-year, time-aligned LTWP turbine availability/generation and curtailment, validated solar modelling, grid limits from connection documents/studies, and documented offtake terms before drawing project conclusions.
