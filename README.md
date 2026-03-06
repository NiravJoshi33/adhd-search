# ADHD Treatment Directory - India

A crowdsourced, ADHD-specific directory of psychiatrists, clinics, and hospitals in India — covering both child and adult ADHD.

**[View the directory](https://your-site-url)** | **[Submit a listing](https://your-site-url/submit)** | **[Report an issue](../../issues/new?template=report-issue.md)**

## What This Is

- A **public, searchable directory** of ADHD-aware providers in India
- Covers both **adult and child ADHD**
- **ADHD-specific fields**: assessment style, medication management, stimulant comfort, comorbidity experience
- **Community-verified** with transparent version history
- **No backend, no database** — static site + JSON data

## What This Is Not

- Not a booking platform
- Not medical advice or treatment recommendations
- Not a ratings or reviews site
- Not an emergency/crisis resource

> **Crisis Resources:** iCall (9152987821) | Vandrevala Foundation (1860-2662-345)

## Tech Stack

- **Astro** — static site generator
- **Data** — `data/doctors.json` (source of truth)
- **Hosting** — GitHub Pages
- **Submissions** — GitHub Issues (no backend needed)

## Development

```bash
npm install
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
```

## Project Structure

```
├── data/
│   └── doctors.json          # Source of truth
├── src/
│   ├── layouts/
│   │   └── BaseLayout.astro  # Shared layout
│   ├── components/
│   │   ├── ProviderCard.astro
│   │   └── VerificationBadge.astro
│   ├── pages/
│   │   ├── index.astro       # Home
│   │   ├── directory.astro   # Search + filters
│   │   ├── submit.astro      # Submission form
│   │   ├── about.astro       # FAQ + crisis resources
│   │   └── provider/
│   │       └── [id].astro    # Listing detail
│   ├── scripts/
│   │   ├── filters.ts        # Client-side filtering
│   │   └── submit.ts         # GitHub Issue URL builder
│   └── styles/
│       └── global.css
├── .github/
│   └── ISSUE_TEMPLATE/
│       ├── new-listing.md
│       ├── update-listing.md
│       └── report-issue.md
├── CONTRIBUTING.md
└── LICENSE                   # CC0
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting listings, reporting issues, and helping maintain the directory.

## Data Sources

This directory is built from multiple community sources:

- **[r/adhdindia wiki](https://www.reddit.com/r/adhdindia/wiki/doctors/)** — initial seed data
- **[Impulse ADHD](https://impulseadhd.github.io)** — community-maintained database by the r/adhdindia mod team

To sync the latest data from Impulse ADHD, run:

```bash
python scripts/sync_impulse.py          # Dry run — preview changes
python scripts/sync_impulse.py --apply  # Write to doctors.json
```

## License

Data: [CC0 1.0 (Public Domain)](LICENSE)
