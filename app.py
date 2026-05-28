<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>APEX — Stock Analyzer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&family=Syne:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
/* ═══════════════════════════════════════════════════════════════════
   APEX — Financial Dashboard · Dark OLED + Data-Dense Style
   UI/UX: JetBrains Mono (data) + Syne (display)
   Anti-patterns avoided: no purple gradients, no emoji icons,
   WCAG AA contrast, smooth transitions, proper hover states
═══════════════════════════════════════════════════════════════════ */
*{box-sizing:border-box;margin:0;padding:0;}
:root{
  --bg:#000;--bg2:#0a0a0a;--bg3:#111;--bg4:#181818;--bg5:#202020;
  --b1:#1c1c1c;--b2:#2a2a2a;--b3:#383838;
  --tx:#e8e8e8;--tx2:#888;--tx3:#484848;
  --g:#00e676;--gd:#00b85a;--gbg:rgba(0,230,118,.07);
  --r:#ff5252;--rbg:rgba(255,82,82,.07);
  --a:#ffab00;--abg:rgba(255,171,0,.07);
  --bl:#448aff;--blbg:rgba(68,138,255,.07);
  --mono:'JetBrains Mono',monospace;
  --disp:'Syne',sans-serif;
  --rad:6px;--radl:10px;
}
html,body{height:100%;background:var(--bg);color:var(--tx);font-family:var(--mono);font-size:13px;overflow-x:hidden;}
::-webkit-scrollbar{width:3px;height:3px;}
::-webkit-scrollbar-track{background:var(--bg2);}
::-webkit-scrollbar-thumb{background:var(--b3);border-radius:2px;}
button,input,select,textarea{font-family:var(--mono);}
a{color:var(--bl);text-decoration:none;}
a:hover{text-decoration:underline;}

/* ── LAYOUT ──────────────────────────────────────────────────────── */
.topbar{
  position:fixed;top:0;left:0;right:0;height:50px;
  display:flex;align-items:center;gap:12px;padding:0 18px;
  background:var(--bg2);border-bottom:1px solid var(--b1);z-index:100;
}
.body-wrap{display:flex;margin-top:50px;min-height:calc(100vh - 50px);}
.sidebar{width:220px;flex-shrink:0;border-right:1px solid var(--b1);background:var(--bg2);position:sticky;top:50px;height:calc(100vh - 50px);overflow-y:auto;}
.main-col{flex:1;min-width:0;display:flex;flex-direction:column;}
.ai-col{width:310px;flex-shrink:0;border-left:1px solid var(--b1);background:var(--bg2);position:sticky;top:50px;height:calc(100vh - 50px);display:flex;flex-direction:column;overflow:hidden;}
@media(max-width:1100px){.ai-col{display:none;}}
@media(max-width:800px){.sidebar{display:none;}.main-col{width:100%;}}

/* ── TOPBAR ──────────────────────────────────────────────────────── */
.logo{display:flex;align-items:center;gap:9px;margin-right:6px;flex-shrink:0;}
.logo-hex{width:20px;height:20px;background:var(--g);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);animation:glow 3s ease-in-out infinite;}
@keyframes glow{0%,100%{filter:drop-shadow(0 0 4px var(--g));}50%{filter:drop-shadow(0 0 12px var(--g));}}
.logo-text{font-family:var(--disp);font-size:16px;font-weight:800;letter-spacing:.08em;}
.search-box{display:flex;gap:6px;flex:1;max-width:400px;}
.search-box input{flex:1;background:var(--bg3);border:1px solid var(--b2);color:var(--tx);padding:6px 12px;border-radius:var(--rad);font-size:13px;letter-spacing:.06em;text-transform:uppercase;outline:none;transition:border-color .15s;}
.search-box input:focus{border-color:var(--g);}
.search-box input::placeholder{text-transform:none;letter-spacing:0;color:var(--tx3);}
.btn{padding:6px 14px;border-radius:var(--rad);font-size:12px;border:none;font-weight:500;cursor:pointer;transition:all .15s;letter-spacing:.04em;}
.btn-g{background:var(--g);color:#000;font-weight:600;}
.btn-g:hover{background:var(--gd);}
.btn-g:disabled{background:var(--bg4);color:var(--tx3);cursor:not-allowed;}
.btn-out{background:transparent;color:var(--tx2);border:1px solid var(--b2);}
.btn-out:hover{border-color:var(--b3);color:var(--tx);}
.top-right{margin-left:auto;display:flex;align-items:center;gap:8px;}
.live-pill{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--tx2);padding:4px 10px;border:1px solid var(--b1);border-radius:20px;}
.dot{width:6px;height:6px;border-radius:50%;background:var(--g);animation:blink 2s infinite;}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.3;}}

/* ── SIDEBAR ─────────────────────────────────────────────────────── */
.sb-section{padding:12px;border-bottom:1px solid var(--b1);}
.sb-label{font-size:10px;color:var(--tx3);letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px;}
.nav-btn{display:flex;align-items:center;gap:8px;width:100%;padding:7px 10px;border:none;background:transparent;color:var(--tx2);border-radius:var(--rad);cursor:pointer;font-size:12px;text-align:left;transition:all .12s;margin-bottom:2px;}
.nav-btn:hover,.nav-btn.active{background:var(--bg4);color:var(--tx);}
.nav-btn.active{color:var(--g);}
.nav-icon{font-size:10px;width:14px;text-align:center;}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:3px 0;}
.sl{font-size:11px;color:var(--tx2);}
.sv{font-size:12px;font-weight:500;}
.wl-row{display:flex;align-items:center;justify-content:space-between;padding:5px 0;border-bottom:1px solid var(--b1);}
.wl-row:last-child{border-bottom:none;}
.wl-t{font-size:12px;font-weight:600;cursor:pointer;color:var(--tx);}
.wl-t:hover{color:var(--g);}
.wl-x{background:none;border:none;color:var(--tx3);cursor:pointer;font-size:12px;padding:2px 5px;}
.wl-x:hover{color:var(--r);}

/* ── VIEWS ───────────────────────────────────────────────────────── */
.view{display:none;flex-direction:column;flex:1;}
.view.active{display:flex;}
.view-hd{padding:14px 20px;border-bottom:1px solid var(--b1);background:var(--bg2);display:flex;align-items:center;justify-content:space-between;flex-shrink:0;}
.view-title{font-family:var(--disp);font-size:15px;font-weight:700;}
.view-body{padding:20px;flex:1;overflow-y:auto;}

/* ── STOCK HEADER ────────────────────────────────────────────────── */
.sh{padding:14px 20px;border-bottom:1px solid var(--b1);background:var(--bg2);}
.sh-row{display:flex;align-items:flex-start;justify-content:space-between;}
.sh-ticker{font-family:var(--disp);font-size:28px;font-weight:800;line-height:1;}
.sh-name{font-size:11px;color:var(--tx2);margin-top:3px;}
.sh-price{font-family:var(--disp);font-size:26px;font-weight:700;text-align:right;}
.sh-chg{font-size:12px;text-align:right;margin-top:3px;}
.up{color:var(--g);}
.dn{color:var(--r);}
.mstrip{display:grid;grid-template-columns:repeat(6,1fr);gap:1px;margin-top:12px;border:1px solid var(--b1);border-radius:var(--rad);overflow:hidden;}
.ms{padding:8px 10px;background:var(--bg3);}
.ms-l{font-size:9px;color:var(--tx3);letter-spacing:.1em;text-transform:uppercase;}
.ms-v{font-size:13px;font-weight:500;margin-top:4px;}
@media(max-width:700px){.mstrip{grid-template-columns:repeat(3,1fr);}}

