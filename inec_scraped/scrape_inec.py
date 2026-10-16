#!/usr/bin/env python3
"""
Scrape all polling units from INEC's CVR portal.
Outputs: /tmp/nigeria-map/inec_scraped/
"""
import urllib.request, json, time, os, sys, re
from concurrent.futures import ThreadPoolExecutor, as_completed

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
BASE = "https://cvr.inecnigeria.org"
API = BASE + "/PublicApi/"
OUT = "/tmp/nigeria-map/inec_scraped"
os.makedirs(OUT, exist_ok=True)

STATES_HTML_IDS = {
    "1": "ABIA", "2": "ADAMAWA", "3": "AKWA IBOM", "4": "ANAMBRA",
    "5": "BAUCHI", "6": "BAYELSA", "7": "BENUE", "8": "BORNO",
    "9": "CROSS RIVER", "10": "DELTA", "11": "EBONYI", "12": "EDO",
    "13": "EKITI", "14": "ENUGU", "15": "FCT", "16": "GOMBE",
    "17": "IMO", "18": "JIGAWA", "19": "KADUNA", "20": "KANO",
    "21": "KATSINA", "22": "KEBBI", "23": "KOGI", "24": "KWARA",
    "25": "LAGOS", "26": "NASARAWA", "27": "NIGER", "28": "OGUN",
    "29": "ONDO", "30": "OSUN", "31": "OYO", "32": "PLATEAU",
    "33": "RIVERS", "34": "SOKOTO", "35": "TARABA", "36": "YOBE",
    "37": "ZAMFARA"
}

def api_get(endpoint, params, retries=3):
    qs = "&".join(f"data[Search][{k}]={v}" for k, v in params.items())
    url = API + endpoint + "?" + qs
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=15) as r:
                raw = json.loads(r.read())
            data = raw[0] if isinstance(raw, list) else raw
            return {k: v for k, v in data.items() if k not in ("0", "selected")}
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
            else:
                print(f"  FAILED: {url} — {e}", file=sys.stderr)
                return {}

def get_coordinates(state_id, lga_id, ward_id, pu_id, retries=3):
    for attempt in range(retries):
        try:
            data = (
                f"data[Search][state_id]={state_id}"
                f"&data[Search][local_government_id]={lga_id}"
                f"&data[Search][registration_area_id]={ward_id}"
                f"&data[Search][polling_unit_id]={pu_id}"
            ).encode()
            req = urllib.request.Request(
                BASE + "/pu_locator/index",
                data=data,
                headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded"},
                method="POST"
            )
            opener = urllib.request.build_opener(NoRedirectHandler())
            resp = opener.open(req, timeout=15)
            loc = resp.headers.get("Location", "")
            m = re.search(r'q=([-\d.]+),([-\d.]+)', loc)
            if m:
                try:
                    return float(m.group(1)), float(m.group(2))
                except ValueError:
                    return None, None
            return None, None
        except urllib.error.HTTPError as e:
            loc = e.headers.get("Location", "")
            m = re.search(r'q=([-\d.]+),([-\d.]+)', loc)
            if m:
                try:
                    return float(m.group(1)), float(m.group(2))
                except ValueError:
                    return None, None
            if attempt < retries - 1:
                time.sleep(0.5)
            return None, None
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(0.5)
            else:
                return None, None

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(newurl, code, msg, headers, fp)

def parse_code(label):
    m = re.match(r'(\d+)\s*-\s*(.*)', label.strip())
    if m:
        return m.group(1), m.group(2).strip()
    return "", label.strip()

