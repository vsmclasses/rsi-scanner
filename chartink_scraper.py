import requests
import pandas as pd
from bs4 import BeautifulSoup

screener_url = "https://chartink.com/screener/vikasrsi"
process_url = "https://chartink.com/screener/process"

session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'application/json, text/javascript, */*; q=0.01'
}

# 1. Fetch live page to get real-time CSRF & scan_run_token
req = session.get(screener_url, headers=headers)
soup = BeautifulSoup(req.text, 'html.parser')

csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']

token_input = soup.find('input', {'name': 'scan_run_token'}) or soup.find('input', {'id': 'scan_run_token'})
token_val = token_input.get('value', '') if token_input else ''

post_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'x-csrf-token': csrf_token,
    'origin': 'https://chartink.com',
    'referer': screener_url
}

# Live request payload
payload = {}
if token_val:
    payload['scan_run_token'] = token_val

res = session.post(process_url, headers=post_headers, data=payload)
data = res.json()

# 2. Extract Data & Column Mapping
if 'data' in data and len(data['data']) > 0:
    df = pd.DataFrame(data['data'])

    # Smart column mapping for Close price
    close_col = None
    for k in ['close', '0', 'close_price', 'scan-column-default-close']:
        if k in df.columns:
            close_col = k
            break
            
    if not close_col and len(df.columns) > 0:
        for c in df.columns:
            if c not in ['name', 'nsecode', 'per_chg', 'volume', 'sr']:
                close_col = c
                break

    # Smart column mapping for Volume
    vol_col = None
    for k in ['volume', '2', '3', 'scan-column-default-volume']:
        if k in df.columns:
            vol_col = k
            break

    # Formatting Close
    if close_col and close_col in df.columns:
        df['Close'] = df[close_col].apply(lambda x: f"{float(x):,.2f}" if pd.notnull(x) and str(x).replace('.','',1).isdigit() else "-")
    else:
        df['Close'] = "-"

    # Formatting Volume
    if vol_col and vol_col in df.columns:
        df['Volume'] = df[vol_col].apply(lambda x: f"{int(float(x)):,}" if pd.notnull(x) and str(x).replace('.','',1).isdigit() else "-")
    else:
        df['Volume'] = "-"

    # Symbol
    df['Symbol'] = df['nsecode'] if 'nsecode' in df.columns else ''

    # TradingView Daily Chart Link Button
    df['Chart'] = df['nsecode'].apply(
        lambda symbol: f'<a href="https://in.tradingview.com/chart/?symbol=NSE:{symbol}&interval=D" target="_blank" class="chart-btn">📈 Daily Chart</a>'
    )

    final_df = df[['Symbol', 'Close', 'Volume', 'Chart']].copy()
    html_table = final_df.to_html(index=False, escape=False, classes='custom-table')
else:
    html_table = "<p style='text-align:center; padding:20px; font-weight:bold;'>No stock has appeared in the filter yet.</p>"

# 3. HTML Generation with Mobile Optimization
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

print("Scraper successfully updated with dynamic live scan session!")