/* ── TABS ────────────────────────────────────────────────────────── */
.tab-bar{display:flex;border-bottom:1px solid var(--b1);background:var(--bg2);flex-shrink:0;overflow-x:auto;}
.tab{padding:10px 16px;font-size:11px;color:var(--tx2);cursor:pointer;border-bottom:2px solid transparent;white-space:nowrap;letter-spacing:.06em;transition:all .12s;}
.tab.active{color:var(--g);border-bottom-color:var(--g);}
.tab:hover:not(.active){color:var(--tx);}
.panel{display:none;padding:20px;overflow-y:auto;}
.panel.active{display:block;}
#p-chart{padding:0;display:none;height:520px;}
#p-chart.active{display:block;}

/* ── CARDS & TABLES ──────────────────────────────────────────────── */
.card{background:var(--bg3);border:1px solid var(--b1);border-radius:var(--radl);padding:14px;margin-bottom:14px;}
.card-t{font-size:10px;color:var(--tx2);letter-spacing:.1em;text-transform:uppercase;margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid var(--b1);}
.dt{width:100%;border-collapse:collapse;}
.dt tr{border-bottom:1px solid var(--b1);}
.dt tr:last-child{border-bottom:none;}
.dt td{padding:7px 2px;font-size:12px;}
.dt td:first-child{color:var(--tx2);}
.dt td:last-child{text-align:right;font-weight:500;}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;}
@media(max-width:600px){.g3,.g4{grid-template-columns:1fr 1fr;}.g2{grid-template-columns:1fr;}}
.pos{color:var(--g);}
.neg{color:var(--r);}
.neu{color:var(--a);}
.mcard{background:var(--bg3);border:1px solid var(--b1);border-radius:var(--rad);padding:12px;}
.mcard-l{font-size:9px;color:var(--tx2);letter-spacing:.1em;text-transform:uppercase;}
.mcard-v{font-size:20px;font-weight:600;margin-top:5px;font-family:var(--disp);}
.mcard-s{font-size:11px;color:var(--tx3);margin-top:3px;}

/* ── TECHNICALS ──────────────────────────────────────────────────── */
.sig-buy{color:var(--g);}
.sig-sell{color:var(--r);}
.sig-neu{color:var(--a);}

