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

# Step 1: Chartink page se CSRF token aur scan_run_token extract karna
response = session.get(screener_url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# CSRF Token
csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']

# Dynamic Token Extraction
scan_run_token_input = soup.find('input', {'name': 'scan_run_token'}) or soup.find('input', {'id': 'scan_run_token'})

if scan_run_token_input:
    token_value = scan_run_token_input.get('value', '')
else:
    # Hardcoded fallback token from screenshot
    token_value = "1a713774944d4be3554922f956afb90fcbdc336a8dcefecf6f7f83891f193e95"

post_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-csrf-token': csrf_token,
    'origin': 'https://chartink.com',
    'referer': screener_url
}

# Payload exact as shown in Network tab
payload = {
    'scan_run_token': token_value,
    'column_clause': ' Daily Close as \'scan-column-default-close\',  Daily "close - 1 candle ago close / 1 candle ago close * 100" as \'scan-column-default-percent-change\', filternumber( daily close >  1 day ago close,1) as \'default-percent-change-conditional-filters-color\',  Daily Volume as \'scan-column-default-volume\''
}

res = session.post(process_url, headers=post_headers, data=payload)
data = res.json()

# Step 2: HTML Table Generator
if 'data' in data and len(data['data']) > 0:
    df = pd.DataFrame(data['data'])
    
    df['sr'] = range(1, len(df) + 1)
    
    # Matching exact Chartink Columns
    df = df[['sr', 'name', 'nsecode', 'close', 'per_chg', 'volume']]
    df.columns = ['Sr.', 'Stock Name', 'Symbol', 'Close', '%_Change', 'Volume']
    
    # Formats
    df['%_Change'] = df['%_Change'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "0.00%")
    df['Volume'] = df['Volume'].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else "0")
    
    html_table = df.to_html(index=False, classes='chartink-table')
else:
    html_table = "<p style='text-align:center; padding:20px; font-weight:bold;'>Abhi koi stock filter mein nahi aaya.</p>"

# Final Output HTML
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

print("Scraper successfully updated with token!")
