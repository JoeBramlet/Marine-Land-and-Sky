# MLS Environmental & Infrastructure Risk Matrix (Public Evaluation Sample)

**Automated Endangered Species Act (ESA), Critical Habitat GIS & Supply-Chain Due Diligence for Real Assets, Energy & Infrastructure.**

---

## 🎯 Why This Dataset Exists
Institutional real estate funds, midstream pipeline operators, and utility-scale renewable developers lose millions every year to unexpected biological injunctions. Government portals (like USFWS IPaC and CITES) are built for field biologists—not deal teams—forcing analysts to manually read dense Federal Register PDFs just to figure out whether a species causes a minor seasonal delay or a complete project freeze.

The **MLS Environmental & Infrastructure Risk Matrix** translates **9,150+ federal and international regulatory profiles** into a single normalized, GIS- and SQL-ready underwriting table.

### 📊 Full Enterprise Dataset vs. This Public Sample

| Metric | Public Evaluation Sample (This Repo) | Full Commercial Release (v1.0) |
| :--- | :--- | :--- |
| **Total Species Profiles** | **100** (Top High-Severity Bottlenecks) | **9,150+** Unified Profiles |
| **Geographic Granularity** | All 56 U.S. States/Territories & USFWS Regions | All **56 U.S. States/Territories** + Global CITES |
| **Critical Habitat GIS Links** | Included (Direct USFWS `.zip` Shapefiles) | **429+ Active Critical Habitat GIS Overlays** |
| **Risk Severity Scoring** | `MLS-ACT-09` & `MLS-ACT-10` Deal Killers | Complete `MLS-ACT-03` through `MLS-ACT-10` Scale |
| **Customs & Trade Mapping** | 6-Digit HS Codes & CITES Appendices I–III | Complete Global CITES & FAO 3-Alpha Coverage |

---

## ⚡ Live Sample Output (North Carolina Solar Corridor Screen)
Running our interactive screening script lets analysts filter by **Industry Division**, **Physical Disturbance Activity**, **Operational Realm**, and **State / USFWS Region / USFS Forestry Region** in seconds:

```text
--- NEW PORTFOLIO DUE-DILIGENCE SCREEN ---
   Industry Divisions:     power utilities | pipeline | solar | wind | timber | dredging
   Disturbance Activities: clearing | trenching | water diversion | intake | pile-driving | blasting

1. Enter Industry Division, Disturbance Activity, or HS Code [Enter for all]: solar
2. Operational Realm (Land / Marine / Sky) [Enter for all]: land
3. State, USFWS Region, or USFS Forestry Region (e.g., NC, TX, Region 4, usfs southern) [Enter for all]: nc
4. Filter to Zero-Tolerance Blockers Only (ACT-09/10)? (y/n) [n]: n

==================================================================
📊 DEAL SCREENING SUMMARY: 13 Matching Compliance Triggers
   • Zero-Tolerance Project Blockers (ACT-09/10): 9
   • Active Critical Habitat GIS Overlays:       8
==================================================================

[1] Lichen, rock gnome (Gymnoderma lineare)
    Tier: MLS-ACT-09 | ESA: LE | CITES: Appendix I
    Restriction: Land clearing, grading, or water diversion inside designated Critical Habitat (Wherever found)

[2] Sedge, golden (Carex lutea)
    Tier: MLS-ACT-09 | ESA: LE | CITES: Appendix I | CH: 139.0 acres
    Restriction: Land clearing, grading, or water diversion inside designated Critical Habitat (Wherever found)
    GIS Polygon: https://fws.gov
```

---

## 📦 What Is Included in This Repository
* **`MLS_Investor_Sample_Top100.csv`**: A 100-row sample of our highest-liability commercial land, marine, and infrastructure bottlenecks.
* **`INVESTOR_DATA_DICTIONARY.md`**: Complete technical schema documentation for PostgreSQL, Snowflake, Excel, and ArcGIS/QGIS ingestion.
* **`demo_sample_radar.py`**: A zero-dependency Python CLI tool that runs live risk screens against the 100-row sample dataset.

### 🚀 Quickstart (Run the Sample Radar Locally)
No external pip packages required—runs on standard Python 3.8+:
```bash
git clone https://github.com/JoeBramlet/Marine-Land-and-Sky.git
cd Marine-Land-and-Sky
python demo_sample_radar.py
```

```


---
## 💼 Licensing the Full 9,150-Record Dataset
To request a custom corridor screening report, API access, or an enterprise flat-file license for all **9,150+ profiles**:
* **Founder:** Joe Bramlet — *Marine, Land & Sky Compliance Intelligence*
* **Direct Email:** [mls@globaltype.org](mailto:mls@globaltype.org)
* **LinkedIn:** [https://www.linkedin.com/in/joe-bramlet/](https://www.linkedin.com/in/joe-bramlet/)
* **Delivery Formats:** UTF-8 CSV, Master JSON, YAML, and custom regional underwriting extracts.