/* ── NEWS ────────────────────────────────────────────────────────── */
.ni{padding:11px 0;border-bottom:1px solid var(--b1);}
.ni:last-child{border-bottom:none;}
.ni-t{font-size:12px;line-height:1.55;margin-bottom:4px;}
.ni-m{font-size:10px;color:var(--tx2);display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
.badge{padding:2px 6px;border-radius:3px;font-size:9px;letter-spacing:.05em;}
.b-bull{background:var(--gbg);color:var(--g);}
.b-bear{background:var(--rbg);color:var(--r);}
.b-neu{background:var(--abg);color:var(--a);}

/* ── AI PANEL ────────────────────────────────────────────────────── */
.ai-hd{padding:12px 14px;border-bottom:1px solid var(--b1);flex-shrink:0;}
.ai-title{font-family:var(--disp);font-size:13px;font-weight:700;display:flex;align-items:center;gap:7px;}
.ai-sub{font-size:10px;color:var(--tx3);margin-top:3px;letter-spacing:.05em;}
.ai-run{width:100%;padding:10px;background:var(--g);color:#000;border:none;font-family:var(--disp);font-weight:700;font-size:13px;letter-spacing:.04em;cursor:pointer;transition:all .15s;flex-shrink:0;}
.ai-run:hover{background:var(--gd);}
.ai-run:disabled{background:var(--bg4);color:var(--tx3);cursor:not-allowed;}
.ai-body{flex:1;overflow-y:auto;padding:14px;}
.ai-empty{color:var(--tx3);font-size:12px;line-height:1.8;text-align:center;padding:40px 10px;}
.verdict-box{border-radius:var(--rad);padding:12px 14px;margin-bottom:14px;border:1px solid;}
.vb-buy{background:var(--gbg);border-color:rgba(0,230,118,.2);}
.vb-hold{background:var(--abg);border-color:rgba(255,171,0,.2);}
.vb-sell{background:var(--rbg);border-color:rgba(255,82,82,.2);}
.vr{font-family:var(--disp);font-size:18px;font-weight:800;margin-bottom:3px;}
.vr-buy{color:var(--g);}
.vr-hold{color:var(--a);}
.vr-sell{color:var(--r);}
.ai-section{margin-bottom:16px;}
.ai-st{font-size:9px;color:var(--tx2);letter-spacing:.12em;text-transform:uppercase;margin-bottom:7px;}
.ai-tx{font-size:11px;line-height:1.8;color:var(--tx2);white-space:pre-wrap;}
.wl-add-btn{width:100%;padding:7px;background:transparent;border:1px solid var(--b2);color:var(--tx2);border-radius:var(--rad);font-size:11px;cursor:pointer;transition:all .15s;margin-top:10px;}
.wl-add-btn:hover{border-color:var(--g);color:var(--g);}

/* ── SETTINGS ────────────────────────────────────────────────────── */
.sg{background:var(--bg3);border:1px solid var(--b1);border-radius:var(--radl);padding:16px;margin-bottom:16px;}
.sg-t{font-family:var(--disp);font-size:14px;font-weight:700;margin-bottom:14px;}
.sf{margin-bottom:12px;}
.sf:last-child{margin-bottom:0;}
.sf-l{font-size:10px;color:var(--tx2);letter-spacing:.1em;text-transform:uppercase;margin-bottom:5px;}
.sf-i{width:100%;background:var(--bg4);border:1px solid var(--b2);color:var(--tx);padding:8px 12px;border-radius:var(--rad);font-size:12px;outline:none;transition:border-color .15s;}
.sf-i:focus{border-color:var(--g);}
.sf-h{font-size:10px;color:var(--tx3);margin-top:4px;}

/* ── PORTFOLIO TABLE ─────────────────────────────────────────────── */
.ptbl{width:100%;border-collapse:collapse;}
.ptbl th{text-align:left;font-size:9px;color:var(--tx3);letter-spacing:.1em;text-transform:uppercase;padding:8px 10px;border-bottom:1px solid var(--b1);}
.ptbl td{padding:10px;border-bottom:1px solid var(--b1);font-size:12px;vertical-align:middle;}
.ptbl tr:last-child td{border-bottom:none;}
.ptbl tr:hover td{background:var(--bg3);}

/* ── HISTORY ─────────────────────────────────────────────────────── */
.hi{display:grid;grid-template-columns:80px 1fr auto;gap:12px;align-items:center;padding:10px 0;border-bottom:1px solid var(--b1);}
.hi:last-child{border-bottom:none;}
.hi-t{font-weight:600;cursor:pointer;color:var(--tx);}
.hi-t:hover{color:var(--g);}

/* ── NOTES ───────────────────────────────────────────────────────── */
.nc{background:var(--bg3);border:1px solid var(--b1);border-radius:var(--rad);padding:12px;margin-bottom:10px;}
.nc-tk{font-size:11px;font-weight:600;color:var(--g);margin-bottom:5px;}
.nc-body{font-size:12px;line-height:1.65;color:var(--tx);}
.nc-foot{display:flex;justify-content:space-between;font-size:10px;color:var(--tx3);margin-top:8px;}

/* ── MODALS ──────────────────────────────────────────────────────── */
.modal-bg{position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:200;display:none;align-items:center;justify-content:center;}
.modal-bg.open{display:flex;}
.modal{background:var(--bg3);border:1px solid var(--b2);border-radius:var(--radl);padding:22px;width:360px;max-width:95vw;}
.modal-t{font-family:var(--disp);font-size:15px;font-weight:700;margin-bottom:16px;display:flex;justify-content:space-between;align-items:center;}
.modal-x{background:none;border:none;color:var(--tx2);font-size:16px;cursor:pointer;line-height:1;}
.modal-x:hover{color:var(--tx);}

/* ── LOADING / EMPTY ─────────────────────────────────────────────── */
.loading{color:var(--tx3);font-size:12px;padding:30px;text-align:center;}
.spin{display:inline-block;width:16px;height:16px;border:1.5px solid var(--b3);border-top-color:var(--g);border-radius:50%;animation:spin .7s linear infinite;margin-right:8px;vertical-align:middle;}
@keyframes spin{to{transform:rotate(360deg);}}
.empty{color:var(--tx3);font-size:12px;text-align:center;padding:60px 20px;line-height:1.9;}
.empty-icon{font-size:24px;color:var(--b3);margin-bottom:10px;}

/* ── TREND BARS ──────────────────────────────────────────────────── */
.tbar-wrap{margin-bottom:10px;}
.tbar-labels{display:flex;justify-content:space-between;font-size:11px;color:var(--tx2);margin-bottom:4px;}
.tbar{height:5px;background:var(--b1);border-radius:3px;overflow:hidden;}
.tbar-fill{height:100%;border-radius:3px;transition:width .8s cubic-bezier(.4,0,.2,1);}
</style>
</head>
<body>

<!-- ── TOPBAR ── -->
<div class="topbar">
  <div class="logo">
    <div class="logo-hex"></div>
    <div class="logo-text">APEX</div>
  </div>
  <div class="search-box">
    <input id="ticker-inp" type="text" placeholder="Enter ticker…" maxlength="10"
           onkeydown="if(event.key==='Enter')analyze()">
    <button class="btn btn-g" id="analyze-btn" onclick="analyze()">ANALYZE</button>
  </div>
  <div class="top-right">
    <div class="live-pill"><div class="dot"></div><span id="src-lbl">loading…</span></div>
    <button class="btn btn-out" onclick="showView('settings')">SETTINGS</button>
  </div>
</div>

<!-- ── BODY ── -->
<div class="body-wrap">

  <!-- SIDEBAR -->
  <div class="sidebar">
    <div class="sb-section">
      <div class="sb-label">Navigation</div>
      <button class="nav-btn active" id="nav-analyzer" onclick="showView('analyzer')"><span class="nav-icon">◆</span>Analyzer</button>
      <button class="nav-btn" id="nav-watchlist" onclick="showView('watchlist')"><span class="nav-icon">◈</span>Watchlist</button>
      <button class="nav-btn" id="nav-portfolio" onclick="showView('portfolio')"><span class="nav-icon">▲</span>Portfolio</button>
      <button class="nav-btn" id="nav-history" onclick="showView('history')"><span class="nav-icon">◉</span>History</button>
      <button class="nav-btn" id="nav-notes" onclick="showView('notes')"><span class="nav-icon">◫</span>Notes</button>
      <button class="nav-btn" id="nav-settings" onclick="showView('settings')"><span class="nav-icon">◎</span>Settings</button>
    </div>
    <div class="sb-section">
      <div class="sb-label">Stats</div>
      <div class="stat-row"><div class="sl">Analyses</div><div class="sv" id="st-a">—</div></div>
      <div class="stat-row"><div class="sl">Tickers tracked</div><div class="sv" id="st-t">—</div></div>
      <div class="stat-row"><div class="sl">Watchlist</div><div class="sv" id="st-w">—</div></div>
      <div class="stat-row"><div class="sl">Positions</div><div class="sv" id="st-p">—</div></div>
    </div>
    <div class="sb-section">
      <div class="sb-label">Watchlist <span style="cursor:pointer;color:var(--g);margin-left:4px;" onclick="openModal('m-wl')">+</span></div>
      <div id="wl-sb"></div>
    </div>
  </div>

  <!-- MAIN -->
  <div class="main-col">

    <!-- ANALYZER VIEW -->
    <div class="view active" id="view-analyzer">
      <div id="sh-area">
        <div class="empty"><div class="empty-icon">◆</div>Enter a ticker symbol and click ANALYZE</div>
      </div>
      <div class="tab-bar" id="tab-bar" style="display:none;">
        <div class="tab active" onclick="switchTab('chart')">CHART</div>
        <div class="tab" onclick="switchTab('overview')">OVERVIEW</div>
        <div class="tab" onclick="switchTab('financials')">FINANCIALS</div>
        <div class="tab" onclick="switchTab('balance')">BALANCE SHEET</div>
        <div class="tab" onclick="switchTab('cashflow')">CASH FLOW</div>
        <div class="tab" onclick="switchTab('technicals')">TECHNICALS</div>
        <div class="tab" onclick="switchTab('news')">NEWS</div>
      </div>
      <div id="p-chart" class="panel">
        <div id="tv-hd" style="padding:8px 14px;background:var(--bg2);border-bottom:1px solid var(--b1);font-size:11px;color:var(--tx2);"></div>
        <div id="tv-wrap" style="flex:1;min-height:460px;"><div class="loading"><span class="spin"></span>Loading chart…</div></div>
      </div>
      <div id="p-overview" class="panel"><div class="loading"><span class="spin"></span>Loading…</div></div>
      <div id="p-financials" class="panel"><div class="loading"><span class="spin"></span>Loading…</div></div>
      <div id="p-balance" class="panel"><div class="loading"><span class="spin"></span>Loading…</div></div>
      <div id="p-cashflow" class="panel"><div class="loading"><span class="spin"></span>Loading…</div></div>
      <div id="p-technicals" class="panel"><div class="loading"><span class="spin"></span>Loading…</div></div>
      <div id="p-news" class="panel"><div class="loading"><span class="spin"></span>Loading…</div></div>
    </div>

    <!-- WATCHLIST VIEW -->
    <div class="view" id="view-watchlist">
      <div class="view-hd">
        <div class="view-title">Watchlist</div>
        <button class="btn btn-out" style="font-size:11px;" onclick="openModal('m-wl')">+ Add Stock</button>
      </div>
      <div class="view-body" id="wl-main"></div>
    </div>

    <!-- PORTFOLIO VIEW -->
    <div class="view" id="view-portfolio">
      <div class="view-hd">
        <div class="view-title">Portfolio</div>
        <button class="btn btn-out" style="font-size:11px;" onclick="openModal('m-pos')">+ Add Position</button>
      </div>
      <div class="view-body" id="port-body"></div>
    </div>

    <!-- HISTORY VIEW -->
    <div class="view" id="view-history">
      <div class="view-hd"><div class="view-title">Analysis History</div></div>
      <div class="view-body" id="hist-body"></div>
    </div>

    <!-- NOTES VIEW -->
    <div class="view" id="view-notes">
      <div class="view-hd">
        <div class="view-title">Research Notes</div>
        <button class="btn btn-out" style="font-size:11px;" id="add-note-btn" disabled onclick="openModal('m-note')">+ Add Note</button>
      </div>
      <div class="view-body" id="notes-body"></div>
    </div>

    <!-- SETTINGS VIEW -->
    <div class="view" id="view-settings">
      <div class="view-hd"><div class="view-title">Settings & API Keys</div></div>
      <div class="view-body" style="max-width:600px;">
        <div class="sg">
          <div class="sg-t">API Keys — saved to your server</div>
          <div class="sf">
            <div class="sf-l">Claude API Key</div>
            <input class="sf-i" type="password" id="k-claude" placeholder="sk-ant-…">
            <div class="sf-h">Get at <a href="https://console.anthropic.com" target="_blank">console.anthropic.com</a> — powers all AI analysis (~$0.003/analysis)</div>
          </div>
          <div class="sf">
            <div class="sf-l">Financial Modeling Prep</div>
            <input class="sf-i" type="password" id="k-fmp" placeholder="FMP API key">
            <div class="sf-h">Free at <a href="https://financialmodelingprep.com" target="_blank">financialmodelingprep.com</a> — financials, balance sheet, ratios (250 calls/day free)</div>
          </div>
          <div class="sf">
            <div class="sf-l">Alpha Vantage</div>
            <input class="sf-i" type="password" id="k-av" placeholder="Alpha Vantage key">
            <div class="sf-h">Free at <a href="https://www.alphavantage.co/support/#api-key" target="_blank">alphavantage.co</a> — RSI, MACD, moving averages (25 calls/day free)</div>
          </div>
          <div class="sf">
            <div class="sf-l">News API</div>
            <input class="sf-i" type="password" id="k-news" placeholder="News API key">
            <div class="sf-h">Free at <a href="https://newsapi.org/register" target="_blank">newsapi.org</a> — live news headlines (100 calls/day free)</div>
          </div>
          <button class="btn btn-g" onclick="saveKeys()" style="margin-top:10px;">SAVE KEYS</button>
          <div id="keys-saved" style="font-size:11px;color:var(--g);margin-top:8px;display:none;">✓ Keys saved</div>
        </div>
        <div class="sg">
          <div class="sg-t">How to Deploy This</div>
          <div style="font-size:12px;color:var(--tx2);line-height:1.9;">
            <b style="color:var(--tx);">Option A — Render.com (recommended, free)</b><br>
            1. Upload the project to GitHub<br>
            2. Go to <a href="https://render.com" target="_blank">render.com</a> → New Web Service → connect repo<br>
            3. Build command: <code style="color:var(--g);">pip install -r requirements.txt</code><br>
            4. Start command: <code style="color:var(--g);">python app.py</code><br>
            5. Add env vars: <code style="color:var(--g);">DATABASE_URL</code> from a free Render PostgreSQL instance<br><br>
            <b style="color:var(--tx);">Option B — Railway.app (also free)</b><br>
            Same steps — Railway auto-detects Flask and sets up PostgreSQL for you.<br><br>
            Your data saves permanently to PostgreSQL. API keys stored server-side.
          </div>
        </div>
      </div>
    </div>

  </div><!-- /main-col -->

  <!-- AI PANEL -->
  <div class="ai-col">
    <div class="ai-hd">
      <div class="ai-title"><div class="dot"></div>CLAUDE AI ANALYSIS</div>
      <div class="ai-sub">Synthesizes all data sources</div>
    </div>
    <button class="ai-run" id="ai-btn" disabled onclick="runAI()">ANALYZE WITH AI</button>
    <div class="ai-body" id="ai-body">
      <div class="ai-empty">Search for a stock and hit ANALYZE to fetch all data sources.<br><br>Then click ANALYZE WITH AI for Claude to synthesize everything into a full verdict.</div>
    </div>
  </div>

</div><!-- /body-wrap -->

<!-- ── MODALS ── -->
<div class="modal-bg" id="m-wl">
  <div class="modal">
    <div class="modal-t">Add to Watchlist <button class="modal-x" onclick="closeModal('m-wl')">✕</button></div>
    <div class="sf"><div class="sf-l">Ticker</div><input class="sf-i" id="wl-ticker" placeholder="AAPL" style="text-transform:uppercase;"></div>
    <div class="sf"><div class="sf-l">Target Price (optional)</div><input class="sf-i" id="wl-target" type="number" placeholder="0.00"></div>
    <div class="sf"><div class="sf-l">Notes (optional)</div><input class="sf-i" id="wl-notes" placeholder="Reason for watching…"></div>
    <button class="btn btn-g" onclick="addWatchlist()" style="width:100%;margin-top:6px;">ADD TO WATCHLIST</button>
  </div>
</div>

<div class="modal-bg" id="m-pos">
  <div class="modal">
    <div class="modal-t">Add Position <button class="modal-x" onclick="closeModal('m-pos')">✕</button></div>
    <div class="sf"><div class="sf-l">Ticker</div><input class="sf-i" id="pos-t" placeholder="AAPL" style="text-transform:uppercase;"></div>
    <div class="sf"><div class="sf-l">Shares</div><input class="sf-i" id="pos-s" type="number" placeholder="10"></div>
    <div class="sf"><div class="sf-l">Avg Buy Price ($)</div><input class="sf-i" id="pos-p" type="number" placeholder="150.00"></div>
    <div class="sf"><div class="sf-l">Notes (optional)</div><input class="sf-i" id="pos-n" placeholder="Entry thesis…"></div>
    <button class="btn btn-g" onclick="addPosition()" style="width:100%;margin-top:6px;">ADD POSITION</button>
  </div>
</div>

<div class="modal-bg" id="m-note">
  <div class="modal">
    <div class="modal-t">Research Note — <span id="note-ticker-lbl"></span> <button class="modal-x" onclick="closeModal('m-note')">✕</button></div>
    <div class="sf"><textarea class="sf-i" id="note-content" rows="6" placeholder="Your thesis, observations, what to watch…"></textarea></div>
    <button class="btn btn-g" onclick="saveNote()" style="width:100%;margin-top:6px;">SAVE NOTE</button>
  </div>
</div>

<script>
// ── STATE ─────────────────────────────────────────────────────────────────
const API = '';  // empty = same origin (works when deployed)
let ticker = '';
let stockData = {};

// ── INIT ──────────────────────────────────────────────────────────────────
async function init() {
  await loadKeys();
  await refreshStats();
  await loadWatchlistSidebar();
}

async function loadKeys() {
  try {
    const r = await fetch(`${API}/api/keys`);
    const k = await r.json();
    document.getElementById('k-claude').value = k.claude === 'set' ? '••••••••' : '';
    document.getElementById('k-fmp').value = k.fmp === 'set' ? '••••••••' : '';
    document.getElementById('k-av').value = k.av === 'set' ? '••••••••' : '';
    document.getElementById('k-news').value = k.news === 'set' ? '••••••••' : '';
    let count = 1;
    if (k.fmp) count++; if (k.av) count++; if (k.news) count++; count++;
    document.getElementById('src-lbl').textContent = `${count} sources active`;
  } catch(e) { document.getElementById('src-lbl').textContent = 'offline'; }
}

async function saveKeys() {
  const vals = {
    claude: document.getElementById('k-claude').value.trim(),
    fmp: document.getElementById('k-fmp').value.trim(),
    av: document.getElementById('k-av').value.trim(),
    news: document.getElementById('k-news').value.trim(),
  };
  // Don't send placeholder dots
  Object.keys(vals).forEach(k => { if (vals[k] === '••••••••') delete vals[k]; });
  await fetch(`${API}/api/keys`, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(vals)});
  const msg = document.getElementById('keys-saved');
  msg.style.display = 'block';
  setTimeout(() => msg.style.display = 'none', 3000);
  await loadKeys();
}

async function refreshStats() {
  try {
    const r = await fetch(`${API}/api/stats`);
    const s = await r.json();
    document.getElementById('st-a').textContent = s.analyses;
    document.getElementById('st-t').textContent = s.tickers;
    document.getElementById('st-w').textContent = s.watchlist;
    document.getElementById('st-p').textContent = s.portfolio;
  } catch(e) {}
}

// ── ANALYZE ───────────────────────────────────────────────────────────────
async function analyze() {
  const t = document.getElementById('ticker-inp').value.trim().toUpperCase();
  if (!t) return;
  ticker = t;
  stockData = {};

  const abtn = document.getElementById('analyze-btn');
  abtn.disabled = true; abtn.textContent = 'LOADING…';
  document.getElementById('ai-btn').disabled = true;
  document.getElementById('tab-bar').style.display = 'flex';
  document.getElementById('add-note-btn').disabled = false;
  document.getElementById('sh-area').innerHTML = '<div class="loading"><span class="spin"></span>Fetching market data…</div>';
  ['overview','financials','balance','cashflow','technicals','news'].forEach(p => {
    document.getElementById('p-'+p).innerHTML = '<div class="loading"><span class="spin"></span>Loading…</div>';
  });
  document.getElementById('ai-body').innerHTML = '<div class="ai-empty">Data loading… click ANALYZE WITH AI when ready.</div>';
  switchTab('chart');

  try {
    const r = await fetch(`${API}/api/analyze/${t}`);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const data = await r.json();
    stockData = data;
    renderHeader(data);
    renderChart(t);
    renderOverview(data);
    renderFinancials(data);
    renderBalance(data);
    renderCashflow(data);
    renderTechnicals(data);
    renderNews(data);
    await refreshStats();
    await loadWatchlistSidebar();
  } catch(e) {
    document.getElementById('sh-area').innerHTML = `<div class="loading" style="color:var(--r)">Error: ${e.message}<br><small>Make sure the backend is running and your FMP key is set.</small></div>`;
  }
  abtn.disabled = false; abtn.textContent = 'ANALYZE';
  document.getElementById('ai-btn').disabled = false;
}

// ── HEADER ────────────────────────────────────────────────────────────────
function renderHeader(d) {
  const q = d.quote || {};
  const chg = q.changesPercentage || 0;
  const up = chg >= 0;
  document.getElementById('sh-area').innerHTML = `
    <div class="sh">
      <div class="sh-row">
        <div><div class="sh-ticker">${q.symbol||ticker}</div><div class="sh-name">${q.name||''} &nbsp;·&nbsp; ${q.exchange||''}</div></div>
        <div><div class="sh-price">$${N(q.price)}</div><div class="sh-chg ${up?'up':'dn'}">${up?'▲':'▼'} ${N(Math.abs(q.change||0))} (${N(Math.abs(chg))}%)</div></div>
      </div>
      <div class="mstrip">
        <div class="ms"><div class="ms-l">Mkt Cap</div><div class="ms-v">${NL(q.marketCap)}</div></div>
        <div class="ms"><div class="ms-l">P/E</div><div class="ms-v">${q.pe?N(q.pe)+'x':'—'}</div></div>
        <div class="ms"><div class="ms-l">52W High</div><div class="ms-v">$${N(q.yearHigh)}</div></div>
        <div class="ms"><div class="ms-l">52W Low</div><div class="ms-v">$${N(q.yearLow)}</div></div>
        <div class="ms"><div class="ms-l">Volume</div><div class="ms-v">${NL(q.volume)}</div></div>
        <div class="ms"><div class="ms-l">Avg Vol</div><div class="ms-v">${NL(q.avgVolume)}</div></div>
      </div>
    </div>`;
}

// ── CHART ─────────────────────────────────────────────────────────────────
function renderChart(t) {
  document.getElementById('tv-hd').textContent = `${t} · Interactive Chart with RSI & MACD · TradingView`;
  document.getElementById('tv-wrap').innerHTML =
    `<iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tv&symbol=${encodeURIComponent(t)}&interval=D&hidesidetoolbar=0&hidetoptoolbar=0&symboledit=1&saveimage=1&toolbarbg=111111&studies=RSI%40tv-basicstudies%1FMACD%40tv-basicstudies%1FBollingerBandsR%40tv-basicstudies&theme=dark&style=1&timezone=exchange&withdateranges=1&showpopupbutton=1&locale=en"
    frameborder="0" allowfullscreen style="width:100%;height:480px;"></iframe>`;
}

// ── OVERVIEW ──────────────────────────────────────────────────────────────
function renderOverview(d) {
  const q=d.quote||{},r=d.ratios||{},f=(d.financials||[{}])[0];
  document.getElementById('p-overview').innerHTML = `
    <div class="g4" style="margin-bottom:14px;">
      ${mc('P/E Ratio',q.pe?N(q.pe)+'x':'—','')}
      ${mc('EV/EBITDA',r.enterpriseValueMultipleTTM?N(r.enterpriseValueMultipleTTM)+'x':'—','')}
      ${mc('P/FCF',r.priceToFreeCashFlowsRatioTTM?N(r.priceToFreeCashFlowsRatioTTM)+'x':'—','')}
      ${mc('P/S',r.priceToSalesRatioTTM?N(r.priceToSalesRatioTTM)+'x':'—','')}
    </div>
    <div class="g4" style="margin-bottom:14px;">
      ${mc('ROE',r.returnOnEquityTTM?N(r.returnOnEquityTTM*100)+'%':'—','')}
      ${mc('ROA',r.returnOnAssetsTTM?N(r.returnOnAssetsTTM*100)+'%':'—','')}
      ${mc('Gross Margin',f.grossProfitRatio?N(f.grossProfitRatio*100)+'%':'—','')}
      ${mc('Net Margin',f.netIncomeRatio?N(f.netIncomeRatio*100)+'%':'—','')}
    </div>
    <div class="card">
      <div class="card-t">Key Ratios</div>
      <table class="dt">
        <tr><td>Debt / Equity</td><td>${r.debtEquityRatioTTM?N(r.debtEquityRatioTTM)+'x':'—'}</td></tr>
        <tr><td>Current Ratio</td><td>${r.currentRatioTTM?N(r.currentRatioTTM)+'x':'—'}</td></tr>
        <tr><td>Quick Ratio</td><td>${r.quickRatioTTM?N(r.quickRatioTTM)+'x':'—'}</td></tr>
        <tr><td>Interest Coverage</td><td>${r.interestCoverageTTM?N(r.interestCoverageTTM)+'x':'—'}</td></tr>
        <tr><td>EPS (diluted)</td><td>${f.epsdiluted?'$'+N(f.epsdiluted):'—'}</td></tr>
        <tr><td>EBITDA</td><td>${NL(f.ebitda)}</td></tr>
      </table>
    </div>`;
}
function mc(l,v,s){return `<div class="mcard"><div class="mcard-l">${l}</div><div class="mcard-v">${v}</div>${s?`<div class="mcard-s">${s}</div>`:''}</div>`;}

// ── FINANCIALS ────────────────────────────────────────────────────────────
function renderFinancials(d) {
  const fins=d.financials||[];
  if(!fins.length){noData('p-financials','Financial Modeling Prep');return;}
  const f=fins[0],pf=fins[1];
  const rg=pf?((f.revenue-pf.revenue)/Math.abs(pf.revenue)*100):null;
  const ng=pf&&pf.netIncome?((f.netIncome-pf.netIncome)/Math.abs(pf.netIncome)*100):null;
  document.getElementById('p-financials').innerHTML = `
    <div class="card">
      <div class="card-t">Income Statement — ${(f.date||'').slice(0,4)}</div>
      <table class="dt">
        <tr><td>Revenue</td><td>${NL(f.revenue)}</td></tr>
        <tr><td>Revenue Growth YoY</td><td class="${rg>0?'pos':'neg'}">${rg!=null?N(rg)+'%':'—'}</td></tr>
        <tr><td>Gross Profit</td><td class="pos">${NL(f.grossProfit)}</td></tr>
        <tr><td>Gross Margin</td><td>${f.grossProfitRatio?N(f.grossProfitRatio*100)+'%':'—'}</td></tr>
        <tr><td>Operating Income</td><td class="${f.operatingIncome>0?'pos':'neg'}">${NL(f.operatingIncome)}</td></tr>
        <tr><td>Operating Margin</td><td>${f.operatingIncomeRatio?N(f.operatingIncomeRatio*100)+'%':'—'}</td></tr>
        <tr><td>Net Income</td><td class="${f.netIncome>0?'pos':'neg'}">${NL(f.netIncome)}</td></tr>
        <tr><td>Net Margin</td><td>${f.netIncomeRatio?N(f.netIncomeRatio*100)+'%':'—'}</td></tr>
        <tr><td>EPS (diluted)</td><td>${f.epsdiluted?'$'+N(f.epsdiluted):'—'}</td></tr>
        <tr><td>EBITDA</td><td>${NL(f.ebitda)}</td></tr>
        <tr><td>R&D Expenses</td><td>${NL(f.researchAndDevelopmentExpenses)}</td></tr>
      </table>
    </div>
    <div class="card">
      <div class="card-t">4-Year Revenue & Net Income Trend</div>
      ${fins.slice(0,4).reverse().map(y=>{
        const maxRev=Math.max(...fins.map(x=>x.revenue||0));
        const pct=maxRev?Math.max((y.revenue||0)/maxRev*100,2):2;
        return `<div class="tbar-wrap">
          <div class="tbar-labels"><span style="color:var(--tx2)">${(y.date||'').slice(0,4)}</span><span>${NL(y.revenue)} rev &nbsp;·&nbsp; <span class="${y.netIncome>0?'pos':'neg'}">${NL(y.netIncome)} net</span></span></div>
          <div class="tbar"><div class="tbar-fill" style="width:${pct}%;background:var(--g);"></div></div>
        </div>`;}).join('')}
    </div>`;
}

// ── BALANCE SHEET ─────────────────────────────────────────────────────────
function renderBalance(d) {
  const bs=d.balance||[];
  if(!bs.length){noData('p-balance','Financial Modeling Prep');return;}
  const b=bs[0];
  const d2e=b.totalStockholdersEquity?(b.totalDebt/b.totalStockholdersEquity):null;
  const cr=b.totalCurrentLiabilities?(b.totalCurrentAssets/b.totalCurrentLiabilities):null;
  document.getElementById('p-balance').innerHTML = `
    <div class="g2">
      <div class="card">
        <div class="card-t">Assets</div>
        <table class="dt">
          <tr><td>Cash & Equivalents</td><td class="pos">${NL(b.cashAndCashEquivalents)}</td></tr>
          <tr><td>Short-term Investments</td><td>${NL(b.shortTermInvestments)}</td></tr>
          <tr><td>Net Receivables</td><td>${NL(b.netReceivables)}</td></tr>
          <tr><td>Total Current Assets</td><td>${NL(b.totalCurrentAssets)}</td></tr>
          <tr><td>PP&E (net)</td><td>${NL(b.propertyPlantEquipmentNet)}</td></tr>
          <tr><td>Goodwill</td><td>${NL(b.goodwill)}</td></tr>
          <tr><td>Total Assets</td><td style="font-weight:600">${NL(b.totalAssets)}</td></tr>
        </table>
      </div>
      <div class="card">
        <div class="card-t">Liabilities & Equity</div>
        <table class="dt">
          <tr><td>Accounts Payable</td><td class="neg">${NL(b.accountPayables)}</td></tr>
          <tr><td>Short-term Debt</td><td class="neg">${NL(b.shortTermDebt)}</td></tr>
          <tr><td>Total Current Liabilities</td><td class="neg">${NL(b.totalCurrentLiabilities)}</td></tr>
          <tr><td>Long-term Debt</td><td class="neg">${NL(b.longTermDebt)}</td></tr>
          <tr><td>Total Debt</td><td class="neg" style="font-weight:600">${NL(b.totalDebt)}</td></tr>
          <tr><td>Retained Earnings</td><td class="${b.retainedEarnings>0?'pos':'neg'}">${NL(b.retainedEarnings)}</td></tr>
          <tr><td>Stockholders' Equity</td><td class="pos" style="font-weight:600">${NL(b.totalStockholdersEquity)}</td></tr>
        </table>
      </div>
    </div>
    <div class="g3" style="margin-top:14px;">
      ${mc('Debt / Equity',d2e!=null?N(d2e)+'x':'—',d2e!=null?(d2e<1?'Conservative':d2e<2?'Moderate':'High leverage'):'')}
      ${mc('Current Ratio',cr!=null?N(cr)+'x':'—',cr!=null?(cr>1.5?'Healthy':cr>1?'Adequate':'Tight'):'')}
      ${mc('Cash on Hand',NL(b.cashAndCashEquivalents),'')}
    </div>`;
}

// ── CASH FLOW ─────────────────────────────────────────────────────────────
function renderCashflow(d) {
  const cfs=d.cashflow||[];
  if(!cfs.length){noData('p-cashflow','Financial Modeling Prep');return;}
  const cf=cfs[0];
  document.getElementById('p-cashflow').innerHTML = `
    <div class="card">
      <div class="card-t">Cash Flow Statement — ${(cf.date||'').slice(0,4)}</div>
      <table class="dt">
        <tr><td>Operating Cash Flow</td><td class="${cf.operatingCashFlow>0?'pos':'neg'}" style="font-weight:600">${NL(cf.operatingCashFlow)}</td></tr>
        <tr><td>Capital Expenditure</td><td class="neg">${NL(cf.capitalExpenditure)}</td></tr>
        <tr><td>Free Cash Flow</td><td class="${cf.freeCashFlow>0?'pos':'neg'}" style="font-weight:700">${NL(cf.freeCashFlow)}</td></tr>
        <tr><td>Acquisitions (net)</td><td>${NL(cf.acquisitionsNet)}</td></tr>
        <tr><td>Stock Buybacks</td><td>${NL(cf.commonStockRepurchased)}</td></tr>
        <tr><td>Dividends Paid</td><td>${NL(cf.dividendsPaid)}</td></tr>
        <tr><td>Net Change in Cash</td><td class="${cf.netChangeInCash>0?'pos':'neg'}">${NL(cf.netChangeInCash)}</td></tr>
      </table>
    </div>
    ${cfs.length>1?`<div class="card">
      <div class="card-t">Free Cash Flow Trend</div>
      ${cfs.slice(0,3).reverse().map(c=>{
        const maxFCF=Math.max(...cfs.map(x=>Math.abs(x.freeCashFlow||0)));
        const pct=maxFCF?Math.abs((c.freeCashFlow||0))/maxFCF*100:2;
        return `<div class="tbar-wrap">
          <div class="tbar-labels"><span style="color:var(--tx2)">${(c.date||'').slice(0,4)}</span><span class="${c.freeCashFlow>0?'pos':'neg'}">FCF: ${NL(c.freeCashFlow)}</span></div>
          <div class="tbar"><div class="tbar-fill" style="width:${Math.max(pct,2)}%;background:${c.freeCashFlow>0?'var(--g)':'var(--r)'};"></div></div>
        </div>`;}).join('')}
    </div>`:''}`;
}

// ── TECHNICALS ────────────────────────────────────────────────────────────
function renderTechnicals(d) {
  const tech=d.technicals||{};
  let rsi=null,macd=null,sig=null,sma50=null,sma200=null;
  try{const k=Object.keys(tech.rsi?.['Technical Analysis: RSI']||{});if(k.length)rsi=parseFloat(tech.rsi['Technical Analysis: RSI'][k[0]]['RSI']);}catch(e){}
  try{const k=Object.keys(tech.macd?.['Technical Analysis: MACD']||{});if(k.length){macd=parseFloat(tech.macd['Technical Analysis: MACD'][k[0]]['MACD']);sig=parseFloat(tech.macd['Technical Analysis: MACD'][k[0]]['MACD_Signal']);}}catch(e){}
  try{const k=Object.keys(tech.sma50?.['Technical Analysis: SMA']||{});if(k.length)sma50=parseFloat(tech.sma50['Technical Analysis: SMA'][k[0]]['SMA']);}catch(e){}
  try{const k=Object.keys(tech.sma200?.['Technical Analysis: SMA']||{});if(k.length)sma200=parseFloat(tech.sma200['Technical Analysis: SMA'][k[0]]['SMA']);}catch(e){}
  const cp=d.quote?.price;
  document.getElementById('p-technicals').innerHTML = `
    <div class="g4" style="margin-bottom:14px;">
      <div class="mcard">
        <div class="mcard-l">RSI (14)</div>
        <div class="mcard-v">${rsi?N(rsi):'—'}</div>
        <div class="mcard-s ${rsi?(rsi<30?'sig-buy':rsi>70?'sig-sell':'sig-neu'):''}">
          ${rsi?(rsi<30?'OVERSOLD':rsi>70?'OVERBOUGHT':'NEUTRAL'):'No data'}</div>
      </div>
      <div class="mcard">
        <div class="mcard-l">MACD</div>
        <div class="mcard-v">${macd?N(macd):'—'}</div>
        <div class="mcard-s ${(macd&&sig)?(macd>sig?'sig-buy':'sig-sell'):''}">
          ${(macd&&sig)?(macd>sig?'BULLISH CROSS':'BEARISH CROSS'):'No data'}</div>
      </div>
      <div class="mcard">
        <div class="mcard-l">50-Day SMA</div>
        <div class="mcard-v">${sma50?'$'+N(sma50):'—'}</div>
        <div class="mcard-s ${cp&&sma50?(cp>sma50?'sig-buy':'sig-sell'):''}">
          ${cp&&sma50?(cp>sma50?'Price above — Bullish':'Price below — Bearish'):'—'}</div>
      </div>
      <div class="mcard">
        <div class="mcard-l">200-Day SMA</div>
        <div class="mcard-v">${sma200?'$'+N(sma200):'—'}</div>
        <div class="mcard-s ${cp&&sma200?(cp>sma200?'sig-buy':'sig-sell'):''}">
          ${cp&&sma200?(cp>sma200?'Long-term uptrend':'Long-term downtrend'):'—'}</div>
      </div>
    </div>
    <div class="card">
      <div class="card-t">Signal Interpretation</div>
      <div style="font-size:12px;color:var(--tx2);line-height:1.9;">
        ${rsi?`<b style="color:var(--tx)">RSI ${N(rsi)}:</b> ${rsi<30?'Deeply oversold — historically a buying opportunity. Market may be overcorrecting.':rsi>70?'Overbought — momentum stretched. Watch for reversal.':rsi<45?'Mildly bearish momentum.':'Neutral to bullish momentum.'}<br>`:''}
        ${(macd&&sig)?`<b style="color:var(--tx)">MACD:</b> ${macd>sig?'Bullish crossover — upward momentum building.':'Bearish crossover — downward pressure present.'}<br>`:''}
        ${(cp&&sma50)?`<b style="color:var(--tx)">50 SMA:</b> Price is ${cp>sma50?'above':'below'} the 50-day average — short-term trend is ${cp>sma50?'bullish':'bearish'}.<br>`:''}
        ${(cp&&sma200)?`<b style="color:var(--tx)">200 SMA:</b> ${cp>sma200?'Long-term uptrend intact.':'In long-term downtrend.'}`:''}
        ${!rsi&&!macd?'<span style="color:var(--tx3)">Add an Alpha Vantage key in Settings to enable technical indicators.</span>':''}
      </div>
    </div>`;
}

// ── NEWS ──────────────────────────────────────────────────────────────────
function renderNews(d) {
  const articles=d.news||[];
  if(!articles.length){noData('p-news','News API');return;}
  const pos=['surge','rally','beat','gain','profit','upgrade','record','growth','buy','strong','rise','soar'];
  const neg=['fall','drop','loss','miss','downgrade','sell','weak','decline','crash','layoff','warn','cut','slump'];
  document.getElementById('p-news').innerHTML = articles.map(a=>{
    const t=a.title||'';const l=t.toLowerCase();
    const p=pos.filter(w=>l.includes(w)).length;const n=neg.filter(w=>l.includes(w)).length;
    const s=p>n?'bull':n>p?'bear':'neu';
    return `<div class="ni">
      <div class="ni-t">${t}</div>
      <div class="ni-m">
        <span>${a.source?.name||''}</span>
        <span>${(a.publishedAt||'').slice(0,10)}</span>
        <span class="badge b-${s}">${s==='bull'?'BULLISH':s==='bear'?'BEARISH':'NEUTRAL'}</span>
      </div>
    </div>`;}).join('');
}

// ── AI ANALYSIS ───────────────────────────────────────────────────────────
async function runAI() {
  document.getElementById('ai-btn').disabled=true;
  document.getElementById('ai-btn').textContent='ANALYZING…';
  document.getElementById('ai-body').innerHTML='<div class="loading"><span class="spin"></span>Claude is reading all data…</div>';
  try {
    const r=await fetch(`${API}/api/ai-analyze`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ticker,data:stockData})});
    const res=await r.json();
    renderAI(res);
  } catch(e) {
    document.getElementById('ai-body').innerHTML=`<div style="color:var(--r);font-size:12px;padding:20px;">Error: ${e.message}</div>`;
  }
  document.getElementById('ai-btn').disabled=false;
  document.getElementById('ai-btn').textContent='ANALYZE WITH AI';
}

