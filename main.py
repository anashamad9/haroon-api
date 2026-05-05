import pandas as pd
import json

# Your Sheet ID
SHEET_ID = "1T-wU4Nr-lilL5wOP5P2j-xEK3INp6BcNd05ae7qlC8g"

# The 3 Tabs and their GIDs (based on your sheet)
TABS = {
    "pending": "0",
    "approved": "763618369",
    "old_pending": "1441773010" # Example GID - update if different
}

for name, gid in TABS.items():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    
    # Convert to JSON
    result = df.to_json(orient="records")
    
    # Save file
    with open(f"{name}.json", "w") as f:
        f.write(result)