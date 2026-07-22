import requests
import pandas as pd
from bs4 import BeautifulSoup

screener_url = "https://chartink.com/screener/vikasrsi"
process_url = "https://chartink.com/screener/process"

session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# 1. Fetch CSRF token & scan_run_token
response = session.get(screener_url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']

scan_run_token_input = soup.find('input', {'name': 'scan_run_token'}) or soup.find('input', {'id': 'scan_run_token'})
token_value = scan_run_token_input.get('value', '') if scan_run_token_input else "1a713774944d4be3554922f956afb90fcbdc336a8dcefecf6f7f83891f193e95"

post_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-csrf-token': csrf_token,
    'origin': 'https://chartink.com',
    'referer': screener_url
}

payload = {
    'scan_run_token': token_value,
    'column_clause': ' Daily Close as \'scan-column-default-close\',  Daily "close - 1 candle ago close / 1 candle ago close * 100" as \'scan-column-default-percent-change\', filternumber( daily close >  1 day ago close,1) as \'default-percent-change-conditional-filters-color\',  Daily Volume as \'scan-column-default-volume\''
}

res = session.post(process_url, headers=post_headers, data=payload)
data = res.json()

# 2. Dynamic Data Processing (Fixes KeyError)
if 'data' in data and len(data['data']) > 0:
    df = pd.DataFrame(data['data'])
    
    # Serial Number
    df.insert(0, 'Sr.', range(1, len(df) + 1))
    
    # Filter only useful columns safely
    keep_cols = [c for c in ['Sr.', 'name', 'nsecode', 'close', 'per_chg', 'volume', '0', '1', '2', '3'] if c in df.columns]
    
    if len(keep_cols) > 1:
        df = df[keep_cols]
    
    # Column Renaming
    rename_dict = {
        'name': 'Stock Name',
        'nsecode': 'Symbol',
        'close': 'Close',
        'per_chg': '% Change',
        'volume': 'Volume'
    }
    df = df.rename(columns=rename_dict)
    
    html_table = df.to_html(index=False, classes='chartink-table')
else:
    html_table = "<p style='text-align:center; padding:20px; font-weight:bold;'>Abhi koi stock filter mein nahi aaya.</p>"

# 3. HTML Layout Output
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
    </style>
</head>
<body>
    {html_table}
</body>
</html>
"""

with open("rsi.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Scraper successfully executed!")