function renderAI(res) {
  const text=res.text||'';const verdict=res.verdict||'';
  const buy=/buy|bullish/i.test(verdict);const sell=/sell|reduce|avoid/i.test(verdict);
  const vc=buy?'vb-buy':sell?'vb-sell':'vb-hold';
  const vrc=buy?'vr-buy':sell?'vr-sell':'vr-hold';
  document.getElementById('ai-body').innerHTML=`
    ${verdict?`<div class="verdict-box ${vc}">
      <div style="font-size:9px;color:var(--tx2);letter-spacing:.1em;margin-bottom:5px;">AI VERDICT · ${ticker}</div>
      <div class="vr ${vrc}">${verdict}</div>
    </div>`:''}
    <div class="ai-section"><div class="ai-st">Full Analysis</div><div class="ai-tx">${text}</div></div>
    <button class="wl-add-btn" onclick="quickAddWL('${ticker}')">+ Add ${ticker} to Watchlist</button>
    <div style="margin-top:12px;font-size:10px;color:var(--tx3);line-height:1.6;border-top:1px solid var(--b1);padding-top:10px;">
      Sources: TradingView · FMP · Alpha Vantage · News API · Claude AI<br>Research only. Not financial advice.
    </div>`;
}

// ── WATCHLIST ─────────────────────────────────────────────────────────────
async function loadWatchlistSidebar() {
  try {
    const r=await fetch(`${API}/api/watchlist`);const list=await r.json();
    const el=document.getElementById('wl-sb');
    if(!list.length){el.innerHTML='<div style="font-size:11px;color:var(--tx3);">Empty</div>';return;}
    el.innerHTML=list.map(w=>`<div class="wl-row">
      <span class="wl-t" onclick="go('${w.ticker}')">${w.ticker}</span>
      <button class="wl-x" onclick="delWL('${w.ticker}')">✕</button>
    </div>`).join('');
  } catch(e){}
}

