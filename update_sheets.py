import os
from urllib.error import HTTPError, URLError

import pandas as pd

SHEET_ID = os.environ.get("GOOGLE_SHEET_ID", "1T-wU4Nr-lilL5wOP5P2j-xEK3INp6BcNd05ae7qlC8g")

TABS = {
    "pending": "0",
    "approved": "763618369",
    "old_pending": "1085594627",
}


def read_sheet_csv(sheet_id: str, gid: str) -> pd.DataFrame:
    urls = [
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}",
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&gid={gid}",
    ]
    last_error = None
    for url in urls:
        try:
            return pd.read_csv(url)
        except (HTTPError, URLError, ValueError) as err:
            last_error = err
            continue
    raise RuntimeError(f"failed to fetch gid={gid}: {last_error}")


updated = 0
for name, gid in TABS.items():
    try:
        df = read_sheet_csv(SHEET_ID, gid)
        df.to_json(f"{name}.json", orient="records")
        updated += 1
        print(f"updated {name}.json")
    except Exception as err:
        # Keep endpoint alive even if one tab fails to parse/fetch.
        with open(f"{name}.json", "w", encoding="utf-8") as f:
            f.write("[]")
        print(f"::warning title=Tab skipped::{name} (gid={gid}) -> {err}")

if updated == 0:
    print("::warning title=All tabs failed::Wrote empty JSON files to avoid 404 endpoints.")
