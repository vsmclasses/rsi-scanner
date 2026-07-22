import requests
from bs4 import BeautifulSoup
import pandas as pd

# Aapka Scanner URL
screener_url = "https://chartink.com/screener/vikasrsi"
process_url = "https://chartink.com/screener/process"

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 1. Page se CSRF Token aur Condition Clause (scan_clause) nikalna
response = session.get(screener_url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

csrf_token = soup.select_one('[name="csrf-token"]')['content']

# Condition input element se exact condition text read karna
scan_clause_element = soup.find('input', {'id': 'scan_clause'}) or soup.find('textarea', {'name': 'scan_clause'})

if scan_clause_element:
    scan_clause = scan_clause_element.get('value', '')
else:
    # Fallback agar text direct na mile
    scan_clause = '( {cash} ( [0] 15 minute rsi > 60 ) )'

# 2. Chartink Engine ko Exact Condition Bhejna
post_headers = {
    'x-csrf-token': csrf_token,
    'referer': screener_url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

payload = {
    'scan_clause': scan_clause
}

res = session.post(process_url, headers=post_headers, data=payload)
data = res.json()

# 3. Data Ko Table Form Mein Convert Karna
if 'data' in data and len(data['data']) > 0:
    df = pd.DataFrame(data['data'])
    
    # Matching exact Chartink columns
    df = df[['sr', 'name', 'nsecode', 'close', 'per_chg', 'volume']]
    df.columns = ['Sr.', 'Stock Name', 'Symbol', 'Close', '%_Change', 'Volume']
    
    # % Change ke aage % symbol lagana
    df['%_Change'] = df['%_Change'].apply(lambda x: f"{x:.2f}%")
    
    html_table = df.to_html(index=False, classes='chartink-table')
else:
    html_table = "<p style='text-align:center; padding:20px; font-weight:bold;'>Koi stock condition me match nahi hua.</p>"

# 4. Final HTML File
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 10px; background: #fff; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; text-align: left; }}
        th {{ background-color: #f0f4f9; color: #333; padding: 12px 8px; border-bottom: 2px solid #ccc; font-weight: 600; }}
        td {{ padding: 10px 8px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background-color: #f8f9fa; }}
        td:nth-child(5) {{ color: #2e7d32; font-weight: bold; }} /* Green color for %_Change */
    </style>
</head>
<body>
    {html_table}
</body>
</html>
"""

with open("rsi.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Data successfully fetched!")
