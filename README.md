# pulse-ndjson-45

**Every 45 minutes** this repo appends a single NDJSON line with:
- UTC timestamp & UNIX time
- Kyiv / New York localized timestamps
- ISO week, weekday, hour/minute, day-of-year
- short checksum & nonce

Output per day: `data/YYYY-MM-DD/events.ndjson`  
Stdlib-only (no external APIs). Powered by GitHub Actions cron (`*/45 * * * *`).
