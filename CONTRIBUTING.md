# Contributing to ADHD Directory India

Thank you for helping make ADHD treatment more discoverable in India.

## Ways to Contribute

### 1. Submit a New Listing

Use the [submission form](https://your-site-url/submit) on the website. It takes under 2 minutes and generates a GitHub Issue automatically.

Alternatively, open a [New Listing issue](../../issues/new?template=new-listing.md) directly.

### 2. Report Stale or Incorrect Info

Click the "Report issue" button on any listing page, or open a [Report issue](../../issues/new?template=report-issue.md) directly.

### 3. Update an Existing Listing

Open an [Update Listing issue](../../issues/new?template=update-listing.md) with the listing ID and the fields that need changing.

### 4. Help Maintain

We welcome co-maintainers. If you'd like to help review submissions and merge PRs:

1. Fork the repo
2. Review open Issues labeled `new-listing`
3. If a submission looks valid, add it to `data/doctors.json` and submit a PR
4. Reach out via Issues if you'd like collaborator access

## Guidelines

### What to Include

- Publicly available professional information only
- Factual, structured data (yes/no/unknown fields, ranges, tags)
- Information you can verify or have personal experience with

### What NOT to Include

- Private contact details (personal mobile, home address)
- Patient information (yours or anyone else's)
- Subjective opinions, ratings, or freeform reviews
- Allegations of malpractice or negligence
- Speculation presented as fact

## Data Format

All listings live in `data/doctors.json`. Each entry follows this schema:

```json
{
  "id": "dr-name-city",
  "name": "Dr. Name",
  "type": "psychiatrist",
  "city": "City",
  "state": "State",
  "address": "",
  "website": "",
  "contact": "",
  "booking_link": "",
  "languages": ["English", "Hindi"],
  "teleconsult": "yes",
  "fee_range": "",
  "wait_time_estimate": "",
  "last_verified": "2026-01-01",
  "verification_tier": "unverified",
  "source": "contributor",
  "adult_adhd": "unknown",
  "child_adhd": "unknown",
  "adolescent_adhd": "unknown",
  "assessment_style": "unknown",
  "med_mgmt": "unknown",
  "stimulant_comfort": "unknown",
  "comorbidities": [],
  "tags": [],
  "flags": []
}
```

## Verification Tiers

| Tier | Meaning |
|------|---------|
| `unverified` | Submitted, not yet reviewed |
| `reviewed` | Checked for completeness; links/location validated |
| `community-verified` | 2+ independent confirmations or recent patient report |
| `stale` | Last verified > 12 months, or 2+ unreachable flags |

## Takedown Requests

If a clinician or institution requests removal or correction, we handle it within 7 days. Open an Issue or contact us directly.

## Code of Conduct

Be respectful. This directory serves a vulnerable community. Keep contributions factual, helpful, and safe.
