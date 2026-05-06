import requests
import pandas as pd
import boto3
import io
from dotenv import load_dotenv
import os

# ---- CONFIG ----
load_dotenv()
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")
S3_BUCKET = "medicaid-poverty-analysis"
S3_PREFIX = "medicaid-project"

s3 = boto3.client("s3")

def upload_df_to_s3(df, filename):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=f"{S3_PREFIX}/{filename}",
        Body=csv_buffer.getvalue()
    )
    print(f"Uploaded {filename} to s3://{S3_BUCKET}/{S3_PREFIX}/{filename}")


# ---- CENSUS ACS ----
def fetch_census():
    years = [2018, 2019, 2021, 2022, 2023, 2024]
    all_data = []
    for year in years:
        url = f"https://api.census.gov/data/{year}/acs/acs5"
        params = {
            "get": "NAME,B17001_001E,B17001_002E,B27001_001E,B27001_005E",
            "for": "county:*",
            "key": CENSUS_API_KEY
        }
        r = requests.get(url, params=params)
        rows = r.json()
        header = rows[0]
        for row in rows[1:]:
            d = dict(zip(header, row))
            d["year"] = year
            all_data.append(d)
        print(f"Census {year}: {len(rows) - 1} counties")

    df = pd.DataFrame(all_data)
    df.columns = [c.lower() for c in df.columns]
    df = df.rename(columns={
        "b17001_001e": "total_pop",
        "b17001_002e": "poverty_pop",
        "b27001_001e": "total_pop_insurance",
        "b27001_005e": "uninsured_pop",
        "b19013_001e": "median household income"
    })
    df["poverty_rate"] = pd.to_numeric(df["poverty_pop"], errors="coerce") / \
                         pd.to_numeric(df["total_pop"], errors="coerce")
    df["uninsured_rate"] = pd.to_numeric(df["uninsured_pop"], errors="coerce") / \
                           pd.to_numeric(df["total_pop_insurance"], errors="coerce")
    return df


# ---- CMS Medicaid ----
def fetch_cms():
    base_url = "https://data.medicaid.gov/api/1/datastore/query/6165f45b-ca93-5bb5-9d06-db29c692a360/0"
    all_results = []
    limit = 1000
    offset = 0
    while True:
        r = requests.get(base_url, params={"limit": limit, "offset": offset})
        data = r.json()
        results = data.get("results", [])
        if not results:
            break
        all_results.extend(results)
        print(f"CMS fetched: {len(all_results)} rows")
        offset += limit
        if len(results) < limit:
            break

    df = pd.DataFrame(all_results)
    # filter out preliminary report, only keep the final
    df = df[df["final_report"] == "Y"]
    # get reporting_period
    df["year"] = df["reporting_period"].astype(str).str[:4].astype(int)
    # keep 2018-2024
    df = df[df["year"].between(2018, 2024)]
    return df


# ---- MAIN ----
if __name__ == "__main__":
    try:
        s3.create_bucket(Bucket=S3_BUCKET)
        print("Bucket created")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print("Bucket already exists, continuing...")

    print("Fetching Census ACS data...")
    census_df = fetch_census()
    upload_df_to_s3(census_df, "census_acs_2018_2024.csv")
    print(f"Census total rows: {len(census_df)}")

    print("\nFetching CMS Medicaid data...")
    cms_df = fetch_cms()
    upload_df_to_s3(cms_df, "cms_medicaid_2018_2024.csv")
    print(f"CMS total rows: {len(cms_df)}")

    print("\nDone! Both datasets uploaded to S3.")