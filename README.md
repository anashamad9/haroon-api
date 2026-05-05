# Haroon API

Live JSON files are generated from Google Sheets by GitHub Actions every 30 minutes.

## Public JSON Links

- `pending.json`  
  `https://raw.githubusercontent.com/anashamad9/haroon-api/main/pending.json`
- `approved.json`  
  `https://raw.githubusercontent.com/anashamad9/haroon-api/main/approved.json`
- `old_pending.json`  
  `https://raw.githubusercontent.com/anashamad9/haroon-api/main/old_pending.json`

## CDN Links (faster for frontend apps)

- `https://cdn.jsdelivr.net/gh/anashamad9/haroon-api@main/pending.json`
- `https://cdn.jsdelivr.net/gh/anashamad9/haroon-api@main/approved.json`
- `https://cdn.jsdelivr.net/gh/anashamad9/haroon-api@main/old_pending.json`

## Notes

- The Google Sheet must be shared as `Anyone with the link` (Viewer).
- If a tab `gid` is invalid, that tab is skipped and a warning appears in the workflow logs.
