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

# 1. Fetch CSRF token and scan_run_token
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

# 2. Dynamic Table Formatting (Without Stock Name)
if 'data' in data and len(data['data']) > 0:
    df = pd.DataFrame(data['data'])
    
    # Close price column identification
    if 'close' in df.columns:
        close_col = 'close'
    elif '0' in df.columns:
        close_col = '0'
    else:
        close_col = df.columns[3] if len(df.columns) > 3 else None

    # Volume column identification
    if 'volume' in df.columns:
        vol_col = 'volume'
    elif '2' in df.columns:
        vol_col = '2'
    elif '3' in df.columns:
        vol_col = '3'
    else:
        vol_col = df.columns[-1]

    # Format Close
    if close_col and close_col in df.columns:
        df['Close'] = df[close_col].apply(lambda x: f"{float(x):,.2f}" if pd.notnull(x) else "-")
    else:
        df['Close'] = "-"

    # Format Volume
    if vol_col and vol_col in df.columns:
        df['Volume'] = df[vol_col].apply(lambda x: f"{int(float(x)):,}" if pd.notnull(x) else "-")
    else:
        df['Volume'] = "-"

    # Symbol
    df['Symbol'] = df['nsecode'] if 'nsecode' in df.columns else ''

    # TradingView Daily Chart Link Button
    df['Chart'] = df['nsecode'].apply(
        lambda symbol: f'<a href="https://in.tradingview.com/chart/?symbol=NSE:{symbol}&interval=D" target="_blank" class="chart-btn">📈 Daily Chart</a>'
    )

    # Columns Sequence: Symbol, Close, Volume, Chart (Stock Name Removed)
    final_df = df[['Symbol', 'Close', 'Volume', 'Chart']].copy()

    html_table = final_df.to_html(index=False, escape=False, classes='custom-table')
else:
    html_table = "<p style='text-align:center; padding:20px; font-weight:bold;'>No stock has appeared in the filter yet.</p>"

# 3. Fully Responsive HTML Page (Mobile, Tablet, PC)
full_html = f"""
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 8px;
            background-color: #ffffff;
        }}
        /* Responsive Table Container */
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
        table.custom-table tr:hover {{
            background-color: #f8fafc;
        }}
        /* Mobile Touch-Friendly Button */
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
        .chart-btn:hover {{
            background-color: #1d4ed8;
        }}

        /* Mobile Adjustments */
        @media screen and (max-width: 600px) {{
            table.custom-table {{
                font-size: 16px;
            }}
            table.custom-table th, table.custom-table td {{
                padding: 8px 8px;
            }}
            .chart-btn {{
                padding: 5px 8px;
                font-size: 14px;
            }}
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

print("Scraper successfully updated for mobile responsiveness!")
