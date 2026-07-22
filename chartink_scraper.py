import requests
from bs4 import BeautifulSoup
import pandas as pd

# Chartink Screener details
chartink_url = "https://chartink.com/screener/vikasrsi"
process_url = "url = "https://chartink.com/screener/process"

# Python Session bana rahe hain
session = requests.Session()

# Step 1: Page open karke CSRF Token nikalna
response = session.get(chartink_url)
soup = BeautifulSoup(response.text, 'html.parser')
csrf_token = soup.select_one('[name="csrf-token"]')['content']

# Step 2: Chartink ko 'Run Scan' ka request bhejna
headers = {
    'x-csrf-token': csrf_token,
    'referer': chartink_url
}

# Scan Condition Clause (Screener payload)
payload = {
    'scan_clause': '( {33619} ( latest rsi( 14 ) > 50 ) )'  # Chartink ka internal condition ID
}

res = session.post(process_url, headers=headers, data=payload)
data = res.json()

# Step 3: Data ko Pandas DataFrame mein convert karna
if 'data' in data and len(data['data']) > 0:
    df = pd.DataFrame(data['data'])
    
    # Manpasand Columns select aur rename karein
    df = df[['nsecode', 'name', 'close', 'per_chg', 'volume']]
    df.columns = ['Symbol', 'Stock Name', 'CMP', 'Chg %', 'Volume']
    
    # Step 4: HTML Table Code Generate karna
    html_table = df.to_html(index=False, classes='chartink-table')
else:
    html_table = "<p style='text-align:center;'>Abhi koi stock filter mein nahi aaya.</p>"

# Step 5: Beautiful Page Structure ke sath Save karna
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

print("Chartink result successfully updated to rsi.html!")