async function loadWatchlistMain() {
  try {
    const r=await fetch(`${API}/api/watchlist`);const list=await r.json();
    const el=document.getElementById('wl-main');
    if(!list.length){el.innerHTML='<div class="empty"><div class="empty-icon">◈</div>No stocks on watchlist yet.</div>';return;}
    el.innerHTML=`<table class="ptbl"><thead><tr>
      <th>Ticker</th><th>Company</th><th>Target Price</th><th>Notes</th><th>Added</th><th></th>
    </tr></thead><tbody>${list.map(w=>`<tr>
      <td style="font-weight:700;cursor:pointer;color:var(--g);" onclick="go('${w.ticker}')">${w.ticker}</td>
      <td style="color:var(--tx2)">${w.company_name||'—'}</td>
      <td>${w.target_price?'$'+N(w.target_price):'—'}</td>
      <td style="color:var(--tx2);max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${w.notes||'—'}</td>
      <td style="color:var(--tx3)">${(w.added_at||'').slice(0,10)}</td>
      <td><button class="btn btn-out" style="font-size:10px;padding:3px 8px;" onclick="delWL('${w.ticker}')">Remove</button></td>
    </tr>`).join('')}</tbody></table>`;
  } catch(e){}
}

async function addWatchlist() {
  const t=document.getElementById('wl-ticker').value.trim().toUpperCase();if(!t)return;
  await fetch(`${API}/api/watchlist`,{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({ticker:t,company_name:stockData.quote?.name||'',
      target_price:document.getElementById('wl-target').value||null,notes:document.getElementById('wl-notes').value})});
  closeModal('m-wl');await loadWatchlistSidebar();await refreshStats();
}

