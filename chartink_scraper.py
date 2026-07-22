import requests
import pandas as pd

screener_url = "https://chartink.com/screener/vikasrsi"
process_url = "https://chartink.com/screener/process"

session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# 1. Fetch CSRF token
req = session.get(screener_url, headers=headers)
csrf_token = req.text.split('name="csrf-token" content="')[1].split('"')[0]

post_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-csrf-token': csrf_token,
    'origin': 'https://chartink.com',
    'referer': screener_url
}

# 2. Aapki conditions aur custom columns
payload = {
    'scan_clause': '( {cash} ( [0] 15 minute rsi > 60 ) )',
    'column_clause': " Daily Close as 'scan-column-default-close', Daily \"close - 1 candle ago close / 1 candle ago close * 100\" as 'scan-column-default-percent-change', filternumber( daily close > 1 day ago close,1) as 'default-percent-change-conditional-filters-color', Daily Volume as 'scan-column-default-volume'"
}

res = session.post(process_url, headers=post_headers, data=payload)
data = res.json()

# 3. Create table
if 'data' in data and len(data['data']) > 0:
    df = pd.DataFrame(data['data'])
    
    # Serial Number column
    df['sr'] = range(1, len(df) + 1)
    
    # Required Columns
    df = df[['sr', 'name', 'nsecode', 'close', 'per_chg', 'volume']]
    df.columns = ['Sr.', 'Stock Name', 'Symbol', 'Close', '%_Change', 'Volume']
    
    # Formatting numbers
    df['%_Change'] = df['%_Change'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "0.00%")
    df['Volume'] = df['Volume'].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else "0")
    
    html_table = df.to_html(index=False, classes='chartink-table')
else:
    html_table = "<p style='text-align:center; padding:20px; font-weight:bold;'>Abhi koi stock filter mein nahi aaya.</p>"

# 4. Generate HTML File
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 10px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; text-align: left; }}
        th {{ background-color: #f0f4f9; color: #333; padding: 10px; border-bottom: 2px solid #ccc; font-weight: 600; text-align: center; }}
        td {{ padding: 8px 10px; border-bottom: 1px solid #eee; text-align: center; }}
        tr:hover {{ background-color: #f8f9fa; }}
        td:nth-child(5) {{ color: #2e7d32; font-weight: bold; }}
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
