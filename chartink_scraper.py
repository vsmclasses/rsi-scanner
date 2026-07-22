import requests
import pandas as pd

# Chartink process endpoint
process_url = "https://chartink.com/screener/process"
screener_url = "https://chartink.com/screener/vikasrsi"

session = requests.Session()

# Step 1: CSRF Token & Cookies Fetch karna
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# CSRF token fetch karne ke liye main page request
req = session.get(screener_url, headers=headers)
csrf_token = req.text.split('name="csrf-token" content="')[1].split('"')[0]

post_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-csrf-token': csrf_token,
    'origin': 'https://chartink.com',
    'referer': screener_url
}

# Step 2: Aapke scanner ki exact Condition Clause
# Note: Agar scanner mein multiple conditions hain, toh exact condition yahan set ki hai
payload = {
    'scan_clause': '( {cash} ( [0] 15 minute rsi > 60 ) )'
}

res = session.post(process_url, headers=post_headers, data=payload)
data = res.json()

# Step 3: Result Table Build karna
if 'data' in data and len(data['data']) > 0:
    df = pd.DataFrame(data['data'])
    
    # Sr No column add karna
    df['sr'] = range(1, len(df) + 1)
    
    # Required Columns
    df = df[['sr', 'name', 'nsecode', 'close', 'per_chg', 'volume']]
    df.columns = ['Sr.', 'Stock Name', 'Symbol', 'Close', '%_Change', 'Volume']
    
    # Formatting
    df['%_Change'] = df['%_Change'].apply(lambda x: f"{x:.2f}%")
    df['Volume'] = df['Volume'].apply(lambda x: f"{x:,}")
    
    html_table = df.to_html(index=False, classes='chartink-table')
else:
    html_table = "<p style='text-align:center; padding:20px; font-weight:bold;'>Abhi koi stock filter mein nahi aaya.</p>"

# HTML Output Layout
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 10px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; text-align: left; }}
        th {{ background-color: #eef2f7; color: #333; padding: 10px; border-bottom: 2px solid #ccc; font-weight: 600; }}
        td {{ padding: 8px 10px; border-bottom: 1px solid #eee; }}
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

print("Scan output updated!")