async function quickAddWL(t) {
  await fetch(`${API}/api/watchlist`,{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({ticker:t,company_name:stockData.quote?.name||''})});
  await loadWatchlistSidebar();await refreshStats();
}

async function delWL(t) {
  await fetch(`${API}/api/watchlist/${t}`,{method:'DELETE'});
  await loadWatchlistSidebar();await refreshStats();
  if(document.getElementById('view-watchlist').classList.contains('active'))loadWatchlistMain();
}

// ── PORTFOLIO ─────────────────────────────────────────────────────────────
async function loadPortfolio() {
  try {
    const r=await fetch(`${API}/api/portfolio`);const list=await r.json();
    const el=document.getElementById('port-body');
    if(!list.length){el.innerHTML='<div class="empty"><div class="empty-icon">▲</div>No positions yet. Add your first position.</div>';return;}
    const totalCost=list.reduce((s,p)=>s+(p.shares*p.avg_price),0);
    el.innerHTML=`
      <div class="g3" style="margin-bottom:16px;">
        ${mc('Total Positions',list.length,'')}
        ${mc('Total Cost Basis','$'+N(totalCost),'')}
        ${mc('Unique Tickers',[...new Set(list.map(p=>p.ticker))].length,'')}
      </div>
      <table class="ptbl"><thead><tr>
        <th>Ticker</th><th>Shares</th><th>Avg Price</th><th>Cost Basis</th><th>Notes</th><th>Date</th><th></th>
      </tr></thead><tbody>${list.map(p=>`<tr>
        <td style="font-weight:700;cursor:pointer;color:var(--g);" onclick="go('${p.ticker}')">${p.ticker}</td>
        <td>${N(p.shares)}</td>
        <td>$${N(p.avg_price)}</td>
        <td style="font-weight:500;">$${N(p.shares*p.avg_price)}</td>
        <td style="color:var(--tx2);max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${p.notes||'—'}</td>
        <td style="color:var(--tx3)">${(p.bought_at||'').slice(0,10)}</td>
        <td><button class="btn btn-out" style="font-size:10px;padding:3px 8px;color:var(--r);" onclick="delPos(${p.id})">✕</button></td>
      </tr>`).join('')}</tbody></table>`;
  } catch(e){}
}

