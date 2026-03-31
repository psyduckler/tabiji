#!/usr/bin/env python3
"""
Sync hospitals, disasterResponse, scams, medications from api/v1/safety/ → kit/data/safety/
"""
import json, os, glob

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_dir = os.path.join(repo, "api/v1/safety")
kit_dir = os.path.join(repo, "kit/data/safety")

kit_files = sorted(glob.glob(f"{kit_dir}/*.json"))
kit_isos = [os.path.basename(f).replace(".json","") for f in kit_files]

synced = {f: [] for f in ["hospitals","disasterResponse","scams","medications"]}

for iso in kit_isos:
    kf = os.path.join(kit_dir, f"{iso}.json")
    af = os.path.join(api_dir, f"{iso}.json")
    if not os.path.exists(af):
        print(f"  SKIP {iso}: no api file")
        continue

    with open(kf) as fh: k = json.load(fh)
    with open(af) as fh: a = json.load(fh)

    changed = False

    # hospitals
    api_hospitals = a.get("hospitals", [])
    if api_hospitals and not k.get("hospitals"):
        k["hospitals"] = api_hospitals
        synced["hospitals"].append(iso)
        changed = True

    # disasterResponse
    api_dr = a.get("disasterResponse")
    if api_dr and not k.get("disasterResponse"):
        k["disasterResponse"] = api_dr
        synced["disasterResponse"].append(iso)
        changed = True

    # scams — only if kit is empty and api has entries
    api_scams = a.get("scams", [])
    kit_scams = k.get("scams", [])
    if api_scams and not kit_scams:
        k["scams"] = api_scams
        synced["scams"].append(iso)
        changed = True

    # medications — only if kit is empty and api has data
    api_meds = a.get("medications")
    kit_meds = k.get("medications")
    if api_meds and not kit_meds:
        k["medications"] = api_meds
        synced["medications"].append(iso)
        changed = True

    if changed:
        with open(kf, "w") as fh:
            json.dump(k, fh, indent=2, ensure_ascii=False)
            fh.write("\n")

for field, isos in synced.items():
    print(f"{field}: synced {len(isos)} countries")

print("\nDone.")
