#!/usr/bin/env python3
"""
Sync professionals from Impulse ADHD (impulseadhd.github.io) into doctors.json.

Usage:
    python scripts/sync_impulse.py              # Dry run - shows what would change
    python scripts/sync_impulse.py --apply      # Actually writes to doctors.json

Data source: https://impulseadhd.github.io (r/adhdindia community project)
"""

import json
import subprocess
import sys
import re
from pathlib import Path

SUPABASE_URL = "https://fmxxpaficuiwrenuhlvk.supabase.co/rest/v1/professionals"
API_KEY = "sb_publishable_d6RIJyr-BwOm2sRpUNT3uQ_c3oKchg9"
DOCTORS_JSON = Path(__file__).parent.parent / "data" / "doctors.json"

SELECT_FIELDS = (
    "*,"
    "city:cities!city_id(name,province,alias),"
    "reviews:reviews!professional_id("
    "id,reviewer_name,reviewer_city,rating,review_text,created_at"
    ")"
)

HEADERS = {
    "accept": "*/*",
    "accept-profile": "public",
    "apikey": API_KEY,
    "authorization": f"Bearer {API_KEY}",
    "origin": "https://impulseadhd.github.io",
    "referer": "https://impulseadhd.github.io/",
}

# Map Impulse province names to our state names (handle known mismatches)
PROVINCE_MAP = {
    "Delhi": "Delhi",
    "Madhya Pradesh": "Madhya Pradesh",
    "Uttar Pradesh": "Uttar Pradesh",
    "Punjab": "Punjab",  # Chandigarh is listed under Punjab in their data
}


def fetch_professionals(mode: str) -> list[dict]:
    """Fetch approved professionals for a given mode (Online/Offline)."""
    import urllib.request
    import urllib.parse

    params = urllib.parse.urlencode({
        "select": SELECT_FIELDS,
        "approved_status": "eq.approved",
        "reviews.approved_status": "eq.approved",
        "mode": f"cs.{{{mode}}}",
        "order": "review_count.desc,full_name.asc",
    })
    url = f"{SUPABASE_URL}?{params}"

    req = urllib.request.Request(url)
    for k, v in HEADERS.items():
        req.add_header(k, v)

    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def make_slug(name: str, city: str) -> str:
    """Generate a URL-friendly slug from name and city."""
    text = f"{name} {city}".lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text.strip())
    text = re.sub(r"-+", "-", text)
    return text


def map_teleconsult(modes: list[str] | None) -> str:
    if not modes:
        return "unknown"
    if "Online" in modes:
        return "yes"
    return "no"


def map_stimulant(value: str | None) -> str:
    if not value:
        return "unknown"
    v = value.lower()
    if v.startswith("yes"):
        return "yes"
    if v.startswith("no"):
        return "no"
    return "unknown"


def map_diagnosis(value: str | None) -> str:
    if not value:
        return "unknown"
    v = value.lower()
    if "yes" in v:
        return "yes"
    if "no" in v:
        return "no"
    return "unknown"


def map_profession(profession: str | None) -> str:
    if not profession:
        return "psychiatrist"
    p = profession.lower()
    if "therapist" in p:
        return "therapist"
    if "psychologist" in p:
        return "psychologist"
    return "psychiatrist"


JUNK_PATTERNS = ["not sure", "not aware", "n/a", "don't know", "unknown", "online only", "i'm not", "don't remember"]


def build_address(p: dict) -> str:
    parts = [p.get("address1"), p.get("address2"), p.get("address3")]
    addr = ", ".join(part for part in parts if part) or ""
    lower = addr.lower().strip()
    if not lower or lower in ("-", "na"):
        return ""
    for pat in JUNK_PATTERNS:
        if pat in lower:
            return ""
    return addr


def build_fee(p: dict) -> str:
    charges = p.get("consultation_charges")
    if charges:
        return f"\u20b9{int(charges)}"
    return ""


def convert_professional(p: dict) -> dict:
    """Convert an Impulse professional to our doctors.json schema."""
    city_data = p.get("city") or {}
    city_name = city_data.get("name", "")
    state = city_data.get("province", "")
    full_name = (p.get("full_name") or "").replace("  ", " ").strip()

    return {
        "id": make_slug(full_name, city_name),
        "name": full_name,
        "type": map_profession(p.get("profession")),
        "city": city_name,
        "state": state,
        "address": build_address(p),
        "website": p.get("online_website_url") or "",
        "contact": p.get("contact_number") or "",
        "booking_link": "",
        "languages": [],
        "teleconsult": map_teleconsult(p.get("mode")),
        "fee_range": build_fee(p),
        "wait_time_estimate": "",
        "last_verified": "2026-03-06",
        "verification_tier": "community-verified",
        "source": "impulse-adhd",
        "adult_adhd": map_diagnosis(p.get("adhd_diagnosis_type")),
        "child_adhd": "unknown",
        "adolescent_adhd": "unknown",
        "assessment_style": "unknown",
        "med_mgmt": "yes" if map_stimulant(p.get("prescribes_stimulants")) == "yes" else "unknown",
        "stimulant_comfort": map_stimulant(p.get("prescribes_stimulants")),
        "comorbidities": [],
        "tags": ["adhd-aware"],
        "flags": [],
    }


