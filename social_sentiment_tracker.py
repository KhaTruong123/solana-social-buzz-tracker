#!/usr/bin/env python
"""
Pull top Solana tokens by mindshare Δ% from Messari Signal API,
optionally enrich with sentiment or usage data
"""

import os, time, requests, json
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

API_KEY = os.getenv("MESSARI_KEY")          # <-- put your key in .env
if not API_KEY:
        raise SystemExit("Please  export MESSARI_KEY=...  and try again.")

HEAD = {"x-messari-api-key": API_KEY}
SIG  = "https://api.messari.io/signal/v0/assets"
DET  = "https://api.messari.io/metrics/v2/assets/details"

THRESHOLD  = 50             # mind-share Δ% filter
TARGET_LEN = 50             # how many Solana tokens to collect
RATE_SLEEP = 0.5            
PAGE = 3                    # number of pages to scrape
LIMIT = 2000                # number of results per page


# Steps
# 1. Download candidates
# 2. Filter by threshold
# 3. Confirm chain
# 4. Collect
# E. Store

# --- Step 1: one page of mind-share movers ---------------------------------
candidates = []

for page in range(1, PAGE):
    resp = requests.get(SIG, headers=HEAD, params={"limit": LIMIT, "page": page}, timeout=30)
    resp.raise_for_status()
    data = resp.json()["data"]
    candidates.extend(data)  # Append results from each page
    time.sleep(RATE_SLEEP)  # Respect rate limits

solana_hits = []

# --- Step 2: Filter by threshold----------------------
for asset in candidates:
    if asset["mindshare"]["percentageChange1d"] is None or asset["mindshare"]["percentageChange1d"] < THRESHOLD:
        continue

# --- Step 3: Check Asset Details for each candidate ----------------------
    aid = asset["id"]
    det = requests.get(DET, headers=HEAD, params={"ids": aid}, timeout=20).json()["data"]

    # Ensure det is a list and iterate over its elements
    slug_ok = any("solana" in item.get("networkSlugs", []) for item in det)
    if not slug_ok:
        continue  # Skip this asset if slug_ok is False
    ca_ok = any(
        c["networkName"] == "Solana"
        for item in det
        for c in item.get("contractAddresses", [])
    )
    if slug_ok or ca_ok:
        solana_hits.append({
            "id": aid,
            "symbol": asset["symbol"],
            "name": asset["name"],
            "slug": det[0]["slug"],
            "category": det[0]["category"],
            "sector": det[0]["sector"],
            "tags": det[0]["tags"],
            "links": det[0]["links"],
            "percentageChange1d": asset["mindshare"]["percentageChange1d"]
        })

    if len(solana_hits) == TARGET_LEN:
        break
    time.sleep(RATE_SLEEP)

# --- Save result -----------------------------------------------------------
out_file = "top_solana_mindshare.json"
# Sort solana_hits by percentageChange1d in descending order
sorted_hits = sorted(solana_hits, key=lambda x: x["percentageChange1d"], reverse=True)
with open(out_file, "w") as f:
    json.dump(sorted_hits, f, indent=2)

print(f"Saved {len(solana_hits)} tokens → {out_file}")
