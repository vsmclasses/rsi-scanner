import yfinance as yf
import pandas as pd
import pandas_ta as ta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# 1. Aapke Stock List (NSE Symbols with .NS Extension)
STOCK_LIST = [
    "20MICRONS", "360ONE", "63MOONS", "AADHARHFC", "AARTIDRUGS", "AARTIIND", "AARTIPHARM", "ABB", "ABCAPITAL", "ABDL", "ABLBL", "ABREL", "ABSLAMC", "ACC", "ACE", "ACMESOLAR", "ACUTAAS", "ADANIENSOL", "ADANIENT", "ADANIGREEN", "ADANIPORTS", "ADANIPOWER", "ADFFOODS", "ADSL", "ADVANCE", "ADVENTHTL", "ADVENZYMES", "AEGISLOG", "AEGISVOPAK", "AEQUS", "AEROENTER", "AEROFLEX", "AETHER", "AFCONS", "AFFLE", "AGARWALEYE", "AGI", "AGIIL", "AIIL", "AJANTPHARM", "AJMERA", "AKUMS", "ALEMBICLTD", "AMAGI", "AMBER", "AMBUJACEM", "AMIRCHAND", "ANANDRATHI", "ANANTRAJ", "ANDHRSUGAR", "ANGELONE", "ANTHEM", "ANURAS", "APEX", "APLAPOLLO", "APLLTD", "APOLLO", "APOLLOHOSP", "APOLLOPIPE", "APOLLOTYRE", "APTECHT", "APTUS", "ARE&M", "ARFIN", "ARIHANTCAP", "ARIS", "ARKADE", "ARSSBL", "ARTEMISMED", "ARVIND", "ARVINDFASN", "ASHAPURMIN", "ASHOKA", "ASHOKLEY", "ASIANENE", "ASIANPAINT", "ASKAUTOLTD", "ASTERDM", "ASTRAL", "ASTRAMICRO", "ATGL", "ATHERENERG", "ATULAUTO", "AUBANK", "AURIONPRO", "AUROPHARMA", "AURUM", "AUTOIND", "AVALON", "AVANTEL", "AVANTIFEED", "AVL", "AWFIS", "AWHCL", "AWL", "AXISBANK", "AXISCADES", "AYE", "AYMSYNTEX", "AZAD", "BAJAJ-AUTO", "BAJAJCON", "BAJAJELEC", "BAJAJFINSV", "BAJAJHCARE", "BAJAJHFL", "BAJEL", "BAJFINANCE", "BALAJITELE", "BALAMINES", "BALKRISIND", "BALMLAWRIE", "BALRAMCHIN", "BALUFORGE", "BANCOINDIA", "BANDHANBNK", "BANKBARODA", "BANKINDIA", "BANSALWIRE", "BATAINDIA", "BBOX", "BDL", "BECTORFOOD", "BEL", "BELRISE", "BEML", "BEPL", "BERGEPAINT", "BHAGCHEM", "BHAGYANGR", "BHARATFORG", "BHARATSE", "BHARATWIRE", "BHARTIARTL", "BHARTIHEXA", "BHEL", "BIOCON", "BLACKBUCK", "BLISSGVS", "BLS", "BLSE", "BLUEJET", "BLUESTARCO", "BLUESTONE", "BLUSPRING", "BOMDYEING", "BOROLTD", "BORORENEW", "BOROSCI", "BPCL", "BRIGADE", "BRITANNIA", "BSE", "BSOFT", "CAMLINFINE", "CAMPUS", "CAMS", "CANBK", "CANFINHOME", "CANHLIFE", "CAPACITE", "CAPILLARY", "CAPLIPOINT", "CARBORUNIV", "CARTRADE", "CARYSIL", "CASTROLIND", "CCL", "CDSL", "CEATLTD", "CEIGALL", "CELLO", "CEMPRO", "CESC", "CEWATER", "CGCL", "CGPOWER", "CHALET", "CHAMBLFERT", "CHEMPLASTS", "CHENNPETRO", "CHOICEIN", "CHOLAFIN", "CHOLAHLDNG", "CIEINDIA", "CIPLA", "CLEAN", "CLEANMAX", "CMPDI", "CMRGREEN", "CMSINFO", "COALINDIA", "COCHINSHIP", "COFORGE", "COHANCE", "COLPAL", "COMSYN", "CONCOR", "CONCORDBIO", "CONFIPET", "COROMANDEL", "CPPLUS", "CRAMC", "CREDITACC", "CRISIL", "CRIZAC", "CROMPTON", "CSBBANK", "CUB", "CUMMINSIND", "CUPID", "CYIENT", "CYIENTDLM", "DABUR", "DALBHARAT", "DALMIASUG", "DAMCAPITAL", "DATAMATICS", "DATAPATTNS", "DBREALTY", "DCAL", "DCBBANK", "DCXINDIA", "DDEVPLSTIK", "DEEDEV", "DEEPAKFERT", "DEEPAKNTR", "DEEPINDS", "DELHIVERY", "DENTA", "DEVYANI", "DHAMPURSUG", "DIACABS", "DIFFNKG", "DIGITIDE", "DIVISLAB", "DIXON", "DJML", "DLF", "DLINKINDIA", "DMART", "DOLATALGO", "DOLLAR", "DREDGECORP", "DRREDDY", "DYCL", "E2E", "EBGNG", "ECLERX", "ECOSMOBLTY", "EDELWEISS", "EFCIL", "EICHERMOT", "EIDPARRY", "EIEL", "EIHOTEL", "EKC", "ELECON", "ELECTCAST", "ELGIEQUIP", "ELIN", "EMAMILTD", "EMCURE", "EMIL", "EMMVEE", "EMSLIMITED", "ENDURANCE", "ENGINERSIN", "ENRIN", "EPACK", "EPACKPEB", "EPL", "EQUITASBNK", "ESCORTS", "ETERNAL", "EUREKAFORB", "EUROPRATIK", "EVEREADY", "EXCELSOFT", "EXICOM", "EXIDEIND", "FABTECH", "FACT", "FDC", "FEDERALBNK", "FEDFINA", "FINCABLES", "FINOPB", "FIRSTCRY", "FIVESTAR", "FLAIR", "FLUOROCHEM", "FORCEMOT", "FORTIS", "FRACTAL", "FSL", "FUSION", "GABRIEL", "GAEL", "GAIL", "GANDHAR", "GANECOS", "GANESHBE", "GANESHHOU", "GARUDA", "GAUDIUMIVF", "GCSL", "GEMAROMA", "GENESYS", "GENUSPOWER", "GEOJITFSL", "GESHIP", "GHCL", "GHCLTEXTIL", "GICHSGFIN", "GICRE", "GIPCL", "GKENERGY", "GKSL", "GLAND", "GLENMARK", "GMBREW", "GMDCLTD", "GMRAIRPORT", "GMRP&UI", "GNA", "GNFC", "GNRL", "GOCLCORP", "GOCOLORS", "GODAVARIB", "GODFRYPHLP", "GODIGIT", "GODREJAGRO", "GODREJCP", "GODREJIND", "GODREJPROP", "GOKEX", "GOKULAGRO", "GOLDIAM", "GOODLUCK", "GPIL", "GPPL", "GPTHEALTH", "GPTINFRA", "GRANULES", "GRAPHITE", "GRASIM", "GRAUWEIL", "GRAVITA", "GREAVESCOT", "GREENPANEL", "GREENPLY", "GRMOVER", "GROWW", "GRSE", "GSFC", "GSPCROP", "GUFICBIO", "GVPIL", "GVT&D", "HAL", "HAPPSTMNDS", "HARIOMPIPE", "HARSHA", "HAVELLS", "HBLENGINE", "HCG", "HCLTECH", "HDBFS", "HDFCAMC", "HDFCBANK", "HDFCLIFE", "HEG", "HERITGFOOD", "HEROMOTOCO", "HEXAGON", "HFCL", "HIKAL", "HIMATSEIDE", "HINDALCO", "HINDCOPPER", "HINDPETRO", "HINDUNILVR", "HINDWAREAP", "HINDZINC", "HITECH", "HLEGLAS", "HOMEFIRST", "HONASA", "HPL", "HSCL", "HUBTOWN", "HUDCO", "HUHTAMAKI", "HYUNDAI", "ICICIAMC", "ICICIBANK", "ICICIGI", "ICICIPRULI", "ICIL", "IDBI", "IDEAFORGE", "IDFCFIRSTB", "IEX", "IFBIND", "IFCI", "IFGLEXPOR", "IGARASHI", "IGCL", "IGIL", "IGL", "IIFL", "IIFLCAPS", "IKIO", "IKS", "IMFA", "INA", "INDGN", "INDHOTEL", "INDIACEM", "INDIAGLYCO", "INDIAMART", "INDIANB", "INDIANHUME", "INDIGO", "INDNIPPON", "INDOBORAX", "INDOCO", "INDOFARM", "INDOSTAR", "INDOTHAI", "INDRAMEDCO", "INDSWFTLAB", "INDUSINDBK", "INDUSTOWER", "INFOBEAN", "INFY", "INOXGREEN", "INOXINDIA", "INOXWIND", "INTELLECT", "IOC", "IOLCP", "IONEXCHANG", "IPCALAB", "IPL", "IRCON", "IRCTC", "IREDA", "IRFC", "ITC", "ITCHOTELS", "ITDC", "ITI", "IVALUE", "IXIGO", "J&KBANK", "JAGSNPHARM", "JAICORPLTD", "JAINREC", "JAMNAAUTO", "JARO", "JASH", "JAYBARMARU", "JAYKAY", "JAYNECOIND", "JBCHEPHARM", "JBMA", "JGCHEM", "JINDALSAW", "JINDALSTEL", "JINDRILL", "JIOFIN", "JKIL", "JKLAKSHMI", "JKPAPER", "JKTYRE", "JMFINANCIL", "JNKINDIA", "JSFB", "JSL", "JSLL", "JSWCEMENT", "JSWENERGY", "JSWINFRA", "JSWSTEEL", "JTEKTINDIA", "JTLIND", "JUBLFOOD", "JUBLINGREA", "JUBLPHARMA", "JUSTDIAL", "JWL", "JYOTHYLAB", "JYOTICNC", "KAJARIACER", "KALAMANDIR", "KALYANKJIL", "KANSAINER", "KARURVYSYA", "KAYNES", "KCP", "KEC", "KEI", "KERNEX", "KFINTECH", "KIMS", "KIRIINDUS", "KIRLFER", "KIRLOSENG", "KIRLPNU", "KISSHT", "KITEX", "KNRCON", "KOTAKBANK", "KOTIC", "KPEL", "KPIGREEN", "KPIL", "KPITTECH", "KPRMILL", "KRBL", "KRISHANA", "KRISHNADEF", "KRN", "KROSS", "KSHINTL", "KTKBANK", "LALPATHLAB", "LANDMARK", "LATENTVIEW", "LAURUSLABS", "LAXMIDENTL", "LEMONTREE", "LENSKART", "LGEINDIA", "LICHSGFIN", "LICI", "LLOYDSENGG", "LLOYDSENT", "LLOYDSME", "LODHA", "LOKESHMACH", "LOTUSDEV", "LT", "LTF", "LTFOODS", "LTM", "LTTS", "LUMAXTECH", "LUPIN", "LXCHEM", "M&M", "M&MFIN", "MAHABANK", "MAHLIFE", "MAHLOG", "MAHSEAMLES", "MANAKCOAT", "MANAPPURAM", "MANBA", "MANCREDIT", "MANINDS", "MANINFRA", "MANKIND", "MANORAMA", "MANYAVAR", "MAPMYINDIA", "MARICO", "MARINE", "MARKOLINES", "MARKSANS", "MARSONS", "MARUTI", "MASFIN", "MASTERTR", "MAWANASUG", "MAXHEALTH", "MAYURUNIQ", "MAZDOCK", "MBAPL", "MBEL", "MCX", "MEDANTA", "MEDIASSIST", "MEESHO", "MENNPIS", "METROPOLIS", "MFSL", "MGL", "MHRIL", "MIDHANI", "MINDACORP", "MMFL", "MOBIKWIK", "MOIL", "MONARCH", "MOSCHIP", "MOTHERSON", "MOTILALOFS", "MPHASIS", "MRPL", "MSTCLTD", "MTARTECH", "MUFIN", "MUNJALAU", "MUTHOOTFIN", "MUTHOOTMF", "NACLIND", "NAM-INDIA", "NATCOPHARM", "NATIONALUM", "NAUKRI", "NAVA", "NAVINFLUOR", "NAVKARCORP", "NAVNETEDUL", "NAZARA", "NBCC", "NCC", "NDTV", "NELCAST", "NELCO", "NESCO", "NESTLEIND", "NETWEB", "NEWGEN", "NFL", "NH", "NHPC", "NIACL", "NIBE", "NIITLTD", "NIITMTS", "NITCO", "NITINSPIN", "NIVABUPA", "NLCINDIA", "NMDC", "NOCIL", "NORTHARC", "NRBBEARING", "NRL", "NTPC", "NTPCGREEN", "NUVAMA", "NUVOCO", "NYKAA", "OBEROIRLTY", "OFSS", "OIL", "OLECTRA", "OMAXE", "OMINFRAL", "OMNI", "OMPOWER", "ONESOURCE", "ONGC", "OPTIEMUS", "ORIENTCEM", "ORIENTELEC", "ORIENTHOT", "ORIENTTECH", "OSWALPUMPS", "PACEDIGITK", "PAISALO", "PANACEABIO", "PANAMAPET", "PARADEEP", "PARAGMILK", "PARAS", "PARKHOSPS", "PARKHOTELS", "PATANJALI", "PATELRMART", "PAYTM", "PCBL", "PDMJEPAPER", "PENIND", "PERSISTENT", "PETRONET", "PFC", "PFOCUS", "PGEL", "PHOENIXLTD", "PICCADIL", "PIDILITIND", "PIGL", "PIIND", "PINELABS", "PLATIND", "PNB", "PNBGILTS", "PNBHOUSING", "PNCINFRA", "PNGJL", "PNGSREVA", "POCL", "POKARNA", "POLICYBZR", "POLYCAB", "POLYPLEX", "POONAWALLA", "POWERGRID", "POWERICA", "POWERINDIA", "PPLPHARMA", "PRAJIND", "PRAKASH", "PRECAM", "PRECWIRE", "PREMEXPLN", "PREMIERENE", "PRESTIGE", "PRICOLLTD", "PRINCEPIPE", "PROSTARM", "PROTEAN", "PRSMJOHNSN", "PSPPROJECT", "PTC", "PURVA", "PVRINOX", "PWL", "QPOWER", "QUADFUTURE", "QUESS", "RADICO", "RAILTEL", "RAIN", "RAINBOW", "RAJESHEXPO", "RAJRATAN", "RALLIS", "RAMCOIND", "RAMCOSYS", "RAMKY", "RAMRAT", "RATEGAIN", "RATNAVEER", "RAYMOND", "RAYMONDLSL", "RAYMONDREL", "RBA", "RBLBANK", "RCF", "RECLTD", "REDINGTON", "REDTAPE", "REFEX", "RELAXO", "RELIANCE", "RELIGARE", "RELTD", "REMSONSIND", "REPCOHOME", "RESPONIND", "RGL", "RHIM", "RICOAUTO", "RISHABH", "RITES", "RKFORGE", "RKSWAMY", "ROLEXRINGS", "ROSSTECH", "ROUTE", "RPTECH", "RRKABEL", "RSYSTEMS", "RUBICON", "RUPA", "RVNL", "SAATVIKGL", "SAIL", "SAILIFE", "SAIPARENT", "SAKAR", "SAKSOFT", "SAMBHV", "SAMHI", "SAMMAANCAP", "SANDHAR", "SANDUMA", "SANGHVIMOV", "SANSERA", "SANSTAR", "SAPPHIRE", "SARDAEN", "SAREGAMA", "SATIN", "SBCL", "SBFC", "SBICARD", "SBILIFE", "SBIN", "SCHNEIDER", "SCI", "SCODATUBES", "SEDEMAC", "SEIL", "SENCO", "SENORES", "SERVOTECH", "SESHAPAPER", "SETL", "SFL", "SGFIN", "SGMART", "SHADOWFAX", "SHAILY", "SHAKTIPUMP", "SHANTIGOLD", "SHARDACROP", "SHAREINDIA", "SHILPAMED", "SHINDL", "SHK", "SHREEJISPG", "SHREEPUSHK", "SHRINGARMS", "SHRIRAMFIN", "SHRIRAMPPS", "SHYAMMETL", "SIEMENS", "SIGMAADV", "SIGNATURE", "SIGNPOST", "SIKA", "SILGO", "SILVERTUC", "SIRCA", "SIS", "SJS", "SJVN", "SKIPPER", "SKMEGGPROD", "SKYGOLD", "SMCGLOBAL", "SMLMAH", "SMSPHARMA", "SOBHA", "SOLARA", "SOLARINDS", "SOLARWORLD", "SOMANYCERA", "SONACOMS", "SONATSOFTW", "SOTL", "SOUTHWEST", "SPAL", "SPANDANA", "SPARC", "SPMLINFRA", "SPORTKING", "SRF", "SRM", "SSWL", "STALLION", "STANLEY", "STAR", "STARCEMENT", "STARHEALTH", "STEELCAS", "STLTECH", "STOVEKRAFT", "STYL", "STYLEBAAZA", "SUDARSCHEM", "SUDEEPPHRM", "SULA", "SUMICHEM", "SUNDARMFIN", "SUNFLAG", "SUNPHARMA", "SUNTECK", "SUNTV", "SUPRAJIT", "SUPREMEIND", "SUPREMEINF", "SUPRIYA", "SURYAROSNI", "SURYODAY", "SUVEN", "SWANCORP", "SWIGGY", "SWSOLAR", "SYMPHONY", "SYNGENE", "SYRMA", "TAJGVK", "TALBROAUTO", "TANLA", "TARC", "TARIL", "TARSONS", "TATACAP", "TATACHEM", "TATACOMM", "TATACONSUM", "TATAELXSI", "TATAINVEST", "TATAPOWER", "TATASTEEL", "TATATECH", "TBOTEK", "TBZ", "TCS", "TDPOWERSYS", "TECHM", "TECHNOE", "TEJASNET", "TEMBO", "TENNIND", "TEXINFRA", "TEXRAIL", "TFCILTD", "THANGAMAYL", "THELEELA", "THERMAX", "THOMASCOOK", "THYROCARE", "TI", "TIINDIA", "TIL", "TIMETECHNO", "TIMEX", "TIPSMUSIC", "TIRUMALCHM", "TITAGARH", "TITAN", "TMB", "TMCV", "TMPV", "TNPETRO", "TNPL", "TOLINS", "TORNTPHARM", "TORNTPOWER", "TPLPLASTEH", "TRANSRAILL", "TRENT", "TRITURBINE", "TRIVENI", "TRUALT", "TSFINV", "TVSMOTOR", "TVSSCS", "UDS", "UFBL", "UGROCAP", "ULTRACEMCO", "UNICHEMLAB", "UNIECOM", "UNIMECH", "UNIONBANK", "UNIPARTS", "UNITDSPR", "UNIVASTU", "UNIVCABLES", "UNOMINDA", "UPL", "URBANCO", "USHAMART", "UTIAMC", "UTLSOLAR", "V2RETAIL", "VAIBHAVGBL", "VARROC", "VBL", "VEDL", "VENUSPIPES", "VERANDA", "VGUARD", "VIDYAWIRES", "VIJAYA", "VIKRAMSOLR", "VIKRAN", "VIMTALABS", "VINCOFE", "VIPIND", "VISAKAIND", "VISHNU", "VIYASH", "VMART", "VMM", "VOLTAS", "VRLLOG", "VSTIND", "VTL", "WAAREEENER", "WAAREERTL", "WABAG", "WAKEFIT", "WALCHANNAG", "WANBURY", "WEBELSOLAR", "WEL", "WELCORP", "WELENT", "WELSPUNLIV", "WEWORK", "WHEELS", "WHIRLPOOL", "WIPRO", "WOCKPHARMA", "WSTCSTPAPR", "YATHARTH", "YATRA", "ZAGGLE", "ZEEL", "ZENSARTECH", "ZENTEC", "ZOTA", "ZUARI", "ZYDUSLIFE", "ZYDUSWELL"
]

