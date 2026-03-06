# PRD — ADHD Treatment Directory (India)

_A crowdsourced, ADHD-specific directory of psychiatrists, clinics, and hospitals in India — covering both child and adult ADHD — optimized for making treatment discoverable and reducing the "doctor-hunting" loop._

---

## 1) Background & Problem

People with ADHD in India — and their caregivers — often struggle to find psychiatrists or clinics that:

- Take adult ADHD seriously and diagnose it properly.
- Handle child/adolescent ADHD with structured assessments.
- Offer medication management where appropriate.
- Provide clear logistics (fees, wait time, booking, telehealth).

General mental-health directories exist but lack ADHD-specific fields and community trust signals. The result is repeated "call → get dismissed → try again" cycles. This is uniquely punishing for ADHD.

---

## 2) Goals & Non-Goals

### Goals

- Provide a **public, searchable directory** of ADHD-aware providers: psychiatrists, clinics, and hospital departments.
- Cover both **child and adult ADHD** from launch.
- Capture **ADHD-specific decision-making fields** (adult/child diagnosis, assessment approach, medication management, telehealth, costs, wait times).
- Use a **low-maintenance architecture**: static site + public GitHub repo as source of truth.
- Enable safe crowdsourcing via structured submissions, moderation, and transparent version history.

### Non-Goals (initially)

- Not a booking platform.
- Not medical advice or treatment recommendations.
- Not an emergency/crisis resource (provide disclaimer + links to iCall, Vandrevala).
- Not a ratings or reviews platform — no freeform text reviews.
- Not a general mental health directory.

---

## 3) Target Users & Personas

1. **Adult seeking diagnosis**
   Needs: adult ADHD experience, assessment details, medication management, cost, teleconsult.
2. **Parent/caregiver (child)**
   Needs: child/adolescent specialization, assessment process, school support guidance, clinic facilities.
3. **Already diagnosed (adult or child)**
   Needs: medication management, follow-ups, telehealth continuity.
4. **Contributors** (patients, caregivers, clinicians)
   Needs: easy structured submission, privacy, confidence that submissions are acted on.

---

## 4) User Stories

- As a user, I can filter by **city/state** and **teleconsult** to find accessible options immediately.
- As a user, I can filter by **adult ADHD** or **child ADHD** to avoid wasting time on wrong providers.
- As a user, I can filter by **medication management** to find providers who handle ongoing care.
- As a user, I can see **last verified date** and **verification tier** so I can judge listing freshness.
- As a contributor, I can submit a listing in under 2 minutes using a structured form.
- As a maintainer, I can review, request clarification, and approve/merge submissions via GitHub Issues.

---

## 5) Key Product Principles

- **Low friction**: fast filtering, mobile-first, minimal clicks to a useful shortlist.
- **Trust over volume**: 60 high-quality listings beat 600 vague ones.
- **Transparency**: all edits are in git history; verification tier and date are visible per listing.
- **Safety**: no freeform reviews, no defamatory claims, structured factual fields only.
- **Resilience**: community-owned, not tied to one person's account or infrastructure.

---

## 6) Data Model

### Provider Types

- `psychiatrist` (individual, private practice)
- `clinic` (multi-provider, ADHD-focused or mental health)
- `hospital_dept` (psychiatry department within a hospital)

### Core Fields (all provider types)

| Field                | Type   | Notes                                              |
| -------------------- | ------ | -------------------------------------------------- |
| `id`                 | slug   | e.g., `dr-priya-shah-ahmedabad`                    |
| `name`               | string | Full name or clinic/hospital name                  |
| `type`               | enum   | psychiatrist / clinic / hospital_dept              |
| `city`               | string |                                                    |
| `state`              | string |                                                    |
| `address`            | string | Optional; public address only                      |
| `website`            | url    | Optional                                           |
| `contact`            | string | Public phone or email only                         |
| `booking_link`       | url    | Optional                                           |
| `languages`          | array  | e.g., ["English", "Hindi", "Gujarati"]             |
| `teleconsult`        | enum   | yes / no / unknown                                 |
| `fee_range`          | string | e.g., "₹800–₹1500" (optional)                      |
| `wait_time_estimate` | string | e.g., "2–4 weeks" (optional)                       |
| `last_verified`      | date   | ISO date                                           |
| `verification_tier`  | enum   | unverified / reviewed / community-verified / stale |
| `source`             | string | contributor / public-profile / clinic-website      |

### ADHD-Specific Fields

| Field               | Type  | Notes                                                                    |
| ------------------- | ----- | ------------------------------------------------------------------------ |
| `adult_adhd`        | enum  | yes / no / unknown                                                       |
| `child_adhd`        | enum  | yes / no / unknown                                                       |
| `adolescent_adhd`   | enum  | yes / no / unknown                                                       |
| `assessment_style`  | enum  | structured / semi-structured / informal / unknown                        |
| `med_mgmt`          | enum  | yes / no / unknown                                                       |
| `stimulant_comfort` | enum  | yes / no / unknown                                                       |
| `comorbidities`     | array | tags: anxiety / depression / asd / ocd / ld / other                      |
| `tags`              | array | adhd-aware / lgbtq-friendly / non-judgmental / cashless / school-support |
| `flags`             | array | stale / unreachable / moved / needs-review                               |

