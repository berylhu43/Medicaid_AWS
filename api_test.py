import requests
import pandas as pd

api_key = "244ffe049fa9755edceae8ef01457e0b4225309f"

years = [2018, 2019, 2021, 2022, 2023, 2024]  # 2020没有ACS 5-year
all_data = []

for year in years:
    url = f"https://api.census.gov/data/{year}/acs/acs5"
    params = {
        "get": "NAME,B17001_001E,B17001_002E,B27001_001E,B27001_005E",
        "for": "county:*",
        "key": api_key
    }
    r = requests.get(url, params=params)
    rows = r.json()
    header = rows[0]
    for row in rows[1:]:
        d = dict(zip(header, row))
        d["year"] = year
        all_data.append(d)
    print(f"{year}: {len(rows)-1} counties")

df = pd.DataFrame(all_data)
print(f"Total rows: {len(df)}")
print(df.head())

if __name__ == "__main__":
    import requests

    url = "https://data.medicaid.gov/api/1/datastore/query/6165f45b-ca93-5bb5-9d06-db29c692a360/0"
    params = {"limit": 100, "offset": 0}

    r = requests.get(url, params=params)
    print(r.status_code)
    print(r.json()[:2] if isinstance(r.json(), list) else r.json())
