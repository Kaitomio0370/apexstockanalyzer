"""
APEX Stock Analyzer — Web Backend
Deploy to Render.com or Railway.app (free tier)
"""
import os, json, sqlite3, urllib.request, urllib.parse
from datetime import datetime
from flask import Flask, render_template, request, jsonify, g
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ── DATABASE ─────────────────────────────────────────────────────────
# Uses SQLite locally; swap for PostgreSQL on Render by setting DATABASE_URL env var
DATABASE_URL = os.environ.get("DATABASE_URL", "")
USE_PG = DATABASE_URL.startswith("postgres")

if USE_PG:
    import psycopg2, psycopg2.extras
    def get_conn():
        url = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        return psycopg2.connect(url, cursor_factory=psycopg2.extras.RealDictCursor)
else:
    DB_FILE = os.path.join(os.path.dirname(__file__), "apex.db")
    def get_conn():
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn

def qmark(sql):
    """Convert ? placeholders to %s for PostgreSQL"""
    return sql.replace("?", "%s") if USE_PG else sql

def init_db():
    conn = get_conn(); c = conn.cursor()
    stmts = [
        """CREATE TABLE IF NOT EXISTS analyses (
            id SERIAL PRIMARY KEY,
            ticker TEXT NOT NULL,
            company_name TEXT,
            price REAL,
            pe_ratio REAL,
            change_pct REAL,
            year_high REAL,
            year_low REAL,
            market_cap TEXT,
            financials_json TEXT,
            balance_json TEXT,
            technicals_json TEXT,
            news_json TEXT,
            ai_verdict TEXT,
            ai_full_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""" if USE_PG else
        """CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL, company_name TEXT,
            price REAL, pe_ratio REAL, change_pct REAL,
            year_high REAL, year_low REAL, market_cap TEXT,
            financials_json TEXT, balance_json TEXT,
            technicals_json TEXT, news_json TEXT,
            ai_verdict TEXT, ai_full_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS watchlist (
            id SERIAL PRIMARY KEY, ticker TEXT UNIQUE NOT NULL,
            company_name TEXT, target_price REAL, notes TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""" if USE_PG else
        """CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT, ticker TEXT UNIQUE NOT NULL,
            company_name TEXT, target_price REAL, notes TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS portfolio (
            id SERIAL PRIMARY KEY, ticker TEXT NOT NULL,
            shares REAL, avg_price REAL, notes TEXT,
            bought_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""" if USE_PG else
        """CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT, ticker TEXT NOT NULL,
            shares REAL, avg_price REAL, notes TEXT,
            bought_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY, ticker TEXT NOT NULL,
            content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""" if USE_PG else
        """CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, ticker TEXT NOT NULL,
            content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS api_keys (
            key_name TEXT PRIMARY KEY, key_value TEXT
        )"""
    ]
    for s in stmts:
        c.execute(s)
    conn.commit(); conn.close()
    print("✓ DB ready")

# ── KEY HELPERS ───────────────────────────────────────────────────────
def get_key(name):
    # Env vars take priority (set on Render dashboard)
    env_map = {"fmp": "FMP_KEY", "av": "AV_KEY", "news": "NEWS_KEY", "claude": "CLAUDE_KEY"}
    env_val = os.environ.get(env_map.get(name, ""), "")
    if env_val: return env_val
    conn = get_conn(); c = conn.cursor()
    c.execute(qmark("SELECT key_value FROM api_keys WHERE key_name=?"), (name,))
    row = c.fetchone(); conn.close()
    return (row["key_value"] if USE_PG else row[0]) if row else ""

def set_key(name, value):
    conn = get_conn(); c = conn.cursor()
    if USE_PG:
        c.execute("INSERT INTO api_keys(key_name,key_value) VALUES(%s,%s) ON CONFLICT(key_name) DO UPDATE SET key_value=EXCLUDED.key_value", (name, value))
    else:
        c.execute("INSERT OR REPLACE INTO api_keys(key_name,key_value) VALUES(?,?)", (name, value))
    conn.commit(); conn.close()

# ── HTTP HELPER ───────────────────────────────────────────────────────
def fetch(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "APEX/2.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"Fetch error: {e} — {url[:70]}")
        return None

def call_claude(prompt, key):
    if not key:
        return "Add your Claude API key in Settings to enable AI analysis."
    try:
        body = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1500,
            "messages": [{"role": "user", "content": prompt}]
        }).encode()
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages", data=body,
            headers={"Content-Type": "application/json",
                     "x-api-key": key,
                     "anthropic-version": "2023-06-01"})
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.loads(r.read().decode())["content"][0]["text"]
    except Exception as e:
        return f"Claude error: {e}"