### Notes on `stimulant_comfort`

- Default for all entries: `unknown`.
- Only set to `yes` or `no` when explicitly confirmed by a contributor (e.g., "confirmed they prescribe methylphenidate").
- Not a top-level filter in the UI — surfaced under "Advanced Filters."
- Rationale: preserves clinical credibility of the directory and avoids the "find me a pill doctor" perception, while still being the most important signal for many adults.

### Verification Tiers

| Tier                 | Meaning                                               |
| -------------------- | ----------------------------------------------------- |
| `unverified`         | Submitted, not yet reviewed                           |
| `reviewed`           | Checked for completeness; links/location validated    |
| `community-verified` | 2+ independent confirmations or recent patient report |
| `stale`              | Last verified > 12 months, or 2+ unreachable flags    |

---

## 7) MVP Feature Scope (V1)

### Public Site Pages

**Home**

- What this is, what it isn't.
- Disclaimer (not medical advice; not emergency help; verify before booking).
- CTA: "Find a provider" + "Submit a listing."

**Directory Page**

- Search: name, city, keyword.
- Filters (top-level):
  - City / State
  - Teleconsult
  - Adult ADHD
  - Child ADHD
  - Medication management
  - Language
  - Last verified within (3 / 6 / 12 months)
- Advanced filters (collapsed by default):
  - Stimulant comfort
  - Assessment style
  - Comorbidity experience
  - Provider type
- Sort: Recently verified / A–Z / City

**Listing Detail View**

- All fields, clearly labeled.
- Verification tier badge + last verified date.
- "Report stale / incorrect info" button (opens prefilled GitHub Issue).
- Disclaimer per listing.

**Submit a Listing Page**

- Structured form; on submit, generates a prefilled GitHub Issue link.
- Field-level guidance (tooltips or helper text).
- Estimated time: < 2 minutes.

**About / FAQ Page**

- Why this exists, how verification works, how to contribute.
- Crisis resources: iCall (9152987821), Vandrevala Foundation (1860-2662-345).

---

## 8) Submission & Moderation Pipeline

### Submission Flow

1. User fills form on site.
2. On submit: site opens a **prefilled GitHub Issue** (no API token, no backend, no security risk).
3. Issue is created in the public repo with structured data.

### Issue Templates (3)

- **New listing**: all fields, structured, required fields marked.
- **Update listing**: reference existing ID, changed fields only.
- **Report stale / incorrect**: listing ID + what is wrong + optional correction.

### Moderation Steps

1. Review submitted Issue for completeness and safety.
2. If OK → convert to PR, merge into `data/doctors.json`.
3. If incomplete → comment asking for missing fields.
4. If invalid / spam → close with brief explanation.
5. Target: < 72 hours for initial triage.

---

## 9) Technical Architecture

### Repo Structure

/
├── data/
│ └── doctors.json # Source of truth
├── site/ # Static site source
│ ├── index.html
│ ├── directory.html
│ ├── submit.html
│ ├── about.html
│ └── js/
│ ├── filters.js
│ └── submit.js # Builds prefilled GitHub Issue URL
├── .github/
│ └── ISSUE_TEMPLATE/
│ ├── new-listing.md
│ ├── update-listing.md
│ └── report-issue.md
├── CONTRIBUTING.md
├── README.md
└── LICENSE # CC0 or ODC-ODbL recommended

### Frontend

- Static HTML + vanilla JS (or Astro if you want component structure — both work fine with Claude Code).
- Client-side filtering on `doctors.json` (no backend, no CORS).
- Mobile-first, accessible.

### Hosting

- **GitHub Pages** (auto-deploys on push to `main`).
- No Vercel, no server, no database, no API keys.

### Infra Minimization Checklist

- [ ] No database service
- [ ] No server / backend
- [ ] No auth
- [ ] No stored API tokens
- [ ] No analytics (or use privacy-first, cookie-free, optional)
- [ ] No paid tier dependencies

### Optional CI (low effort)

- JSON schema validation on PR (GitHub Action, ~10 lines of YAML) — prevents malformed data from merging.

---

## 10) Legal, Safety & Moderation Rules

### What is allowed

- Publicly available professional information (clinic name, public address, website, public phone).
- Factual, structured fields only (yes/no/unknown, tags, ranges).
- Contributor-verified ADHD-specific fields with explicit source notes.

### What is not allowed