def scrape_state(state_id, state_name):
    state_file = os.path.join(OUT, f"state_{state_id}_{state_name.lower().replace(' ', '-').replace('/', '-')}.json")
    if os.path.exists(state_file):
        with open(state_file) as f:
            data = json.load(f)
        total_pus = sum(len(w.get("pus", [])) for l in data.get("lgas", []) for w in l.get("wards", []))
        if total_pus > 0:
            print(f"  [{state_name}] Already scraped ({total_pus} PUs), skipping hierarchy")
            return data

    print(f"  [{state_name}] Fetching LGAs...")
    lgas_raw = api_get("lgas/1/Search", {"state_id": state_id})
    time.sleep(0.15)

    state_data = {"id": state_id, "name": state_name, "lgas": []}

    for lga_id, lga_label in sorted(lgas_raw.items(), key=lambda x: x[1]):
        lga_code, lga_name = parse_code(lga_label)
        wards_raw = api_get("wards/1/Search", {"local_government_id": lga_id})
        time.sleep(0.15)

        lga_data = {"id": lga_id, "code": lga_code, "name": lga_name, "wards": []}

        for ward_id, ward_label in sorted(wards_raw.items(), key=lambda x: x[1]):
            ward_code, ward_name = parse_code(ward_label)
            pus_raw = api_get("pus/1/Search", {"registration_area_id": ward_id})
            time.sleep(0.15)

            ward_data = {"id": ward_id, "code": ward_code, "name": ward_name, "pus": []}

            for pu_id, pu_label in sorted(pus_raw.items(), key=lambda x: x[1]):
                pu_code, pu_name = parse_code(pu_label)
                ward_data["pus"].append({
                    "id": pu_id, "code": pu_code, "name": pu_name
                })

            lga_data["wards"].append(ward_data)

        state_data["lgas"].append(lga_data)
        ward_count = len(lga_data["wards"])
        pu_count = sum(len(w["pus"]) for w in lga_data["wards"])
        print(f"    [{state_name}] {lga_name}: {ward_count} wards, {pu_count} PUs")

    total_pus = sum(len(w["pus"]) for l in state_data["lgas"] for w in l["wards"])
    print(f"  [{state_name}] DONE — {len(state_data['lgas'])} LGAs, {total_pus} PUs")

    with open(state_file, "w") as f:
        json.dump(state_data, f)

    return state_data

def scrape_coordinates_for_state(state_file):
    with open(state_file) as f:
        state_data = json.load(f)

    state_name = state_data["name"]
    state_id = state_data["id"]
    coord_file = state_file.replace(".json", "_coords.json")

    # Load existing coords if resuming
    existing = {}
    if os.path.exists(coord_file):
        with open(coord_file) as f:
            existing = json.load(f)

    total = 0
    done = len(existing)
    for lga in state_data["lgas"]:
        for ward in lga["wards"]:
            total += len(ward["pus"])

    if done >= total and total > 0:
        print(f"  [{state_name}] Coords complete ({done}/{total})")
        return existing

    print(f"  [{state_name}] Fetching coords ({done}/{total} done)...")
    count = 0
    batch_size = 50

    for lga in state_data["lgas"]:
        for ward in lga["wards"]:
            for pu in ward["pus"]:
                pu_id = pu["id"]
                if pu_id in existing:
                    count += 1
                    continue

                lat, lng = get_coordinates(state_id, lga["id"], ward["id"], pu_id)
                existing[pu_id] = {"lat": lat, "lng": lng}
                count += 1

                if count % batch_size == 0:
                    with open(coord_file, "w") as f:
                        json.dump(existing, f)
                    pct = count * 100 // total
                    print(f"    [{state_name}] {count}/{total} ({pct}%)")

                time.sleep(0.1)

    with open(coord_file, "w") as f:
        json.dump(existing, f)

    coords_found = sum(1 for v in existing.values() if v["lat"] is not None)
    print(f"  [{state_name}] Coords DONE — {coords_found}/{total} have GPS")
    return existing

# ============ MAIN ============

print("=" * 60)
print("PHASE 1: Scrape hierarchy (states → LGAs → wards → PUs)")
print("=" * 60)

all_states = {}
for sid, sname in sorted(STATES_HTML_IDS.items(), key=lambda x: int(x[0])):
    all_states[sid] = scrape_state(sid, sname)

grand_total = sum(
    len(w["pus"])
    for s in all_states.values()
    for l in s["lgas"]
    for w in l["wards"]
)
print(f"\nHierarchy complete: {grand_total} polling units across {len(all_states)} states")

print("\n" + "=" * 60)
print("PHASE 2: Scrape GPS coordinates for each polling unit")
print("=" * 60)

state_files = sorted([
    os.path.join(OUT, f) for f in os.listdir(OUT)
    if f.startswith("state_") and not f.endswith("_coords.json")
])

for sf in state_files:
    scrape_coordinates_for_state(sf)

print("\n" + "=" * 60)
print("DONE!")
print("=" * 60)