async function addPosition() {
  await fetch(`${API}/api/portfolio`,{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({ticker:document.getElementById('pos-t').value.trim().toUpperCase(),
      shares:parseFloat(document.getElementById('pos-s').value),
      avg_price:parseFloat(document.getElementById('pos-p').value),
      notes:document.getElementById('pos-n').value})});
  closeModal('m-pos');await loadPortfolio();await refreshStats();
}

async function delPos(id) {
  await fetch(`${API}/api/portfolio/${id}`,{method:'DELETE'});
  await loadPortfolio();await refreshStats();
}

// ── HISTORY ───────────────────────────────────────────────────────────────
async function loadHistory() {
  try {
    const r=await fetch(`${API}/api/history`);const list=await r.json();
    const el=document.getElementById('hist-body');
    if(!list.length){el.innerHTML='<div class="empty"><div class="empty-icon">◉</div>No analyses yet.</div>';return;}
    el.innerHTML=list.map(a=>`<div class="hi">
      <span class="hi-t" onclick="go('${a.ticker}')">${a.ticker}</span>
      <span style="font-size:11px;color:var(--tx2)">${a.company_name||'—'} ${a.price?'· $'+N(a.price):''} ${a.ai_verdict?'<span style="color:var(--g)">· '+a.ai_verdict+'</span>':''}</span>
      <span style="font-size:10px;color:var(--tx3)">${(a.created_at||'').slice(0,16)}</span>
    </div>`).join('');
  } catch(e){}
}

