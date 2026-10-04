#!/usr/bin/env python3
"""Build an illustrative LTWP-area interval case from public data.

The interval profiles are modelled. Wind shape is normalized to LTWP's
published 2024 annual net-generation anchor; it is not LTWP interval telemetry.
"""
import argparse, csv, json, math, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path

LAT, LON = 2.5, 36.8
START, END = "20240101", "20241231"
WIND_NAMEPLATE_MW, SOLAR_DC_MWP, SOLAR_AC_MW = 310.25, 77.5, 74.62
WIND_HUB_HEIGHT_M, WIND_SHEAR_EXPONENT = 80.0, 0.14
CUT_IN, RATED, CUT_OUT = 3.5, 12.0, 25.0
WIND_AVAILABILITY_PCT, SOLAR_AVAILABILITY_PCT, SOLAR_PR = 98.5, 99.0, 0.82
WIND_ANNUAL_NET_ANCHOR_MWH = 1_367_000.0
BASE_CURTAILMENT_LIMIT_MW, SCENARIO_ENVELOPE_MW = 310.0, 400.0


def request_weather():
    q = {"parameters":"ALLSKY_SFC_SW_DWN,WS50M","community":"RE","longitude":LON,"latitude":LAT,
         "start":START,"end":END,"format":"JSON","time-standard":"UTC"}
    url = "https://power.larc.nasa.gov/api/temporal/hourly/point?" + urllib.parse.urlencode(q)
    with urllib.request.urlopen(url, timeout=60) as response:
        payload = json.load(response)
    return url, payload


def generic_wind_cf(ws50):
    ws80 = ws50 * (WIND_HUB_HEIGHT_M / 50.0) ** WIND_SHEAR_EXPONENT
    if ws80 < CUT_IN or ws80 >= CUT_OUT:
        return 0.0
    if ws80 >= RATED:
        return 1.0
    return ((ws80 - CUT_IN) / (RATED - CUT_IN)) ** 3


def calibrate_wind_scale(raw_cfs):
    """Find a scalar on the generic power-curve shape to match annual net MWh."""
    lo, hi = 0.0, 100.0
    target = WIND_ANNUAL_NET_ANCHOR_MWH
    for _ in range(100):
        mid = (lo + hi) / 2
        annual = sum(min(1.0, cf * mid) * WIND_NAMEPLATE_MW * WIND_AVAILABILITY_PCT / 100
                     for cf in raw_cfs)
        if annual < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--weather", type=Path, default=Path("data/nasa_power_weather_2024.csv"))
    p.add_argument("--output", type=Path, default=Path("data/case_study_hourly_2024.csv"))
    p.add_argument("--fetch", action="store_true")
    args = p.parse_args()
    if args.fetch:
        url, payload = request_weather()
        par = payload["properties"]["parameter"]
        ghi, wind = par["ALLSKY_SFC_SW_DWN"], par["WS50M"]
        args.weather.parent.mkdir(parents=True, exist_ok=True)
        with args.weather.open("w", newline="", encoding="utf-8") as f:
            w=csv.writer(f); w.writerow(["timestamp_utc","wind_speed_50m_m_s","ghi_wh_m2"])
            for k in sorted(ghi):
                ts=k[:4]+"-"+k[4:6]+"-"+k[6:8]+"T"+k[8:10]+":00:00Z"
                w.writerow([ts,"%.2f"%wind[k],"%.2f"%ghi[k]])
        meta={"query_url":url,"api":payload["header"]["api"],"sources":payload["header"]["sources"],
              "time_standard":payload["header"]["time_standard"],"period":[START,END],
              "coordinates":payload["geometry"]["coordinates"],"parameters":payload["parameters"]}
        args.weather.with_name("nasa_power_weather_2024_metadata.json").write_text(json.dumps(meta,indent=2)+"\n")
    with args.weather.open(newline="",encoding="utf-8") as f:
        weather=list(csv.DictReader(f))
    if len(weather)!=8784:
        raise ValueError("Expected 8,784 hourly rows for leap year 2024; got %d"%len(weather))
    raw_cfs=[generic_wind_cf(float(r["wind_speed_50m_m_s"])) for r in weather]
    wind_scale=calibrate_wind_scale(raw_cfs)
    fields=["timestamp","wind_available_mw","solar_available_mw","export_limit_mw",
            "wind_availability_pct","solar_availability_pct","wind_export_mw_310","wind_curtailment_mw_310","solar_export_mw_310",
            "solar_curtailment_mw_310","curtailment_cause_310"]
    totals={k:0.0 for k in ("wind_available_mwh","wind_export_310_mwh","wind_curtailment_310_mwh",
                            "solar_available_mwh","solar_export_310_mwh","solar_curtailment_310_mwh")}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r,cf in zip(weather,raw_cfs):
            ws50,ghi=float(r["wind_speed_50m_m_s"]),max(0,float(r["ghi_wh_m2"]))
            wind=min(1.0,cf*wind_scale)*WIND_NAMEPLATE_MW*WIND_AVAILABILITY_PCT/100
            solar=min(SOLAR_AC_MW,SOLAR_DC_MWP*ghi/1000*SOLAR_PR)*SOLAR_AVAILABILITY_PCT/100
            wind_exp=min(wind,BASE_CURTAILMENT_LIMIT_MW)
            solar_exp=min(solar,max(0,BASE_CURTAILMENT_LIMIT_MW-wind_exp))
            wc=max(0,wind-wind_exp);sc=max(0,solar-solar_exp)
            cause="none" if wc+sc<1e-8 else ("wind_priority_shared_poi_headroom" if sc>0 else "assumed_export_limit")
            ts=r["timestamp_utc"].replace("+00:00","Z")
            w.writerow({"timestamp":ts,"wind_available_mw":"%.2f"%wind,"solar_available_mw":"%.2f"%solar,
                        "export_limit_mw":"%.2f"%SCENARIO_ENVELOPE_MW,
                        "wind_availability_pct":"%.2f"%WIND_AVAILABILITY_PCT,
                        "solar_availability_pct":"%.2f"%SOLAR_AVAILABILITY_PCT,
                        "wind_export_mw_310":"%.2f"%wind_exp,"wind_curtailment_mw_310":"%.2f"%wc,
                        "solar_export_mw_310":"%.2f"%solar_exp,"solar_curtailment_mw_310":"%.2f"%sc,
                        "curtailment_cause_310":cause})
            for k,v in (("wind_available_mwh",wind),("wind_export_310_mwh",wind_exp),
                        ("wind_curtailment_310_mwh",wc),("solar_available_mwh",solar),
                        ("solar_export_310_mwh",solar_exp),("solar_curtailment_310_mwh",sc)):
                totals[k]+=v
    print("wind_curve_scale=%.6f (calibrated to public 2024 aggregate; interval shape remains unverified)"%wind_scale)
    for k,v in totals.items():print("%s=%.2f"%(k,v))

if __name__=="__main__":main()
