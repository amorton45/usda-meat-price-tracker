# scraper.py  – downloads today's chicken, pork, and beef prices
import datetime as dt, os, pathlib, requests, pandas as pd

API_KEY = os.getenv("USDA_API_KEY")          # read from GitHub secret
TODAY = dt.date.today().strftime("%m/%d/%Y")

FEEDS = {
    "chicken": f"https://marsapi.ams.usda.gov/services/v1.2/reports/PY_BROILER_MARKET"
               f"?filter=report_date={TODAY}",
    "pork":    f"https://mpr.datamart.ams.usda.gov/services/v1.1/reports/LM_PK602/Summary"
               f"?q=report_date={TODAY}",
    "beef":    f"https://mpr.datamart.ams.usda.gov/services/v1.1/reports/LM_CT100/Summary"
               f"?q=report_date={TODAY}"
}

pathlib.Path("data").mkdir(exist_ok=True)

for name, url in FEEDS.items():
    r = requests.get(url, auth=(API_KEY, "")); r.raise_for_status()
    df = pandas.json_normalize(r.json()["results"])
    fname = f"data/{name}_{dt.date.today()}.csv"
    df.to_csv(fname, index=False)
    print(f"✓ wrote {fname}  ({len(df)} rows)")
