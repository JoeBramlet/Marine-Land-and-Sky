import os
import re
import csv
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_CSV = os.path.join(BASE_DIR, "MLS_Investor_Sample_Top100.csv")
REPORTS_DIR = os.path.join(BASE_DIR, "sample_client_reports")

INDUSTRY_DIVISIONS = (
    "power utilities",
    "pipeline",
    "solar",
    "wind",
    "timber",
    "dredging"
)

DISTURBANCE_ACTIVITIES = (
    "clearing",
    "trenching",
    "water diversion",
    "intake",
    "pile-driving",
    "blasting"
)

INDUSTRY_SYNONYMS = {
    "pipeline": ["pipeline", "trenching", "excavation", "corridor", "habitat disturbance", "clearing"],
    "power": ["power", "intake", "water diversion", "clearing", "corridor", "habitat disturbance", "hydro"],
    "power utilities": ["power", "utility", "intake", "water diversion", "clearing", "corridor", "habitat disturbance", "hydro"],
    "utilities": ["utility", "power", "corridor", "clearing", "water diversion", "habitat disturbance"],
    "energy": ["energy", "power", "solar", "wind", "intake", "water diversion", "clearing", "habitat disturbance"],
    "timber": ["timber", "logging", "forest", "pine", "clearcutting", "4403", "4407", "4401"],
    "dredging": ["dredging", "dredge", "channel", "port", "harbor", "pile-driving", "bulkhead", "water diversion"],
    "solar": ["solar", "grading", "clearing", "habitat disturbance", "desert", "tortoise"],
    "wind": ["wind", "rotor", "turbine", "acoustic", "offshore", "speed rule"]
}

# Maps full state/territory names to two-letter postal codes (includes all 50 states plus DC and major territories)
STATE_NAME_TO_CODE = {
    "alabama": "AL", "alaska": "AK", "arkansas": "AR", "arizona": "AZ", "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD", "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS", "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY", "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC", "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY", "washington dc": "DC", "puerto rico": "PR", "guam": "GU", "american samoa": "AS", "northern mariana islands": "MP", "virgin islands": "VI","district of columbia": "DC"
    
   
}

VALID_STATE_CODES = set(STATE_NAME_TO_CODE.values())


# Maps U.S. Forest Service (USFS) Forestry Regions to their overlapping USFWS Regions
USFS_FORESTRY_REGIONS = {
    "usfs northern": ["1", "6"],
    "usfs rocky mountain": ["6"],
    "usfs southwestern": ["2"],
    "usfs intermountain": ["1", "6", "8"],
    "usfs pacific southwest": ["8"],
    "usfs pacific northwest": ["1"],
    "usfs southern": ["2", "4", "5"],
    "usfs eastern": ["3", "5"],
    "usfs alaska": ["7"]
}