# ── ROUTES ────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/keys", methods=["GET", "POST"])
def keys_route():
    if request.method == "POST":
        d = request.json
        for k in ["fmp", "av", "news", "claude"]:
            if d.get(k): set_key(k, d[k])
        return jsonify({"ok": True})
    return jsonify({k: ("set" if get_key(k) else "") for k in ["fmp", "av", "news", "claude"]})

@app.route("/api/analyze/<ticker>")
def analyze(ticker):
    ticker = ticker.upper().strip()
    fmp = get_key("fmp"); av = get_key("av"); nk = get_key("news")

    # Parallel-style fetches (sequential but fast enough)
    quote_data = fetch(f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={fmp}") if fmp else None
    quote = quote_data[0] if isinstance(quote_data, list) and quote_data else None

    fins = fetch(f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=4&apikey={fmp}") if fmp else None
    bal = fetch(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?limit=2&apikey={fmp}") if fmp else None
    cf = fetch(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?limit=3&apikey={fmp}") if fmp else None
    ratios = fetch(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={fmp}") if fmp else None
    rsi = fetch(f"https://www.alphavantage.co/query?function=RSI&symbol={ticker}&interval=daily&time_period=14&series_type=close&apikey={av}") if av else None
    macd = fetch(f"https://www.alphavantage.co/query?function=MACD&symbol={ticker}&interval=daily&series_type=close&apikey={av}") if av else None
    sma50 = fetch(f"https://www.alphavantage.co/query?function=SMA&symbol={ticker}&interval=daily&time_period=50&series_type=close&apikey={av}") if av else None
    sma200 = fetch(f"https://www.alphavantage.co/query?function=SMA&symbol={ticker}&interval=daily&time_period=200&series_type=close&apikey={av}") if av else None

    # News
    news = []
    if nk:
        nd = fetch(f"https://newsapi.org/v2/everything?q={urllib.parse.quote(ticker)}+stock&sortBy=publishedAt&pageSize=10&language=en&apiKey={nk}")
        if nd and nd.get("articles"): news = nd["articles"]
    if not news and fmp:
        nd = fetch(f"https://financialmodelingprep.com/api/v3/stock_news?tickers={ticker}&limit=10&apikey={fmp}")
        if isinstance(nd, list): news = [{"title": a.get("title",""), "publishedAt": a.get("publishedDate",""), "source": {"name": a.get("site","")}, "url": a.get("url","")} for a in nd]

    # Save to DB
    if quote:
        conn = get_conn(); c = conn.cursor()
        c.execute(qmark("""INSERT INTO analyses
            (ticker,company_name,price,pe_ratio,change_pct,year_high,year_low,market_cap,
             financials_json,balance_json,technicals_json,news_json)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""),
            (ticker, quote.get("name",""), quote.get("price"), quote.get("pe"),
             quote.get("changesPercentage"), quote.get("yearHigh"), quote.get("yearLow"),
             str(quote.get("marketCap","")),
             json.dumps(fins), json.dumps(bal),
             json.dumps({"rsi":rsi,"macd":macd,"sma50":sma50,"sma200":sma200}),
             json.dumps(news[:5])))
        conn.commit(); conn.close()

    return jsonify({
        "ticker": ticker, "quote": quote,
        "financials": fins, "balance": bal, "cashflow": cf,
        "ratios": ratios[0] if isinstance(ratios,list) and ratios else ratios,
        "technicals": {"rsi":rsi,"macd":macd,"sma50":sma50,"sma200":sma200},
        "news": news[:10]
    })

@app.route("/api/ai-analyze", methods=["POST"])
def ai_analyze():
    d = request.json
    ticker = d.get("ticker","").upper()
    sd = d.get("data", {})
    claude_key = get_key("claude")

    q = sd.get("quote") or {}
    fin = (sd.get("financials") or [{}])[0]
    bal = (sd.get("balance") or [{}])[0]
    cf = (sd.get("cashflow") or [{}])[0]
    ratios = sd.get("ratios") or {}
    tech = sd.get("technicals") or {}
    news = sd.get("news") or []

    def fl(n):
        if not n or n=="—": return "—"
        try:
            v=float(n); a=abs(v); sign="-" if v<0 else ""
            if a>=1e12: return f"{sign}${a/1e12:.2f}T"
            if a>=1e9: return f"{sign}${a/1e9:.2f}B"
            if a>=1e6: return f"{sign}${a/1e6:.1f}M"
            return f"{sign}${v:,.0f}"
        except: return str(n)

    rsi_val="—"; macd_sig="—"; sma50_val="—"
    try:
        rd=list(tech.get("rsi",{}).get("Technical Analysis: RSI",{}).keys())
        if rd: rsi_val=tech["rsi"]["Technical Analysis: RSI"][rd[0]]["RSI"]
    except: pass
    try:
        md=list(tech.get("macd",{}).get("Technical Analysis: MACD",{}).keys())
        if md:
            m=float(tech["macd"]["Technical Analysis: MACD"][md[0]]["MACD"])
            s=float(tech["macd"]["Technical Analysis: MACD"][md[0]]["MACD_Signal"])
            macd_sig=f"{m:.2f} vs signal {s:.2f} → {'BULLISH' if m>s else 'BEARISH'}"
    except: pass
    try:
        sd2=list(tech.get("sma50",{}).get("Technical Analysis: SMA",{}).keys())
        if sd2: sma50_val=tech["sma50"]["Technical Analysis: SMA"][sd2[0]]["SMA"]
    except: pass

    headlines="\n".join([a.get("title","") for a in news[:5]])

    prompt=f"""You are a senior equity analyst. Analyze {ticker} ({q.get("name","")}) using this REAL live data:

PRICE DATA:
Price: ${q.get("price","—")} | Change: {q.get("changesPercentage","—")}% | P/E: {q.get("pe","—")}x
Market Cap: {fl(q.get("marketCap"))} | 52W Range: ${q.get("yearLow","—")} – ${q.get("yearHigh","—")}

INCOME STATEMENT (latest annual):
Revenue: {fl(fin.get("revenue"))} | Gross Margin: {f"{fin.get('grossProfitRatio',0)*100:.1f}%" if fin.get("grossProfitRatio") else "—"}
Net Income: {fl(fin.get("netIncome"))} | Net Margin: {f"{fin.get('netIncomeRatio',0)*100:.1f}%" if fin.get("netIncomeRatio") else "—"}
EPS: ${fin.get("epsdiluted","—")} | EBITDA: {fl(fin.get("ebitda"))}

BALANCE SHEET:
Cash: {fl(bal.get("cashAndCashEquivalents"))} | Total Debt: {fl(bal.get("totalDebt"))}
Total Assets: {fl(bal.get("totalAssets"))} | Equity: {fl(bal.get("totalStockholdersEquity"))}

CASH FLOW:
Operating CF: {fl(cf.get("operatingCashFlow"))} | Free CF: {fl(cf.get("freeCashFlow"))}

KEY RATIOS: ROE: {ratios.get("returnOnEquityTTM","—")} | D/E: {ratios.get("debtEquityRatioTTM","—")} | Current Ratio: {ratios.get("currentRatioTTM","—")}

TECHNICALS: RSI(14): {rsi_val} | MACD: {macd_sig} | 50-Day SMA: ${sma50_val}

RECENT NEWS:
{headlines or "(none)"}

Give a structured investment analysis with EXACTLY these sections:

VERDICT: [Strong Buy / Buy / Hold / Reduce / Sell]
SCORES: Financial Health [x/10] | Growth [x/10] | Value [x/10] | Momentum [x/10] | Sentiment [x/10]

BULL CASE:
• [data-backed reason 1]
• [data-backed reason 2]
• [data-backed reason 3]

BEAR CASE:
• [specific risk 1]
• [specific risk 2]
• [specific risk 3]

PRICE TARGET: 12-month range $[low]–$[high] | Base case: $[price]

FINAL TAKE:
[2-3 direct sentences. Honest. Reference actual numbers.]

Use real figures. No generic statements."""

    result = call_claude(prompt, claude_key)

    # Extract verdict and save
    verdict_line = ""
    for line in result.split("\n"):
        if line.startswith("VERDICT:"): verdict_line = line.replace("VERDICT:","").strip()
    conn = get_conn(); c = conn.cursor()
    c.execute(qmark("UPDATE analyses SET ai_verdict=?,ai_full_text=? WHERE ticker=? AND id=(SELECT id FROM analyses WHERE ticker=? ORDER BY created_at DESC LIMIT 1)"),
              (verdict_line, result, ticker, ticker))
    conn.commit(); conn.close()

    return jsonify({"text": result, "verdict": verdict_line})

# ── WATCHLIST ─────────────────────────────────────────────────────────
@app.route("/api/watchlist", methods=["GET","POST"])
def watchlist():
    conn=get_conn(); c=conn.cursor()
    if request.method=="POST":
        d=request.json; ticker=d.get("ticker","").upper()
        try:
            if USE_PG:
                c.execute("INSERT INTO watchlist(ticker,company_name,target_price,notes) VALUES(%s,%s,%s,%s) ON CONFLICT(ticker) DO NOTHING",(ticker,d.get("company_name",""),d.get("target_price"),d.get("notes","")))
            else:
                c.execute("INSERT OR IGNORE INTO watchlist(ticker,company_name,target_price,notes) VALUES(?,?,?,?)",(ticker,d.get("company_name",""),d.get("target_price"),d.get("notes","")))
            conn.commit(); conn.close()
            return jsonify({"ok":True})
        except Exception as e:
            conn.close(); return jsonify({"ok":False,"error":str(e)})
    c.execute("SELECT * FROM watchlist ORDER BY added_at DESC")
    rows=[dict(r) for r in c.fetchall()]; conn.close()
    return jsonify(rows)

@app.route("/api/watchlist/<ticker>", methods=["DELETE"])
def delete_watchlist(ticker):
    conn=get_conn(); c=conn.cursor()
    c.execute(qmark("DELETE FROM watchlist WHERE ticker=?"),(ticker.upper(),))
    conn.commit(); conn.close()
    return jsonify({"ok":True})

# ── PORTFOLIO ─────────────────────────────────────────────────────────
@app.route("/api/portfolio", methods=["GET","POST"])
def portfolio():
    conn=get_conn(); c=conn.cursor()
    if request.method=="POST":
        d=request.json
        c.execute(qmark("INSERT INTO portfolio(ticker,shares,avg_price,notes) VALUES(?,?,?,?)"),(d["ticker"].upper(),d["shares"],d["avg_price"],d.get("notes","")))
        conn.commit(); conn.close()
        return jsonify({"ok":True})
    c.execute("SELECT * FROM portfolio ORDER BY bought_at DESC")
    rows=[dict(r) for r in c.fetchall()]; conn.close()
    return jsonify(rows)

@app.route("/api/portfolio/<int:pid>", methods=["DELETE"])
def delete_portfolio(pid):
    conn=get_conn(); c=conn.cursor()
    c.execute(qmark("DELETE FROM portfolio WHERE id=?"),(pid,))
    conn.commit(); conn.close()
    return jsonify({"ok":True})

# ── NOTES ─────────────────────────────────────────────────────────────
@app.route("/api/notes/<ticker>")
def get_notes(ticker):
    conn=get_conn(); c=conn.cursor()
    c.execute(qmark("SELECT * FROM notes WHERE ticker=? ORDER BY created_at DESC"),(ticker.upper(),))
    rows=[dict(r) for r in c.fetchall()]; conn.close()
    return jsonify(rows)

@app.route("/api/notes", methods=["POST"])
def save_note():
    d=request.json; conn=get_conn(); c=conn.cursor()
    c.execute(qmark("INSERT INTO notes(ticker,content) VALUES(?,?)"),(d["ticker"].upper(),d["content"]))
    conn.commit(); conn.close()
    return jsonify({"ok":True})

@app.route("/api/notes/<int:nid>", methods=["DELETE"])
def delete_note(nid):
    conn=get_conn(); c=conn.cursor()
    c.execute(qmark("DELETE FROM notes WHERE id=?"),(nid,))
    conn.commit(); conn.close()
    return jsonify({"ok":True})

# ── HISTORY & STATS ───────────────────────────────────────────────────
@app.route("/api/history")
def history():
    conn=get_conn(); c=conn.cursor()
    c.execute("SELECT ticker,company_name,price,change_pct,ai_verdict,created_at FROM analyses ORDER BY created_at DESC LIMIT 50")
    rows=[dict(r) for r in c.fetchall()]; conn.close()
    return jsonify(rows)

@app.route("/api/stats")
def stats():
    conn=get_conn(); c=conn.cursor()
    def cnt(t): c.execute(f"SELECT COUNT(*) as n FROM {t}"); r=c.fetchone(); return r["n"] if USE_PG else r[0]
    def distinct(): c.execute("SELECT COUNT(DISTINCT ticker) as n FROM analyses"); r=c.fetchone(); return r["n"] if USE_PG else r[0]
    result={"analyses":cnt("analyses"),"watchlist":cnt("watchlist"),"portfolio":cnt("portfolio"),"tickers":distinct()}
    conn.close(); return jsonify(result)

# ── STARTUP ───────────────────────────────────────────────────────────
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"\n  APEX running → http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