// ── NOTES ─────────────────────────────────────────────────────────────────
async function loadNotes() {
  const el=document.getElementById('notes-body');
  if(!ticker){el.innerHTML='<div class="empty"><div class="empty-icon">◫</div>Analyze a stock first, then add notes.</div>';return;}
  try {
    const r=await fetch(`${API}/api/notes/${ticker}`);const notes=await r.json();
    document.getElementById('note-ticker-lbl').textContent=ticker;
    if(!notes.length){el.innerHTML=`<div class="empty"><div class="empty-icon">◫</div>No notes for ${ticker} yet.<br>Click "+ Add Note" to start.</div>`;return;}
    el.innerHTML=notes.map(n=>`<div class="nc">
      <div class="nc-tk">${n.ticker}</div>
      <div class="nc-body">${n.content}</div>
      <div class="nc-foot">
        <span>${(n.created_at||'').slice(0,16)}</span>
        <span style="cursor:pointer;color:var(--r);" onclick="delNote(${n.id})">Delete</span>
      </div>
    </div>`).join('');
  } catch(e){}
}

async function saveNote() {
  const content=document.getElementById('note-content').value.trim();if(!content)return;
  await fetch(`${API}/api/notes`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ticker,content})});
  closeModal('m-note');loadNotes();
}

async function delNote(id) {
  await fetch(`${API}/api/notes/${id}`,{method:'DELETE'});loadNotes();
}

// ── NAVIGATION ────────────────────────────────────────────────────────────
function showView(name) {
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('view-'+name)?.classList.add('active');
  document.getElementById('nav-'+name)?.classList.add('active');
  if(name==='watchlist')loadWatchlistMain();
  if(name==='portfolio')loadPortfolio();
  if(name==='history')loadHistory();
  if(name==='notes')loadNotes();
}

function switchTab(name) {
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  const names=['chart','overview','financials','balance','cashflow','technicals','news'];
  document.querySelectorAll('.tab')[names.indexOf(name)]?.classList.add('active');
  const panel=document.getElementById('p-'+name);
  if(panel){panel.classList.add('active');}
}

function go(t) {
  document.getElementById('ticker-inp').value=t;
  showView('analyzer');
  analyze();
}

function openModal(id){document.getElementById(id).classList.add('open');}
function closeModal(id){document.getElementById(id).classList.remove('open');}

// ── UTILS ─────────────────────────────────────────────────────────────────
function N(n){if(n==null||isNaN(n))return '—';return parseFloat(n).toLocaleString('en-US',{maximumFractionDigits:2});}
function NL(n){
  if(!n||isNaN(n))return '—';
  const a=Math.abs(n),s=n<0?'-':'';
  if(a>=1e12)return s+'$'+(a/1e12).toFixed(2)+'T';
  if(a>=1e9)return s+'$'+(a/1e9).toFixed(2)+'B';
  if(a>=1e6)return s+'$'+(a/1e6).toFixed(1)+'M';
  if(a>=1e3)return s+'$'+(a/1e3).toFixed(1)+'K';
  return s+'$'+a.toFixed(0);
}
function noData(id,src){
  document.getElementById(id).innerHTML=`<div style="font-size:12px;color:var(--tx3);padding:16px;background:var(--bg3);border-radius:var(--rad);border:1px solid var(--b1);">
    No data available — add a <b style="color:var(--tx2)">${src}</b> API key in Settings.
  </div>`;
}

// ── START ─────────────────────────────────────────────────────────────────
init();
</script>
</body>
</html>