def load_master_data():
    if not os.path.exists(MASTER_CSV):
        print(f"❌ Could not find {MASTER_CSV}. Run BuildInvestorPackage.py first.")
        return []
    with open(MASTER_CSV, mode="r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def resolve_region_patterns(reg_input):
    reg = reg_input.strip().lower()
    if not reg:
        return []
    if reg in USFS_FORESTRY_REGIONS:
        nums = USFS_FORESTRY_REGIONS[reg]
        patterns = []
        for n in nums:
            patterns.extend([rf"\bregion\s*{n}\b", rf"\br{n}\b"])
        return patterns
    if reg.isdigit():
        return [rf"\bregion\s*{reg}\b", rf"\br{reg}\b"]
    if reg.startswith("region"):
        num = reg.replace("region", "").strip()
        return [rf"\bregion\s*{num}\b", rf"\br{num}\b"]
    if reg.startswith("r") and reg[1:].isdigit():
        num = reg[1:]
        return [rf"\bregion\s*{num}\b", rf"\br{num}\b"]
    return [re.escape(reg)]


def search_records(records, keyword="", realm="", region="", high_risk_only=False):
    kw = keyword.strip().lower()
    rlm = realm.strip().lower()
    reg_clean = region.strip().lower()

    # Check if the user entered a specific U.S. State or Territory
    target_state = None
    if reg_clean.upper() in VALID_STATE_CODES:
        target_state = reg_clean.upper()
    elif reg_clean in STATE_NAME_TO_CODE:
        target_state = STATE_NAME_TO_CODE[reg_clean]

    region_patterns = [] if target_state else resolve_region_patterns(region)
    kw_terms = INDUSTRY_SYNONYMS.get(kw, [kw]) if kw else []
    matches = []

    for row in records:
        if high_risk_only and not ("09" in row.get("act_tier", "") or "10" in row.get("act_tier", "")):
            continue
        if rlm and row.get("realm", "").lower() != rlm:
            continue

        # Exact State Filter (matches only species documented in that state)
        if target_state:
            states_list = [s.strip().upper() for s in row.get("states_present", "").split(",") if s.strip()]
            if target_state not in states_list:
                continue
        elif region_patterns:
            reg_blob = f"{row.get('lead_fws_region', '')} {row.get('federal_register_citation', '')}".lower()
            if not any(re.search(pat, reg_blob) for pat in region_patterns):
                continue

        if kw_terms:
            searchable = " ".join([
                row.get("common_name", ""),
                row.get("scientific_name", ""),
                row.get("category_id", ""),
                row.get("hscode_associated_prefix", ""),
                row.get("prohibited_gear_or_activity", ""),
                row.get("customs_instruction_note", ""),
                row.get("designated_footprint", "")
            ]).lower()
            if not any(kt in searchable for kt in kw_terms):
                continue
        matches.append(row)

    def priority(r):
        score = 0
        if "10" in r.get("act_tier", ""):
            score += 50
        elif "09" in r.get("act_tier", ""):
            score += 35
        if r.get("critical_habitat_status", "None") not in ("None", ""):
            score += 40
        return score

    return sorted(matches, key=priority, reverse=True)

def export_custom_report(matches, label):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_label = "".join(c if c.isalnum() else "_" for c in label).strip("_") or "query"
    out_path = os.path.join(REPORTS_DIR, f"Client_DueDiligence_{clean_label}_{stamp}.csv")

    with open(out_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=next(iter(matches)).keys())
        writer.writeheader()
        writer.writerows(matches)
    print(f"📁 Saved client-ready screening report: {out_path}")

def run_interactive_demo():
    records = load_master_data()
    if not records:
        return

    print("==================================================================")
    print("🏢 MLS PORTFOLIO RISK RADAR — PUBLIC EVALUATION SAMPLE (100 HIGH-SEVERITY PROFILES)")
    print(f"   Loaded {len(records):,} Active Global & Federal Compliance Profiles")
    print("==================================================================")

    while True:
        print("\n--- NEW PORTFOLIO DUE-DILIGENCE SCREEN ---")
        print(f"   Industry Divisions:     {' | '.join(INDUSTRY_DIVISIONS)}")
        print(f"   Disturbance Activities: {' | '.join(DISTURBANCE_ACTIVITIES)}")
        keyword = input("\n1. Enter Industry Division, Disturbance Activity, or HS Code [Enter for all]: ")
        realm = input("2. Operational Realm (Land / Marine / Sky) [Enter for all]: ")
        region = input("3. State, USFWS Region, or USFS Forestry Region (e.g., NC, TX, Region 4, usfs southern) [Enter for all]: ")
        hr_input = input("4. Filter to Zero-Tolerance Blockers Only (ACT-09/10)? (y/n) [n]: ").strip().lower()
        high_risk_only = (hr_input == "y")

        matches = search_records(records, keyword, realm, region, high_risk_only)
        crithab_hits = sum(1 for m in matches if m.get("critical_habitat_status", "None") not in ("None", ""))
        zt_hits = sum(1 for m in matches if "09" in m.get("act_tier", "") or "10" in m.get("act_tier", ""))

        print("\n==================================================================")
        print(f"📊 DEAL SCREENING SUMMARY: {len(matches):,} Matching Compliance Triggers")
        print(f"   • Zero-Tolerance Project Blockers (ACT-09/10): {zt_hits:,}")
        print(f"   • Active Critical Habitat GIS Overlays:       {crithab_hits:,}")
        print("==================================================================")

        for i, m in enumerate(matches[:10], start=1):
            ch_tag = f" | CH: {m['designated_footprint']}" if m.get("critical_habitat_status", "None") not in ("None", "") else ""
            print(f"\n[{i}] {m['common_name']} ({m['scientific_name']})")
            print(f"    Tier: {m['act_tier']} | ESA: {m['usfws_esa_status_code']} | CITES: {m['cites_appendix_tier']}{ch_tag}")
            print(f"    Restriction: {m['prohibited_gear_or_activity'][:95]}")
            if m.get("gis_shapefile_url") not in ("N/A", ""):
                print(f"    GIS Polygon: {m['gis_shapefile_url']}")

        if len(matches) > 10:
            print(f"\n... plus {len(matches) - 10:,} additional matching records.")

        if matches:
            save_q = input("\n💾 Export this screening result to a client-ready CSV? (y/n) [n]: ").strip().lower()
            if save_q == "y":
                export_custom_report(matches, keyword or realm or region or "full_screen")

        again = input("\n🔄 Run another portfolio screen? (y/n) [y]: ").strip().lower()
        if again == "n":
            print("👋 Closing Portfolio Risk Radar. Ready for investor outreach!")
            break

if __name__ == "__main__":
        run_interactive_demo()
