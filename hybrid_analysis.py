#!/usr/bin/env python3
"""Chronological LTWP wind + solar dispatch screening.

A transparent screening tool, not a production-cost model, grid study, PPA model
or lender model. No synthetic resource profiles are generated.
"""
import argparse
import csv
from datetime import datetime
from pathlib import Path
from statistics import median

REQUIRED = ("timestamp", "wind_available_mw", "solar_available_mw", "export_limit_mw")
POLICIES = ("solar_priority", "wind_priority", "pro_rata")


def read_profiles(path):
    if not path.exists():
        raise ValueError("Input file not found: " + str(path))
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(missing))
        rows = []
        for line, raw in enumerate(reader, start=2):
            if not any((v or "").strip() for v in raw.values()):
                continue
            try:
                stamp = datetime.fromisoformat(raw["timestamp"].strip().replace("Z", "+00:00"))
            except (ValueError, AttributeError) as exc:
                raise ValueError("Line %d: timestamp must be ISO-8601." % line) from exc
            if stamp.tzinfo is None:
                raise ValueError("Line %d: timestamp must include a timezone." % line)
            row = {"timestamp": stamp}
            for name in REQUIRED[1:]:
                try:
                    row[name] = float(raw[name])
                except (ValueError, TypeError) as exc:
                    raise ValueError("Line %d: %s must be numeric." % (line, name)) from exc
                if row[name] < 0:
                    raise ValueError("Line %d: %s cannot be negative." % (line, name))
            price = (raw.get("energy_price_usd_mwh") or "").strip()
            row["energy_price_usd_mwh"] = float(price) if price else None
            rows.append(row)
    if len(rows) < 2:
        raise ValueError("At least two timestamped records are needed to infer interval length.")
    rows.sort(key=lambda r: r["timestamp"])
    steps = [(rows[i+1]["timestamp"]-rows[i]["timestamp"]).total_seconds()/3600
             for i in range(len(rows)-1)]
    if any(x <= 0 for x in steps):
        raise ValueError("Timestamps must be unique and strictly increasing.")
    step = median(steps)
    if any(abs(x-step) > 1e-6 for x in steps):
        raise ValueError("Intervals must be regular; resample or split the input.")
    if step > 24:
        raise ValueError("Inferred interval exceeds 24 hours; supply sub-daily data.")
    return rows, step


def allocate(wind, solar, limit, policy):
    if wind + solar <= limit:
        return wind, solar
    if policy == "solar_priority":
        s = min(solar, limit)
        return min(wind, max(0.0, limit-s)), s
    if policy == "wind_priority":
        w = min(wind, limit)
        return w, min(solar, max(0.0, limit-w))
    scale = limit / (wind + solar) if wind + solar else 0.0
    return wind*scale, solar*scale


def parse_caps(value):
    if not value:
        return [("input_export_limit", None)]
    result = []
    for item in value.split(","):
        cap = float(item.strip())
        if cap <= 0:
            raise ValueError("Scenario caps must be positive MW values.")
        result.append(("scenario_cap_%g_mw" % cap, cap))
    return result


def run(rows, hours, caps, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    detail_fields = ("timestamp,scenario,dispatch_policy,interval_hours,"
        "wind_only_export_mwh,hybrid_wind_export_mwh,hybrid_solar_export_mwh,"
        "hybrid_total_export_mwh,wind_curtailed_mwh,solar_curtailed_mwh,"
        "incremental_hybrid_export_mwh,illustrative_revenue_usd").split(",")
    summaries = []
    with (outdir/"hourly_dispatch.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=detail_fields)
        writer.writeheader()
        for scenario, cap in caps:
            for policy in POLICIES:
                sums = {k: 0.0 for k in ("wind_only_export_mwh","hybrid_wind_export_mwh",
                    "hybrid_solar_export_mwh","wind_curtailed_mwh","solar_curtailed_mwh",
                    "incremental_hybrid_export_mwh","illustrative_revenue_usd")}
                price_complete = True
                for r in rows:
                    limit = min(r["export_limit_mw"], cap) if cap is not None else r["export_limit_mw"]
                    wind, solar = r["wind_available_mw"], r["solar_available_mw"]
                    wo = min(wind, limit)*hours
                    hw, hs = allocate(wind, solar, limit, policy)
                    hw, hs = hw*hours, hs*hours
                    wc, sc = max(0.0,wind-hw/hours)*hours, max(0.0,solar-hs/hours)*hours
                    total = hw+hs
                    incremental = total-wo
                    price = r["energy_price_usd_mwh"]
                    if price is None:
                        price_complete = False
                    else:
                        sums["illustrative_revenue_usd"] += total*price
                    vals = {
                        "timestamp":r["timestamp"].isoformat(),"scenario":scenario,
                        "dispatch_policy":policy,"interval_hours":hours,
                        "wind_only_export_mwh":wo,"hybrid_wind_export_mwh":hw,
                        "hybrid_solar_export_mwh":hs,"hybrid_total_export_mwh":total,
                        "wind_curtailed_mwh":wc,"solar_curtailed_mwh":sc,
                        "incremental_hybrid_export_mwh":incremental,
                        "illustrative_revenue_usd":"" if price is None else total*price}
                    writer.writerow(vals)
                    for k in ("wind_only_export_mwh","hybrid_wind_export_mwh",
                              "hybrid_solar_export_mwh","wind_curtailed_mwh",
                              "solar_curtailed_mwh","incremental_hybrid_export_mwh"):
                        sums[k] += vals[k]
                if not price_complete:
                    sums["illustrative_revenue_usd"] = ""
                summaries.append({"scenario":scenario,"dispatch_policy":policy,
                    "interval_hours":hours,"records":len(rows),**sums,
                    "revenue_note":("Illustrative only; supplied prices are not evidence of a PPA."
                    if price_complete else "Not calculated: price missing in one or more intervals.")})
    with (outdir/"dispatch_scenarios.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)
    return summaries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/hourly_profile_template.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--scenario-caps-mw", default=None,
        help="Optional sensitivities such as 100,200,300,400 MW; illustrative absent grid evidence.")
    args = parser.parse_args()
    try:
        rows, hours = read_profiles(args.input)
        results = run(rows, hours, parse_caps(args.scenario_caps_mw), args.output_dir)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print("Processed %d records at %g-hour intervals." % (len(rows), hours))
    print("Wrote hourly_dispatch.csv and dispatch_scenarios.csv to %s" % args.output_dir)
    for r in results:
        total = r["hybrid_wind_export_mwh"] + r["hybrid_solar_export_mwh"]
        print("%s | %s | wind-only %.1f MWh | hybrid %.1f MWh | incremental %.1f MWh" %
              (r["scenario"],r["dispatch_policy"],r["wind_only_export_mwh"],
               total,r["incremental_hybrid_export_mwh"]))


if __name__ == "__main__":
    main()
