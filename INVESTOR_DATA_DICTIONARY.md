# MLS Environmental & Infrastructure Risk Matrix — Data Dictionary
**Release Date:** 2026-11-12 | **Total Active Profiles:** 9,150 | **High-Severity Bottlenecks (ACT-09/10):** 1,658 | **Critical Habitat GIS Records:** 950

## Overview
This dataset normalizes federal Endangered Species Act (ESA) listings, USFWS Active Critical Habitat boundaries, CITES trade appendices, and Harmonized System (HS) logistics codes into a flat underwriting table for infrastructure funds, REITs, energy developers, and supply-chain compliance teams.

## Schema Field Definitions

| Column Name | Type | Description |
| :--- | :--- | :--- |
| `g_sequence` | String | Unique master sequence identifier (`mls_2026_m###`). |
| `id_slug` | String | Machine-readable canonical species key. |
| `realm` | String | Primary operational domain (`Land`, `Marine`, or `Sky`). |
| `common_name` | String | Standard English name and commercial bottleneck tag. |
| `scientific_name` | String | Standardized binomial or trinomial taxonomic name. |
| `category_id` | String | Taxonomic family or regulatory group key (e.g., `cat_percidae`, `cat_unionidae_fws`). |
| `act_tier` | String | Internal regulatory severity scale (`MLS-ACT-03` Moderate to `MLS-ACT-10` Zero-Tolerance Freeze). |
| `enforcement_threat_level` | String | Underwriting risk flag (`High` or `Moderate`). |
| `usfws_esa_status_code` | String | Federal status (`LE` = Listed Endangered, `LT` = Listed Threatened, `CITES` = International Appendix). |
| `cites_appendix_tier` | String | CITES trade appendix (`Appendix I`, `Appendix II`, `Appendix III`, or `Not Listed`). |
| `critical_habitat_status` | String | USFWS Critical Habitat designation status (`Final`, `Proposed`, or `None`). |
| `designated_footprint` | String | Legally protected land acreage or river-mile footprint. |
| `gis_shapefile_url` | URL | Direct download link to official USFWS Critical Habitat GIS `.zip` polygon boundary. |
| `lead_fws_region` | String | Lead U.S. Fish & Wildlife Service administrative region. |
| `federal_register_citation` | String | Codified Federal Register rule date, volume/page, or ECOS reference. |
| `hscode_associated_prefix` | String | 6-digit Harmonized System (HS) customs commodity code linked to habitat/trade transit. |
| `is_zero_tolerance_trade` | Boolean | `True` when `MLS-ACT-09` or `MLS-ACT-10` prohibits unpermitted commercial activity. |
| `fao_3alpha_code` | String | UN FAO 3-letter species code for maritime and fishery manifests. |
| `target_demographic` | String | Primary regulated industries impacted by this species. |
| `prohibited_gear_or_activity` | String | Specific land-clearing, dredging, or transit activities restricted without Section 7/10 permits. |
| `customs_instruction_note` | String | Actionable compliance screening directive for legal and logistics teams. |
