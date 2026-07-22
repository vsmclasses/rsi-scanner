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

# 2. Filtering & Customizing Table Columns
if 'data' in data and len(data['data']) > 0:
    df = pd.DataFrame(data['data'])
    
    # 1. Format CMP (Close Price)
    df['cmp_val'] = df['close'].apply(lambda x: f"{x:,.2f}" if pd.notnull(x) else "-")
    
    # 2. Format Volume
    df['vol_val'] = df['volume'].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "-")
    
    # 3. Create TradingView Daily Chart Button Link
    df['chart_btn'] = df['nsecode'].apply(
        lambda symbol: f'<a href="https://in.tradingview.com/chart/?symbol=NSE:{symbol}&interval=D" target="_blank" class="chart-btn">📈 Daily Chart</a>'
    )
    
    # Selecting only required columns: Stock Name, CMP, Volume, Chart
    final_df = df[['name', 'cmp_val', 'vol_val', 'chart_btn']].copy()
    final_df.columns = ['Stock Name', 'CMP', 'Volume', 'Chart']
    
    # Convert to HTML (escape=False for rendering HTML link button)
    html_table = final_df.to_html(index=False, escape=False, classes='custom-table')
else:
    html_table = "<p style='text-align:center; padding:20px; font-weight:bold;'>Abhi koi stock filter mein nahi aaya.</p>"

# 3. Styling similar to reference design
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 10px;
            background-color: #fff;
        }}
        table.custom-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            text-align: left;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        table.custom-table th {{
            background-color: #1e293b;
            color: #ffffff;
            padding: 12px 15px;
            font-weight: 600;
            text-align: center;
        }}
        table.custom-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e2e8f0;
            text-align: center;
            color: #0f172a;
            font-weight: 500;
        }}
        table.custom-table td:first-child {{
            font-weight: bold;
            text-align: left;
            padding-left: 20px;
        }}
        table.custom-table tr:hover {{
            background-color: #f8fafc;
        }}
        /* Daily Chart Button Style */
        .chart-btn {{
            background-color: #2563eb;
            color: #ffffff !important;
            padding: 6px 14px;
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
    </style>
</head>
<body>
    {html_table}
</body>
</html>
"""

with open("rsi.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Scraper successfully updated with TradingView links!")
