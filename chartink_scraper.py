import requests
from bs4 import BeautifulSoup
import pandas as pd

# Chartink Screener details
chartink_url = "https://chartink.com/screener/vikasrsi"
process_url = "https://chartink.com/screener/process"

session = requests.Session()

# Step 1: CSRF Token fetch karna
headers_initial = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
response = session.get(chartink_url, headers=headers_initial)
soup = BeautifulSoup(response.text, 'html.parser')
csrf_token = soup.select_one('[name="csrf-token"]')['content']

# Step 2: Exact Scan condition bhejkar result maangna
headers = {
    'x-csrf-token': csrf_token,
    'referer': chartink_url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Scan Condition (Agar aapne scanner ki conditions change ki hain toh scan_clause adjust kar sakte hain)
payload = {
    'scan_clause': '( {cash} ( [0] 15 minute rsi > 60 ) )'
}

res = session.post(process_url, headers=headers, data=payload)
data = res.json()

# Step 3: Result Process karna
if 'data' in data and len(data['data']) > 0:
    df = pd.DataFrame(data['data'])
    
    # Required columns format karna
    df = df[['nsecode', 'name', 'close', 'per_chg', 'volume']]
    df.columns = ['Symbol', 'Stock Name', 'CMP', 'Chg %', 'Volume']
    
    html_table = df.to_html(index=False, classes='chartink-table')
else:
    html_table = "<p style='text-align:center; padding:20px;'>Abhi koi stock filter mein nahi aaya.</p>"

# Step 4: HTML output file generate karna
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 10px; background: #fff; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 10px; }}
        th {{ background-color: #1a2530; color: #fff; padding: 10px; text-align: center; }}
        td {{ padding: 8px; border-bottom: 1px solid #ddd; text-align: center; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    {html_table}
</body>
</html>
"""

with open("rsi.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Scraper successfully updated rsi.html!")