CITY_ALIASES = {
    "gurugram": "gurgaon",
    "gurgaon": "gurugram",
    "bengaluru": "bangalore",
    "bangalore": "bengaluru",
    "mumbai": "bombay",
    "bombay": "mumbai",
    "chennai": "madras",
    "madras": "chennai",
    "kolkata": "calcutta",
    "calcutta": "kolkata",
    "thiruvananthapuram": "trivandrum",
    "trivandrum": "thiruvananthapuram",
    "kochi": "cochin",
    "cochin": "kochi",
}


def cities_match(city1: str, city2: str) -> bool:
    c1 = city1.lower().strip()
    c2 = city2.lower().strip()
    if c1 == c2:
        return True
    return CITY_ALIASES.get(c1) == c2


def normalize_name(name: str) -> str:
    """Strip prefixes and normalize for comparison."""
    for prefix in ["Dr.", "Ms.", "Mr.", "Mrs."]:
        name = name.replace(prefix, "")
    return " ".join(name.split()).lower().strip()


def names_match(name1: str, name2: str) -> bool:
    """Fuzzy name matching - handles partial names, typos in last chars."""
    n1 = normalize_name(name1)
    n2 = normalize_name(name2)
    if n1 == n2:
        return True
    # One name is a prefix of the other (e.g., "Porrselvi" vs "Porrselvi AP")
    if n1.startswith(n2) or n2.startswith(n1):
        return True
    # Same first name, similar last name (1 char diff, e.g., Hazra vs Hajra)
    parts1 = n1.split()
    parts2 = n2.split()
    if len(parts1) >= 2 and len(parts2) >= 2 and parts1[0] == parts2[0]:
        # Check if last names are within 1 edit
        l1, l2 = parts1[-1], parts2[-1]
        if len(l1) == len(l2) and sum(a != b for a, b in zip(l1, l2)) <= 1:
            return True
    return False


def find_match(entry: dict, existing: list[dict]) -> dict | None:
    """Find matching existing entry by name + city (fuzzy)."""
    for e in existing:
        if cities_match(entry["city"], e["city"]) and names_match(entry["name"], e["name"]):
            # Extra check: skip if first names clearly differ (like Devanshi vs Sneha)
            n1_parts = normalize_name(entry["name"]).split()
            n2_parts = normalize_name(e["name"]).split()
            if n1_parts and n2_parts and n1_parts[0][0] != n2_parts[0][0]:
                continue
            return e
    return None


def enrich_existing(existing: dict, new: dict) -> tuple[dict, list[str]]:
    """Enrich existing entry with data from Impulse where we have gaps. Returns (updated, changes)."""
    changes = []
    updated = dict(existing)

    # Fill in empty fields from Impulse data
    fill_fields = ["contact", "address", "fee_range"]
    for field in fill_fields:
        if not updated.get(field) and new.get(field):
            updated[field] = new[field]
            changes.append(f"  + {field}: {new[field]}")

    # Upgrade unknown fields
    upgrade_fields = ["teleconsult", "stimulant_comfort", "adult_adhd", "med_mgmt"]
    for field in upgrade_fields:
        if updated.get(field) == "unknown" and new.get(field) != "unknown":
            updated[field] = new[field]
            changes.append(f"  ~ {field}: unknown -> {new[field]}")

    return updated, changes


def main():
    apply = "--apply" in sys.argv

    print("Fetching from Impulse ADHD...")
    offline = fetch_professionals("Offline")
    online = fetch_professionals("Online")

    # Deduplicate by Impulse ID
    all_pros = {}
    for p in offline + online:
        all_pros[p["id"]] = p

    print(f"  Offline: {len(offline)}, Online: {len(online)}, Unique: {len(all_pros)}")

    # Load existing
    existing = json.loads(DOCTORS_JSON.read_text())
    existing_ids = {e["id"] for e in existing}
    print(f"  Existing entries: {len(existing)}")

    # Convert all Impulse data
    converted = [convert_professional(p) for p in all_pros.values()]

    # Separate into matches and new
    enriched_count = 0
    new_entries = []
    enrichment_log = []

    for entry in converted:
        match = find_match(entry, existing)
        if match:
            updated, changes = enrich_existing(match, entry)
            if changes:
                enriched_count += 1
                enrichment_log.append(f"  {match['name']} ({match['city']}):")
                enrichment_log.extend(changes)
                # Update in place
                idx = existing.index(match)
                existing[idx] = updated
        else:
            # Check slug collision
            if entry["id"] in existing_ids:
                entry["id"] = entry["id"] + "-impulse"
            new_entries.append(entry)
            existing_ids.add(entry["id"])

    # Sort all entries by city, then name
    final = existing + new_entries
    final.sort(key=lambda x: (x["city"].lower(), x["name"].lower()))

    print(f"\nResults:")
    print(f"  Enriched existing: {enriched_count}")
    print(f"  New entries: {len(new_entries)}")
    print(f"  Total after merge: {len(final)}")

    if enrichment_log:
        print(f"\nEnrichments:")
        for line in enrichment_log:
            print(line)

    if new_entries:
        print(f"\nNew professionals:")
        for e in sorted(new_entries, key=lambda x: (x["city"], x["name"])):
            print(f"  + {e['name']} - {e['city']}, {e['state']}")

    if apply:
        DOCTORS_JSON.write_text(json.dumps(final, indent=2, ensure_ascii=False) + "\n")
        print(f"\nWritten {len(final)} entries to {DOCTORS_JSON}")
    else:
        print(f"\nDry run. Use --apply to write changes.")


if __name__ == "__main__":
    main()