- Allegations of malpractice or negligence.
- Personal insults or subjective characterizations.
- Any patient information (yours or others').
- Speculation presented as fact.

### Takedown Process

- If a clinician or institution requests removal/correction: handle within 7 days.
- Provide a dedicated contact email in the README and About page.

### License

Recommend **CC0 (public domain)** or **ODC Open Database License** — makes the data maximally reusable and signals community intent.

---

## 11) Success Metrics

### MVP (First 30 Days)

- 50–150 listings across at least 10 cities.
- ≥ 30% of listings community-verified or reviewed.
- ≥ 20 community-submitted listings.
- All top 6 metros covered: Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Ahmedabad.

### Ongoing

- % stale listings < 20%.
- Median submission-to-merge time < 72 hours.
- Monthly "report stale" Issues filed (signals active use).

---

## 12) Risks & Mitigations

| Risk               | Mitigation                                                          |
| ------------------ | ------------------------------------------------------------------- |
| Stale listings     | `last_verified` field, stale flag, "report update" CTA per listing  |
| Low submissions    | Seeding + targeted community outreach + low-friction form           |
| Spam/abuse         | Issue moderation + structured templates (free text minimized)       |
| Defamation         | No freeform reviews; structured factual fields only                 |
| Maintainer burnout | Recruit co-maintainers early; document everything; keep scope small |
| Clinician backlash | Takedown process; respectful framing; no rankings or scores         |

---

## 13) Open Questions (Resolved)

| Question                   | Decision                                         |
| -------------------------- | ------------------------------------------------ |
| Scope: psychiatrists only? | No — include clinics and hospital departments    |
| Age scope?                 | Both adult and child/adolescent ADHD             |
| Stimulant comfort field?   | Yes, but `unknown` default, advanced filter only |
| Freeform reviews?          | No — structured fields only                      |

---

# Go-To-Market & Growth Strategy

## Phase 0 — Pre-Launch (Days 1–3)

**Objective**: Seed minimum viable data and get the site live.

Seed data tasks:

- Mine public clinic/hospital websites for psychiatrists who mention ADHD.
- Use existing general mental health lists as lead lists; validate ADHD-specific fields manually.
- Ask 10–15 people in your personal network who've been diagnosed to submit one doctor each.
- Target: **40–60 seed entries** before announcing.

Deliverables:

- Repo live and public.
- Site deployed on GitHub Pages.
- Issue templates working.
- README + About + CONTRIBUTING.md complete.

---

## Phase 1 — Community Seeding (Weeks 1–2)

**Objective**: Reach useful coverage in top 6 metros.

Channels:

- **r/ADHD_India** and **r/india** (mental health threads): one well-crafted post, not promotional — lead with the problem ("I spent months finding a doctor; here's what I built").
- **X/Twitter**: thread on adult ADHD diagnosis in India → mention the directory naturally.
- **Telegram/WhatsApp** ADHD/mental health groups (ask admins first).
- **LinkedIn**: short post aimed at mental health professionals — invite clinicians to self-submit.

Ask framing:

> "If you found a good doctor — or you ARE one — add them. Takes 2 minutes. Pay it forward."

---

## Phase 2 — Launch & Discoverability (Weeks 3–6)

**Objective**: Make the directory findable organically.

SEO foundations:

- City-specific URLs: `/india/maharashtra/mumbai`, `/india/gujarat/ahmedabad`.
- Page titles like "ADHD psychiatrists in Mumbai, India — verified directory."
- A neutral informational guide: "How to get an ADHD diagnosis in India (adult)" — this will rank and drive qualified traffic.

Content hooks (shareable):

- "What to ask your psychiatrist in your first ADHD appointment" (checklist, sharable image).
- "Which cities in India have the most ADHD-aware psychiatrists?" (data from your own directory — instant authority).

Shareable links:

- Deep links with pre-applied filters: `?city=Bengaluru&adult=true&tele=true` — easy to share in community threads.

---

## Phase 3 — Flywheel (Month 2–3+)

**Objective**: Make contributions self-sustaining.

Mechanisms:

- Recruit **regional maintainers** (one per metro initially) — reduces your triage burden.
- Quarterly **re-verification drives**: post in communities asking users to confirm top listings are still accurate.
- "**Contribute 1, benefit from all**" messaging — ADHD communities respond well to reciprocal framing.

Optional partnerships (amplification only, no medical endorsement):

- ADHD coaches and psychologists (they regularly need to refer for medication).
- College counseling centers (late-diagnosed adults are a major underserved group).
- Mental health journalists / newsletter writers in India.

---

## Phase 4 — Long-Term Resilience (Month 4+)

**Objective**: Ensure the directory survives independent of you.

Actions:

- Add 2–3 co-maintainers with repo admin access.
- Document `MAINTAINER.md`: how to review, merge, handle takedowns, do re-verification drives.
- Encourage forks and mirrors (CC0 license makes this frictionless).
- If traffic justifies it: explore a simple **OpenCollective** for hosting costs (currently zero, but good to have a plan).

---

## MVP Build Checklist

- [ ] Create public GitHub repo with `data/doctors.json` and schema.
- [ ] Write `CONTRIBUTING.md`, `README.md`, issue templates (3).
- [ ] Build static site with Claude Code:
  - [ ] Home + disclaimer
  - [ ] Directory with search + filters (top-level + advanced)
  - [ ] Listing detail view
  - [ ] Submit form (prefilled Issue link)
  - [ ] Report stale/update per listing
  - [ ] About / FAQ + crisis resources
- [ ] Seed 40–60 entries.
- [ ] Deploy on GitHub Pages.
- [ ] Write and schedule launch post for r/ADHD_India.
