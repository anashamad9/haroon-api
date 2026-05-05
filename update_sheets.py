import os
from urllib.error import HTTPError, URLError

import pandas as pd

# Override via env in GitHub Actions if needed.
SHEET_ID = os.environ.get("GOOGLE_SHEET_ID", "1T-wU4Nr-lilL5wOP5P2j-xEK3INp6BcNd05ae7qlC8g")

# The 3 tabs and their GIDs.
TABS = {
    "pending": "0",
    "approved": "763618369",
    "old_pending": "1085594627",
}


def load_tab_dataframe(sheet_id: str, gid: str) -> pd.DataFrame:
    """Try multiple public CSV endpoints because Google can reject one format."""
    urls = [
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}",
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&gid={gid}",
    ]

    errors: list[str] = []
    for url in urls:
        try:
            return pd.read_csv(url)
        except HTTPError as exc:
            errors.append(f"{url} -> HTTP {exc.code}")
        except URLError as exc:
            errors.append(f"{url} -> URL error: {exc.reason}")
        except Exception as exc:  # pandas parser and runtime issues
            errors.append(f"{url} -> {type(exc).__name__}: {exc}")

    raise RuntimeError(
        "Unable to read tab. Check that the sheet is public ('Anyone with the link') "
        f"and that gid={gid} exists. Attempts: {' | '.join(errors)}"
    )


success_count = 0
failures: list[str] = []

for name, gid in TABS.items():
    try:
        df = load_tab_dataframe(SHEET_ID, gid)
        df.to_json(f"{name}.json", orient="records")
        success_count += 1
        print(f"Updated {name}.json ({len(df)} rows)")
    except Exception as exc:
        failures.append(f"{name} (gid={gid}): {exc}")
        print(f"::warning title=Skipped tab::{name} (gid={gid}) - {exc}")

if success_count == 0:
    raise SystemExit("No tabs were exported successfully. " + " || ".join(failures))

if failures:
    print("Completed with warnings: " + " || ".join(failures))
