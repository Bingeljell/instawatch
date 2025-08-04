# Insta‑Watch 📸 – Project Charter & Roadmap
*A zero‑budget, 100 % local Instagram watch‑list for competitive and trend monitoring.*

---

## 1  Product Idea

| Item | Description |
|------|-------------|
| **Problem** | Small e‑commerce teams need to stay on top of competitors’ and influencers’ latest Instagram posts without paying for expensive social‑listening SaaS tools or storing mountains of old content. |
| **Solution** | A lean desktop tool that: 1) fetches only the *N* most‑recent posts (e.g., 10) for a curated list of public Instagram handles, 2) refreshes every 24–48 h to remain polite, 3) stores data locally in SQLite, and 4) exposes the results both as an RSS feed and a simple Tailwind‑styled web page. |
| **Value Props** | • **Zero recurring cost** – runs entirely on your machine. <br>• **Tiny resource footprint** – self‑pruning DB keeps storage constant. <br>• **Open data** – RSS feed plugs into any reader or automation workflow. |
| **Target Users** | • Solo founders & small brands <br>• Growth / content marketers <br>• Indie hackers who prefer open‑source over SaaS |
| **MVP Scope** | Public profiles only • Up to *N* posts per account • Manual list of handles • Daily cron job • RSS feed • Local HTML dashboard |

---

## 2  Technology Stack

| Layer | Choice | Notes |
|-------|--------|-------|
| **Language** | Python 3.11 | Readily available; excellent libraries |
| **Scraping** | `instaloader` | Handles login, pagination, JSON export; supports “only new posts” mode |
| **Storage** | SQLite (`sqlite3` std‑lib) | Zero‑config, file‑based, ACID |
| **Feed Generation** | `feedgen` | Builds RSS/Atom feeds programmatically |
| **Scheduler** | `cron` (Linux/macOS) or **Task Scheduler** (Windows) | Native, no extra deps |
| **Local UI** | Two interchangeable options: <br>**A. Static** – `index.html` + Tailwind CDN + vanilla JS <br>**B. Server‑rendered** – Flask 3.x + Jinja + Tailwind CDN |
| **Dev‑Ops (opt.)** | Docker (`python:slim`) • GitHub Actions for CI • `pre‑commit` hooks |

---

## 3  Roadmap

| Phase | Goal | Key Deliverables | Est. Effort |
|-------|------|------------------|-------------|
| **0. Setup** | Project skeleton & env | `git init`, virtual env, `requirements.txt`, GitHub repo | ½ day |
| **1. Data Layer** | Fetch & store posts | `insta_watch.py` script, SQLite schema, pruning logic | 1 day |
| **2. Feed Layer** | Expose RSS | Integrate `feedgen`, write `insta_watch.xml` | ½ day |
| **3A. Static UI** | Browser view | `static/index.html`, Tailwind cards, JS RSS parser | ½ day |
| **3B. Flask UI** (optional) | Server‑rendered view | `app.py`, Jinja template, `/` route | 1 day |
| **4. Automation** | Hands‑free refresh | Cron / Task Scheduler entry, log rotation | ½ day |
| **5. Polish** | Docs & packaging | `Project.md`, inline docstrings, README gifs | ½ day |
| **6. Stretch** | Docker & CI | `Dockerfile`, GitHub Action lint/test workflow | 1 day |

> **Total MVP time** ≈ **4 – 5 part‑time days**

---

## 4  Detailed Milestones & Micro‑Actions

### Milestone 1 – Local Scraper
1. **Create watch list** – hard‑code `USERS = ["nike", "adidas"]`.
2. **Implement fetch loop** – call `Profile.get_posts()` and slice first *N* items.
3. **Insert or ignore** – use `INSERT OR IGNORE` to avoid duplicates.
4. **Prune** – delete rows beyond *N* per user.
5. **Smoke‑test** – verify DB row counts.

### Milestone 2 – Feed Generator
1. Instantiate `FeedGenerator()`.
2. Loop over `SELECT * FROM posts ORDER BY ts DESC`.
3. Map columns → RSS `<item>` fields.
4. Write `insta_watch.xml`.
5. Validate in a feed reader.

### Milestone 3 – UI Option A (Static)
1. Scaffold `static/index.html`.
2. Load Tailwind via `<script src="https://cdn.tailwindcss.com">`.
3. Fetch `/insta_watch.xml` with `fetch`.
4. Parse XML → DOM → render cards.
5. Serve with `python -m http.server`.

### Milestone 4 – UI Option B (Flask)
1. `pip install flask feedparser`.
2. Write `app.py` with `/` route, parse RSS using `feedparser`.
3. Add Jinja template (`templates/index.html`).
4. Run `flask run`, test.

### Milestone 5 – Automation & Logs
1. Add cron entry `30 2 * * * python insta_watch.py`.
2. Pipe output to `insta_watch.log`.
3. Add weekly `logrotate` rule (Linux) or manual clean‑up script (Win).

### Milestone 6 – Docs & Packaging
1. Finalise **Project.md** (this file).
2. Update `README.md` with quick‑start commands.
3. Create `LICENSE` (MIT).
4. Tag `v0.1.0` release on GitHub.

---

## 5  Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| IG blocks IP for scraping | Script fails | Low request volume, long refresh interval |
| HTML markup change | Parsing errors | Instaloader maintainer community usually patches quickly; pin version |
| Data loss | Lost history | Include `.db` in backup routine or git‑ignored `/backups` folder |
| Feature creep | Delays | Freeze MVP scope; log extras in `TODO.md` |

---

## 6  Success Metrics

* **Accuracy** – ≥ 95 % of scheduled runs complete without HTTP or DB errors.
* **Freshness** – New posts appear in RSS < 2 h after Instagram publish (given daily schedule).
* **Footprint** – DB size ≤ (Users × N × 5 kB).  
* **User happiness** – Personal feedback: “I open one feed and see all competitor posts.”

---

## 7  Next Steps After MVP

1. **Add TikTok** via Apify actor, merge into same DB/schema.
2. **Slack / email alerts** – push only when a new post hits.
3. **Trend stats** – compute rolling engagement deltas.
4. **Docker Hub image** – `docker run -d insta-watch`.
5. **Optional authentication** – private feed via Basic Auth or token.

---

> **“Build small, ship fast, iterate later.”**  
> — Your future self, sipping coffee while the cron job hums happily
