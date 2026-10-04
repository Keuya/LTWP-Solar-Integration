# PV yield model and provenance record

## What is available

The repository contains `data/PVsyst_Simulation_Results.csv`, which reports for a 77.5 MWp study:

- annual `E_Grid`: 199,336,378 kWh (199.336 GWh);
- performance ratio: 0.862;
- annual `GlobHor`: 2,231.3 kWh/m²;
- annual `GlobInc`: 2,985.1 kWh/m².

## What is missing

No native PVsyst project file, project/version metadata, original weather file, exact coordinates, array orientation, module/inverter selection, loss diagram or uncertainty/P50/P90 report is included. The published CSV is a result extract, not enough information to reproduce or audit the simulation. In particular, its reported plane-of-array irradiation is materially above the horizontal irradiation and needs reconciliation with the original project and weather inputs.

## Case-study substitute

The case study therefore includes a transparent proxy, not a fabricated native PVsyst file:

- Weather provenance: NASA POWER v2.10.2 hourly 2024 series at 2.5°N, 36.8°E, supplied in `data/nasa_power_weather_2024.csv` with metadata in `data/nasa_power_weather_2024_metadata.json`.
- Proxy model: 77.5 MWp DC × hourly horizontal GHI / 1,000 × generic 0.82 aggregate performance factor, capped at the study's 74.62 MWac inverter capacity, with 99.0% assumed plant availability.
- Modelled 2024 solar availability: 142.85 GWh before grid curtailment. Under wind-priority dispatch with a 310 MW assumed shared export cap, the model exports 92.39 GWh and curtails 50.45 GWh.

The NASA grid point is regional reanalysis, not project-site pyranometer data. Horizontal GHI is not plane-of-array irradiance. The generic performance factor is not a PVsyst loss model. The annual value is not a forecast, P50, P90, independent engineer opinion or bankable yield.

## Required to create an auditable native PVsyst case

Obtain the original native project and the author/model version; confirm exact site coordinates and elevation; obtain the licensed weather file and long-term correction; reconcile `GlobHor`, `GlobInc` and the unusually high reported annual yield; confirm module/inverter configuration, tilt/azimuth, shading and loss assumptions; and obtain an independent uncertainty assessment. Only then should the native project be revised and exported from PVsyst.
