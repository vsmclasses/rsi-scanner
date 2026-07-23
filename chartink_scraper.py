import time
import json
import pandas as pd
from playwright.sync_api import sync_playwright

screener_url = "https://chartink.com/screener/vikasrsi"

captured_data = {}

def handle_response(response):
    global captured_data
    # Network request mein se Chartink process API ka exact JSON response pakdna
    if "screener/process" in response.url and response.status == 200:
        try:
            captured_data = response.json()
            print("Successfully captured Chartink JSON response!")
        except Exception as e:
            print("Error parsing captured JSON:", e)

with sync_playwright() as p:
    print("Launching headless Chromium browser...")
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )
    
    # Realistic User Agent simulation
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    
    page = context.new_page()
    
    # Network response listener attach karein
    page.on("response", handle_response)
    
    print(f"Opening Chartink URL: {screener_url}")
    page.goto(screener_url, wait_until="networkidle", timeout=60000)
    
    # Extra wait taaki agar koi button click/scan ho raha ho toh complete ho jaaye
    page.wait_for_timeout(5000)
    
    browser.close()

data = captured_data

# Data formatting for HTML Table
if 'data' in data and len(data['data']) > 0:
    df = pd.DataFrame(data['data'])

    # Close Column Identification
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

    # TradingView Daily Chart Link
    df['Chart'] = df['nsecode'].apply(
        lambda symbol: f'<a href="https://in.tradingview.com/chart/?symbol=NSE:{symbol}&interval=D" target="_blank" class="chart-btn">📈 Chart</a>'
    )

    final_df = df[['Symbol', 'Close', 'Volume', 'Chart']].copy()
    html_table = final_df.to_html(index=False, escape=False, classes='custom-table')
else:
    html_table = "<p style='text-align:center; padding:20px; font-weight:bold;'>No stock has appeared in the filter yet.</p>"

# Generating Responsive HTML Page
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

print("Playwright script finished execution successfully!")