def scan_stocks():
    matched_stocks = []
    
    # Bulk Download Data (Fast processing ke liye)
    tickers = [s + ".NS" for s in STOCK_LIST]
    print("Fetching Daily Data...")
    d_data = yf.download(tickers, period="6m", interval="1d", group_by='ticker', progress=False)
    print("Fetching Weekly Data...")
    w_data = yf.download(tickers, period="2y", interval="1wk", group_by='ticker', progress=False)
    print("Fetching Monthly Data...")
    m_data = yf.download(tickers, period="5y", interval="1mo", group_by='ticker', progress=False)

    for symbol in STOCK_LIST:
        try:
            ns_symbol = symbol + ".NS"
            df_d = d_data[ns_symbol].dropna()
            df_w = w_data[ns_symbol].dropna()
            df_m = m_data[ns_symbol].dropna()

            if len(df_d) < 30 or len(df_w) < 20 or len(df_m) < 15:
                continue

            # Indicators Calculation
            rsi_d = ta.rsi(df_d['Close'], length=14)
            rsi_w = ta.rsi(df_w['Close'], length=14)
            rsi_m = ta.rsi(df_m['Close'], length=14)
            sma_7 = ta.sma(df_d['Close'], length=7)

            # Extracting latest and previous values
            curr_close = float(df_d['Close'].iloc[-1])
            curr_open = float(df_d['Open'].iloc[-1])
            prev_close = float(df_d['Close'].iloc[-2])

            curr_vol = float(df_d['Volume'].iloc[-1])
            prev_vol = float(df_d['Volume'].iloc[-2])

            curr_rsi_d = float(rsi_d.iloc[-1])
            prev_rsi_d = float(rsi_d.iloc[-2])

            curr_rsi_w = float(rsi_w.iloc[-1])
            curr_rsi_m = float(rsi_m.iloc[-1])
            curr_sma7 = float(sma_7.iloc[-1])

            # Condition Checks (1 to 11)
            c1 = curr_rsi_d > 50                         # Current RSI > 50
            c2 = prev_rsi_d < 50                         # Prev RSI < 50
            c3 = curr_rsi_w > 60                         # Weekly RSI > 60
            c4 = curr_rsi_m > 60                         # Monthly RSI > 60
            c5 = curr_close > curr_sma7                  # Close > 7 SMA
            c6 = curr_vol > prev_vol                     # Volume > Prev Volume
            c7 = curr_close > curr_open                  # Green Candle
            c8 = ((curr_close - curr_open) / curr_open) <= 0.10             # Candle Size <= 10%
            c9 = ((curr_open - prev_close) / prev_close) <= 0.05            # Gap Up <= 5%
            c10 = ((curr_close - curr_sma7) / curr_sma7) >= 0.005           # Min 0.5% distance from 7 SMA
            c11 = curr_close <= (curr_sma7 * 1.03)                          # Close <= (7 SMA * 1.03)

            if c1 and c2 and c3 and c4 and c5 and c6 and c7 and c8 and c9 and c10 and c11:
                matched_stocks.append({
                    "Symbol": symbol,
                    "Close": round(curr_close, 2),
                    "Daily RSI": round(curr_rsi_d, 2),
                    "Weekly RSI": round(curr_rsi_w, 2),
                    "Monthly RSI": round(curr_rsi_m, 2),
                    "7 SMA": round(curr_sma7, 2)
                })

        except Exception as e:
            continue

    return pd.DataFrame(matched_stocks)

# Google Sheets Update Function
def update_google_sheet(df):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # Environment variable se credentials fetch karna (GitHub Actions ke liye)
    if "G_CREDENTIALS" in os.environ:
        creds_dict = json.loads(os.environ["G_CREDENTIALS"])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    else:
        # Local testing ke liye service_account.json
        creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)

    client = gspread.authorize(creds)
    sheet = client.open("Strategy_Breakout_Stocks").sheet1
    
    sheet.clear()
    sheet.append_row(["Symbol", "Close", "Daily RSI", "Weekly RSI", "Monthly RSI", "7 SMA"])
    
    if not df.empty:
        sheet.append_rows(df.values.tolist())
    print("Google Sheet updated successfully!")

if __name__ == "__main__":
    result_df = scan_stocks()
    print("Filtered Stocks:\n", result_df)
    update_google_sheet(result_df)
