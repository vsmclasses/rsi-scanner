import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

screener_url = "https://chartink.com/screener/vikasrsi"
process_url = "https://chartink.com/screener/process"

session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
}

# 1. Page load karke CSRF token aur exact scan_clause nikalna
response = session.get(screener_url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# CSRF Token
csrf_meta = soup.find('meta', {'name': 'csrf-token'})
csrf_token = csrf_meta['content'] if csrf_meta else ''

# Scan Clause extraction (Formula Text)
scan_clause = ""

# Method A: Input tag se scan_clause dhoondna
clause_input = soup.find('input', {'name': 'scan_clause'}) or soup.find('textarea', {'id': 'scan_clause'})
if clause_input:
    scan_clause = clause_input.get('value', '')

# Method B: Regex se JavaScript code ke andar se dhoondna
if not scan_clause:
    match = re.search(r'scan_clause["\']?\s*:\s*["\'](.*?)["\']', response.text)
    if match:
        scan_clause = match.group(1)

post_headers = {
    'User-Agent': headers['User-Agent'],
    'x-csrf-token': csrf_token,
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://chartink.com',
    'Referer': screener_url
}

# Payload mein scan_clause bhejenge
payload = {
    'scan_clause': scan_clause
}

# API Call
res = session.post(process_url, headers=post_headers, data=payload)

try:
    data = res.json()
except Exception as e:
    print("JSON decode error:", e)
    data = {}

# 2. Extract & Format Table
if 'data' in data and len(data['data']) > 0:
    df = pd.DataFrame(data['data'])

    # Close Price Column Identification
    close_col = None
    for k in ['close', '0', 'scan-column-default-close']:
        if k in df.columns:
            close_col = k
            break

    # Volume Column Identification
    vol_col = None
    for k in ['volume', '2', '3', 'scan-column-default-volume']:
        if k in df.columns:
            vol_col = k
            break

    # Format Close
    if close_col and close_col in df.columns:
        df['Close'] = df[close_col].apply(lambda x: f"{float(x):,.2f}" if pd.notnull(x) and str(x).replace('.','',1).isdigit() else "-")
    else:
        df['Close'] = "-"

    # Format Volume
    if vol_col and vol_col in df.columns:
        df['Volume'] = df[vol_col].apply(lambda x: f"{int(float(x)):,}" if pd.notnull(x) and str(x).replace('.','',1).isdigit() else "-")
    else:
        df['Volume'] = "-"

    # Symbol
    df['Symbol'] = df['nsecode'] if 'nsecode' in df.columns else ''

    # TradingView Link
    df['Chart'] = df['nsecode'].apply(
        lambda symbol: f'<a href="https://in.tradingview.com/chart/?symbol=NSE:{symbol}&interval=D" target="_blank" class="chart-btn">📈 Daily Chart</a>'
    )

    final_df = df[['Symbol', 'Close', 'Volume', 'Chart']].copy()
    html_table = final_df.to_html(index=False, escape=False, classes='custom-table')
else:
    html_table = "<p style='text-align:center; padding:20px; font-weight:bold;'>Abhi koi stock filter mein nahi aaya.</p>"

# 3. Generating Responsive HTML
full_html = f"""
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 8px;
            background-color: #ffffff;
        }}
        .table-container {{
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            border-radius: 8px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
        }}
        table.custom-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 18px;
            text-align: center;
            white-space: nowrap;
        }}
        table.custom-table th {{
            background-color: #2a3952;
            text-align: center;
            color: #ffffff;
            padding: 12px 10px;
            font-weight: 600;
        }}
        table.custom-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #e2e8f0;
            color: #0f172a;
            font-weight: 500;
        }}
        table.custom-table td:first-child {{
            font-weight: bold;
            color: #1e293b;
        }}
        table.custom-table tr:hover {{ background-color: #f8fafc; }}
        .chart-btn {{
            background-color: #2563eb;
            color: #ffffff !important;
            padding: 6px 12px;
            text-decoration: none;
            border-radius: 6px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
            transition: background-color 0.2s ease;
        }}
        .chart-btn:hover {{ background-color: #1d4ed8; }}
        @media screen and (max-width: 600px) {{
            table.custom-table {{ font-size: 16px; }}
            table.custom-table th, table.custom-table td {{ padding: 8px 8px; }}
            .chart-btn {{ padding: 5px 8px; font-size: 14px; }}
        }}
    </style>
</head>
<body>
    <div class="table-container">
        {html_table}
    </div>
</body>
</html>
"""

with open("rsi.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Scraper successfully extracted scan_clause and updated rsi.html!")
