import re, sys, io, os

SRC = "/sessions/optimistic-vigilant-turing/mnt/Blood test/blood-tests-dashboard/catalogue.html"
DST = "/sessions/optimistic-vigilant-turing/mnt/Blood test/blood-tests-dashboard/index-v2.html"

s = io.open(SRC, encoding="utf8").read()
orig_len = len(s)
applied = []

def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    assert n == count, "MATCH FAIL [%s]: found %d, expected %d" % (label, n, count)
    s = s.replace(old, new)
    applied.append(label)

# ---------------------------------------------------------------- grab the figure SVG
m = re.search(r'<svg class="cxfig".*?</svg>', s, re.S)
assert m, "figure svg not found"
FIG = m.group(0)

# ================================================================ E0: title
rep('<title>What is your blood trying to tell you? — dashboard</title>',
    '<title>What is your blood telling you? — an atlas of blood</title>',
    'E0 title')

# ================================================================ E1: CSS
V2CSS = r"""
/* ==================== v2 — atlas landing, gap map, family atlas ==================== */
#cxRoute .cxwrap{min-height:0;display:block;max-width:1180px;padding:20px 24px 70px;}
#cxRoute .cxhero{text-align:left;font-size:32px;line-height:1.26;margin:10px 0 10px;}
#cxRoute .cxherosub{text-align:left;margin:0 0 2px;max-width:640px;}
.v2num{color:var(--accent);}
.v2hero{display:grid;grid-template-columns:1fr 200px;gap:24px;align-items:center;}
.v2hero .cxfig{width:100%;max-height:260px;}
#cxRoute .cxecg{margin:12px 0 0;width:min(430px,80%);}
@media(max-width:860px){.v2hero{grid-template-columns:1fr;}.v2hero .cxfig{max-width:170px;margin:0 auto;}}

.v2stats{display:flex;gap:30px;flex-wrap:wrap;margin:20px 0 6px;padding:15px 0;
 border-top:1px solid var(--line);border-bottom:1px solid var(--line);}
.v2stat{max-width:250px;}
.v2stat b{font-family:var(--font-serif);font-size:25px;font-weight:700;display:block;line-height:1.1;color:var(--accent);}
.v2stat b i{font-style:normal;font-size:14px;color:var(--dim);}
.v2stat.b b{color:var(--teal);}.v2stat.c b{color:var(--warn);}
.v2stat span{font-size:12.5px;color:var(--muted);display:block;margin-top:3px;}

.v2routes{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;max-width:none;margin:22px 0 0;align-items:stretch;}
@media(max-width:860px){.v2routes{grid-template-columns:1fr;}}
.v2routes .cxroute{padding:20px 20px 17px;gap:7px;}
.v2routes .cxroute h3{font-size:19px;}
.v2routes .cxroute .arr{margin-top:auto;padding-top:6px;}
.v2routes .cxroute .ic2{width:32px;height:32px;}
.v2flag{position:absolute;top:13px;right:13px;font-family:var(--font-mono);font-size:9px;
 letter-spacing:.06em;color:#fff;background:var(--accent);padding:2px 7px;border-radius:8px;}
.v2gapbar{display:flex;height:9px;border-radius:5px;overflow:hidden;border:1px solid var(--line);margin:5px 0 1px;background:#fff;}
.v2gapbar i{display:block;height:100%;}
.v2gapkey{font-family:var(--font-mono);font-size:9.5px;color:var(--dim);display:flex;gap:11px;flex-wrap:wrap;}
.v2blocked{background:repeating-linear-gradient(45deg,#fff,#fff 6px,#eef2f2 6px,#eef2f2 12px);}

.v2band{margin:34px 0 0;}
.v2band h2{font-family:var(--font-serif);font-size:20px;color:var(--slate);margin:0 0 3px;}
.v2band .sub{font-size:13px;color:var(--muted);margin:0 0 12px;max-width:720px;}
.v2q{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}
@media(max-width:860px){.v2q{grid-template-columns:1fr;}}
.v2qc{background:#fff;border:1px solid var(--line);border-radius:11px;padding:13px 14px;}
.v2qc h4{font-family:var(--font-serif);font-size:15px;color:var(--slate);margin:0 0 4px;}
.v2qc p{font-size:11.5px;color:var(--muted);margin:0;line-height:1.5;}
.v2pill{display:inline-block;font-family:var(--font-mono);font-size:9px;letter-spacing:.05em;
 text-transform:uppercase;padding:2px 7px;border-radius:9px;margin-top:8px;}
.v2pill.ok{background:#e3f2ea;color:var(--ok);}
.v2pill.proto{background:#fdf1ea;color:var(--accent);}
.v2pill.part{background:#fbf3e0;color:var(--warn);}
.v2pill.no{background:#f0f3f3;color:var(--dim);}

.v2mapwrap{background:#fff;border:1px solid var(--line);border-radius:13px;padding:8px 10px 10px;}
.v2mapwrap svg{width:100%;height:auto;display:block;}
.v2mapleg{display:flex;gap:16px;flex-wrap:wrap;font-size:11.5px;color:var(--muted);padding:2px 4px 6px;}
.v2mapleg i{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:5px;vertical-align:-1px;}
.v2famleg{display:flex;flex-wrap:wrap;gap:4px 14px;padding:8px 4px 2px;border-top:1px solid var(--line);margin-top:6px;}
.v2famleg span{font-size:11px;color:var(--muted);white-space:nowrap;}
.v2famleg b{font-family:var(--font-mono);font-size:10px;color:var(--dim);font-weight:400;}
.v2famleg i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px;vertical-align:0;}
.v2mapnote{font-size:12px;color:var(--muted);margin:10px 0 0;max-width:760px;}
.v2mapnote b{color:var(--accent);}
.v2fam-t{font-family:var(--font-sans);font-size:8.5px;fill:var(--muted);}
.v2fam-n{font-family:var(--font-mono);font-size:8px;fill:var(--dim);}

.v2honest{background:#fff;border:1px solid var(--line);border-left:3px solid var(--teal);
 border-radius:9px;padding:14px 16px;font-size:12.5px;color:var(--muted);margin:30px 0 0;}
.v2honest h4{font-family:var(--font-serif);font-size:15px;color:var(--slate);margin:0 0 5px;}
.v2covbar{display:flex;height:11px;border-radius:6px;overflow:hidden;margin:9px 0 8px;border:1px solid var(--line);}

/* ---------- scrolling screen chrome (gap map) ---------- */
#cxGaps{position:fixed;inset:0;overflow-y:auto;background:var(--paper);z-index:40;display:none;}
#cxGaps.cx-on{display:block;}
#cxGaps .cxwrap{max-width:1120px;margin:0 auto;padding:22px 24px 90px;}
#cxGaps .cxtop{display:flex;align-items:center;gap:14px;border-bottom:1px solid var(--line);
 padding:12px 24px;background:var(--panel);position:sticky;top:0;z-index:3;}
#cxGaps .cxtop .logo{font-family:var(--font-serif);font-size:19px;color:var(--slate);font-weight:700;}
#cxGaps .cxtop .logo b{color:var(--teal);}
#cxGaps .cxtop .tag{font-family:var(--font-mono);font-size:10.5px;color:var(--muted);letter-spacing:.04em;}
#cxGaps h1{font-family:var(--font-serif);font-size:26px;color:var(--slate);margin:12px 0 4px;}
#cxGaps .lead{font-size:14px;color:var(--muted);margin:0 0 18px;max-width:720px;}
.v2sec{margin:26px 0 0;}
.v2sec h2{font-family:var(--font-serif);font-size:19px;color:var(--slate);margin:0 0 3px;}
.v2sec .sub{font-size:12.5px;color:var(--muted);margin:0 0 12px;max-width:760px;}
.v2tools{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:0 0 12px;}
.v2tool{border:1px solid var(--line);background:#fff;color:var(--slate);font-size:12px;font-weight:600;
 padding:5px 12px;border-radius:16px;cursor:pointer;font-family:var(--font-sans);}
.v2tool:hover{border-color:var(--teal);color:var(--teal);}
.v2tool.on{background:var(--teal);border-color:var(--teal);color:#fff;}
.v2tools .lab{font-family:var(--font-mono);font-size:10px;letter-spacing:.05em;color:var(--dim);text-transform:uppercase;margin-right:2px;}

/* ==================== ATLAS COCKPIT — fixed, nothing reflows ====================
   The stage never scrolls and no panel ever changes size. Panels are absolutely
   positioned against the stage; anything that could overflow scrolls inside its
   own box. The map packs once per stage size and only re-paints on shade change,
   so circles never jump. */
#cxAtlas{position:fixed;inset:0;background:var(--paper);z-index:40;display:none;overflow:hidden;}
#cxAtlas.cx-on{display:block;}
.atl-top{position:absolute;top:0;left:0;right:0;height:53px;display:flex;align-items:center;gap:14px;
 padding:0 20px;background:var(--panel);border-bottom:1px solid var(--line);z-index:6;}
.atl-top .logo{font-family:var(--font-serif);font-size:18px;color:var(--slate);font-weight:700;}
.atl-top .logo b{color:var(--teal);}
.atl-top .tag{font-family:var(--font-mono);font-size:10.5px;color:var(--muted);letter-spacing:.04em;}
.atl-top .sp{flex:1;}
.atl-hdrstat{font-family:var(--font-mono);font-size:10.5px;color:var(--dim);white-space:nowrap;}
@media(max-width:820px){.atl-hdrstat{display:none;}}

.atl-stage{position:absolute;top:53px;left:0;right:0;bottom:0;overflow:hidden;}
.atl-map{position:absolute;inset:0;width:100%;height:100%;display:block;}
.atl-map circle{transition:stroke-width .12s,filter .12s;cursor:pointer;}
.atl-map .fam-t{font-family:var(--font-sans);font-size:10px;fill:var(--muted);pointer-events:none;}
.atl-map .fam-n{font-family:var(--font-mono);font-size:9px;fill:var(--dim);pointer-events:none;}
.atl-map g.lit .fam-t{fill:var(--slate);}
.atl-map g.lit .fam-n{fill:var(--teal);}
.atl-map g.hot circle{stroke-width:3.4;filter:drop-shadow(0 3px 9px rgba(12,30,36,.22));}
.atl-map g.sel circle{stroke:var(--accent)!important;stroke-width:3.4;stroke-dasharray:none!important;}
.atl-map g.sel .fam-t,.atl-map g.sel .fam-n{fill:var(--accent);}

/* --- shared panel shell: glass, fixed, never resizes --- */
.atl-panel{position:absolute;background:rgba(255,255,255,.9);border:1px solid var(--line);
 border-radius:14px;box-shadow:0 12px 34px rgba(12,30,36,.11);z-index:3;
 -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);display:flex;flex-direction:column;}
.atl-panel header{flex:0 0 auto;padding:11px 15px 9px;border-bottom:1px solid var(--line);
 font-family:var(--font-mono);font-size:10px;letter-spacing:.07em;text-transform:uppercase;color:var(--dim);
 display:flex;align-items:center;gap:8px;}
.atl-panel header b{font-family:var(--font-mono);color:var(--slate);font-weight:600;}
.atl-panel header .sp{flex:1;}

/* --- left column: controls above, family index filling the rest --- */
.atl-left{position:absolute;top:16px;left:16px;bottom:110px;width:302px;
 display:flex;flex-direction:column;gap:12px;z-index:3;}
.atl-ctl{position:relative;flex:0 0 auto;padding:15px 16px 14px;}
.atl-ctl h1{font-family:var(--font-serif);font-size:20px;color:var(--slate);margin:0 0 4px;line-height:1.25;}
.atl-ctl p{font-size:11.5px;color:var(--muted);margin:0 0 11px;line-height:1.5;}
.atl-row{display:flex;align-items:center;gap:9px;margin-top:7px;}
.atl-lab{font-family:var(--font-mono);font-size:9px;letter-spacing:.06em;text-transform:uppercase;
 color:var(--dim);width:42px;flex:0 0 auto;}
.atl-seg{display:flex;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff;flex:1;}
.atl-seg button{flex:1;border:none;background:none;font-family:var(--font-sans);font-size:10.5px;
 font-weight:600;color:var(--muted);padding:5px 4px;white-space:nowrap;border-right:1px solid var(--line);}
.atl-seg button:last-child{border-right:none;}
.atl-seg button:hover{color:var(--teal);background:var(--aqua);}
.atl-seg button.on{background:var(--teal);color:#fff;}

.atl-index{position:relative;flex:1 1 auto;min-height:0;}
.atl-idxscroll{flex:1 1 auto;min-height:0;overflow-y:auto;padding:5px;}
.atl-idxscroll::-webkit-scrollbar{width:7px;}
.atl-idxscroll::-webkit-scrollbar-thumb{background:var(--line);border-radius:7px;}
.atl-ir{display:grid;grid-template-columns:1fr 54px;gap:7px;align-items:center;width:100%;
 height:34px;padding:0 9px;border:1px solid transparent;border-radius:8px;background:none;
 text-align:left;font-family:inherit;cursor:pointer;}
.atl-ir:hover{background:var(--aqua);}
.atl-ir.hot{background:var(--aqua);border-color:var(--teal);}
.atl-ir.sel{background:#fdf1ea;border-color:var(--accent);}
.atl-ir .n{font-size:12px;color:var(--slate);font-weight:600;white-space:nowrap;overflow:hidden;
 text-overflow:ellipsis;}
.atl-ir.sel .n{color:var(--accent);}
.atl-ir .b{display:flex;height:7px;border-radius:4px;overflow:hidden;border:1px solid var(--line);background:#fff;}
.atl-ir .b i{display:block;height:100%;}

/* --- right column: detail, always mounted at a fixed size --- */
.atl-detail{top:16px;right:16px;bottom:110px;width:330px;}
.atl-dbody{flex:1 1 auto;min-height:0;overflow-y:auto;padding:15px 16px 14px;}
.atl-dbody::-webkit-scrollbar{width:7px;}
.atl-dbody::-webkit-scrollbar-thumb{background:var(--line);border-radius:7px;}
.atl-dt{font-family:var(--font-serif);font-size:19px;color:var(--slate);margin:0 0 2px;line-height:1.24;}
.atl-dsub{font-family:var(--font-mono);font-size:10.5px;color:var(--dim);margin:0 0 13px;}
.atl-big{font-family:var(--font-serif);font-size:33px;font-weight:700;color:var(--teal);line-height:1;}
.atl-big small{font-family:var(--font-sans);font-size:12px;color:var(--muted);font-weight:400;margin-left:5px;}
.atl-cov{margin:15px 0 0;}
.atl-cov .k{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.05em;text-transform:uppercase;
 color:var(--dim);display:flex;justify-content:space-between;gap:8px;margin-bottom:4px;}
.atl-cov .k b{color:var(--slate);font-weight:600;}
.atl-cov .k b.zero{color:var(--accent);}
.atl-cov .bar{display:flex;height:9px;border-radius:5px;overflow:hidden;border:1px solid var(--line);background:#fff;}
.atl-cov .bar i{display:block;height:100%;}
.atl-samp{margin:16px 0 0;border-top:1px solid var(--line);padding-top:11px;}
.atl-samp .h{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.05em;text-transform:uppercase;
 color:var(--dim);margin:0 0 7px;}
.atl-samp li{font-size:11.5px;color:var(--muted);list-style:none;padding:2px 0;white-space:nowrap;
 overflow:hidden;text-overflow:ellipsis;}
.atl-samp ul{margin:0;padding:0;}
.atl-acts{flex:0 0 auto;padding:11px 15px 13px;border-top:1px solid var(--line);display:flex;
 flex-direction:column;gap:7px;}
.atl-btn{border:1px solid var(--teal);background:var(--teal);color:#fff;font-family:inherit;font-size:12px;
 font-weight:700;padding:8px 12px;border-radius:9px;width:100%;}
.atl-btn:hover{background:#005e6d;}
.atl-btn.ghost{background:#fff;color:var(--teal);}
.atl-btn.ghost:hover{background:var(--aqua);}
.atl-btn[disabled]{opacity:.4;cursor:default;background:#fff;color:var(--dim);border-color:var(--line);}
.atl-empty{font-size:12.5px;color:var(--muted);line-height:1.6;}
.atl-empty b{color:var(--slate);}

/* --- bottom bar: legend + the honesty line --- */
.atl-foot{left:16px;right:16px;bottom:16px;height:82px;flex-direction:row;align-items:center;
 gap:18px;padding:0 18px;}
.atl-leg{display:flex;gap:16px;flex-wrap:wrap;font-size:11.5px;color:var(--muted);flex:0 0 auto;}
.atl-leg i{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:5px;vertical-align:-1px;}
.atl-note{font-size:11.5px;color:var(--muted);margin:0;line-height:1.5;border-left:1px solid var(--line);
 padding-left:18px;flex:1;min-width:0;}
.atl-note b{color:var(--accent);}
@media(max-width:1180px){.atl-note{display:none;}}

/* --- overlay sheet: fades in, never pushes anything --- */
.atl-scrim{position:absolute;inset:0;background:rgba(24,44,50,.34);z-index:8;opacity:0;visibility:hidden;
 transition:opacity .2s;-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px);}
.atl-scrim.on{opacity:1;visibility:visible;}
.atl-sheet{position:absolute;top:16px;bottom:16px;right:16px;width:min(660px,calc(100% - 360px));
 background:var(--panel);border:1px solid var(--line);border-radius:14px;z-index:9;
 box-shadow:0 24px 60px rgba(12,30,36,.24);display:flex;flex-direction:column;
 opacity:0;visibility:hidden;transition:opacity .2s;}
.atl-sheet.on{opacity:1;visibility:visible;}
.atl-shhead{flex:0 0 auto;padding:15px 18px 12px;border-bottom:1px solid var(--line);}
.atl-shhead h2{font-family:var(--font-serif);font-size:20px;color:var(--slate);margin:0 0 2px;}
.atl-shhead p{font-family:var(--font-mono);font-size:10.5px;color:var(--dim);margin:0;}
.atl-shclose{position:absolute;top:13px;right:14px;width:28px;height:28px;border-radius:50%;
 border:1px solid var(--line);background:#fff;color:var(--muted);font-size:15px;line-height:1;}
.atl-shclose:hover{border-color:var(--accent);color:var(--accent);}
.atl-shtools{flex:0 0 auto;padding:11px 18px;border-bottom:1px solid var(--line);display:flex;gap:9px;align-items:center;}
.atl-shtools input{flex:1;padding:7px 13px;border:1px solid var(--line);border-radius:18px;font-size:12.5px;
 font-family:inherit;background:#fff;cursor:text;}
.atl-shtools input:focus{outline:none;border-color:var(--teal);box-shadow:0 0 0 3px rgba(0,115,133,.09);}
.atl-shcount{font-family:var(--font-mono);font-size:10px;color:var(--dim);white-space:nowrap;}
.atl-shlist{flex:1 1 auto;min-height:0;overflow-y:auto;padding:4px 0;}
.atl-shlist::-webkit-scrollbar{width:9px;}
.atl-shlist::-webkit-scrollbar-thumb{background:var(--line);border-radius:9px;}
.atl-mr{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;padding:9px 18px;
 border-bottom:1px solid #eef2f2;}
.atl-mr .mn{font-size:12.5px;color:var(--slate);line-height:1.35;}
.atl-mr .mn i{font-style:normal;font-family:var(--font-mono);font-size:10px;color:var(--dim);margin-left:6px;}
.atl-mr .mt{display:flex;gap:5px;flex-wrap:wrap;justify-content:flex-end;}
.atl-tg{font-family:var(--font-mono);font-size:8.5px;letter-spacing:.04em;text-transform:uppercase;
 padding:2px 7px;border-radius:9px;white-space:nowrap;}
.atl-tg.panel{background:var(--aqua);color:var(--teal);}
.atl-tg.q{background:#e3f2ea;color:var(--ok);}
.atl-tg.g{background:#f0f3f3;color:var(--dim);}
.atl-shfoot{flex:0 0 auto;padding:11px 18px;border-top:1px solid var(--line);display:flex;gap:9px;
 align-items:center;justify-content:space-between;}
.atl-shfoot span{font-size:11px;color:var(--dim);}
.atl-shfoot button{border:1px solid var(--teal);background:#fff;color:var(--teal);font-family:inherit;
 font-size:11.5px;font-weight:700;padding:6px 13px;border-radius:9px;white-space:nowrap;}
.atl-shfoot button:hover{background:var(--aqua);}

/* --- narrow fallback: the cockpit needs width; below this it stacks --- */
@media(max-width:1000px){
 .atl-left{width:250px;bottom:16px;}
 .atl-detail{display:none;}
 .atl-foot{display:none;}
 .atl-sheet{width:calc(100% - 32px);left:16px;right:16px;}
}

/* ---------- gap map ---------- */
.v2panels{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:11px;}
.v2pc{background:#fff;border:1px solid var(--line);border-radius:11px;padding:13px 14px;cursor:pointer;
 text-align:left;font-family:inherit;transition:.15s;display:flex;flex-direction:column;gap:4px;}
.v2pc:hover{border-color:var(--teal);}
.v2pc.on{border-color:var(--teal);background:var(--aqua);}
.v2pc .pn{font-family:var(--font-serif);font-size:15px;color:var(--slate);font-weight:700;}
.v2pc .pq{font-size:11.5px;color:var(--muted);line-height:1.45;}
.v2pc .pc{font-family:var(--font-mono);font-size:10px;color:var(--dim);}
.v2pc .pmark{font-family:var(--font-mono);font-size:10px;color:var(--teal);font-weight:600;}
.v2addwrap{position:relative;max-width:460px;margin:12px 0 8px;}
.v2add{width:100%;padding:9px 12px;border:1px solid var(--line);border-radius:20px;font-size:13px;background:#fff;cursor:text;}
.v2add:focus{outline:none;border-color:var(--teal);box-shadow:0 0 0 3px rgba(0,115,133,.09);}
.v2addout{position:absolute;left:0;right:0;top:100%;background:#fff;border:1px solid var(--line);
 border-radius:10px;margin-top:4px;box-shadow:0 10px 26px rgba(12,30,36,.13);z-index:5;overflow:hidden;display:none;}
.v2addout.on{display:block;}
.v2addout button{display:block;width:100%;text-align:left;background:none;border:none;padding:8px 12px;
 font-size:12.5px;color:var(--slate);cursor:pointer;font-family:inherit;}
.v2addout button:hover{background:var(--aqua);}
.v2addout button small{color:var(--dim);font-family:var(--font-mono);font-size:10px;margin-left:6px;}
.v2chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 0;}
.v2chip{border:1px solid var(--line);background:#fff;color:var(--slate);font-size:12px;padding:4px 9px;
 border-radius:14px;cursor:pointer;font-family:inherit;}
.v2chip:hover{border-color:var(--accent);color:var(--accent);}
.v2chip::after{content:' \00d7';color:var(--dim);}
.v2sum{background:var(--slate);color:#fff;border-radius:13px;padding:18px 20px;margin:6px 0 0;}
.v2sum h3{font-family:var(--font-serif);font-size:21px;margin:0 0 6px;color:#fff;}
.v2sum p{font-size:13px;color:#c8d5d7;margin:0;max-width:720px;line-height:1.55;}
.v2sum .big{font-family:var(--font-serif);font-size:30px;color:var(--warm);font-weight:700;}
.v2rows{margin-top:12px;}
.v2row{display:grid;grid-template-columns:210px 1fr 132px 92px;gap:12px;align-items:center;
 padding:9px 12px;border-bottom:1px solid var(--line);background:#fff;cursor:pointer;text-align:left;
 width:100%;font-family:inherit;border-left:none;border-right:none;border-top:none;}
.v2row:first-child{border-radius:11px 11px 0 0;}
.v2row:last-child{border-bottom:none;border-radius:0 0 11px 11px;}
.v2row:hover{background:var(--aqua);}
.v2row .rn{font-size:13px;color:var(--slate);font-weight:600;line-height:1.3;}
.v2row .rb{display:flex;height:9px;border-radius:5px;overflow:hidden;border:1px solid var(--line);background:#fff;}
.v2row .rb i{display:block;height:100%;}
.v2row .rc{font-family:var(--font-mono);font-size:11px;color:var(--muted);text-align:right;}
.v2row .rc.zero{color:var(--accent);}
.v2row .ra{font-size:11.5px;color:var(--teal);font-weight:700;text-align:right;}
@media(max-width:760px){.v2row{grid-template-columns:1fr;gap:5px;}.v2row .rc,.v2row .ra{text-align:left;}}
.v2caveat{background:#fdf1ea;border:1px solid #f0cdb6;border-radius:10px;padding:13px 15px;
 font-size:12.5px;color:#7a4326;margin:14px 0 0;max-width:820px;line-height:1.55;}
.v2caveat b{color:#5e3219;}
.v2empty{background:#fff;border:1px dashed var(--line);border-radius:11px;padding:22px;
 text-align:center;font-size:13px;color:var(--muted);}
"""
rep("\n</style>\n</head>", V2CSS + "\n</style>\n</head>", "E1 css")

# ================================================================ E2: landing markup
i0 = s.index('<!-- ===== Route landing ===== -->')
i1 = s.index('<!-- ===== Condition explorer ===== -->')
OLD_LANDING = s[i0:i1]

NEW_LANDING = """<!-- ===== Route landing (v2: atlas framing) ===== -->
<div id="cxRoute">
 <div class="cxtop"><span class="logo">What is your blood telling you<b>?</b></span><span class="tag">an atlas of what can be measured</span></div>
 <div class="cxwrap">

  <div class="v2hero">
   <div>
    <h1 class="cxhero">There are <span class="v2num" id="v2Total">&hellip;</span> things that can be measured in your blood.<br>A routine annual checkup measures <span class="v2num" id="v2Base">&hellip;</span>.</h1>
    <p class="cxherosub">This is a map of the rest &mdash; what each marker means, which family it belongs to, and how much of that family has never been looked at. What has <em>not</em> been measured is information too.</p>
    <svg class="cxecg" viewBox="0 0 600 40" aria-hidden="true"><path d="M0 20 H218 l8 -5 8 5 h14 l5 -13 7 26 5 -13 h16 l9 -7 11 7 H600"/></svg>
   </div>
   __FIG__
  </div>

  <div class="v2stats" id="v2Stats"></div>

  <div class="cxroutes v2routes">

   <button class="cxroute" id="cxRouteFeel">
    <svg class="ic2" viewBox="0 0 48 48" aria-hidden="true">
     <path d="M24 41 C10 31 4 20 8.5 13 C12.5 6.5 21 7.5 24 14 C27 7.5 35.5 6.5 39.5 13 C44 20 38 31 24 41 Z"/>
     <path d="M13 23 h7 l3 -6 4 12 3 -6 h7"/>
    </svg>
    <h3>Start with how you feel</h3>
    <p>You rarely arrive knowing the diagnosis &mdash; you arrive with a feeling. Pick what is on your mind and see the conditions and markers it opens onto.</p>
    <span class="arr">Guided by symptom &rarr;</span>
   </button>

   <button class="cxroute" id="cxRouteGaps">
    <span class="v2flag">new</span>
    <svg class="ic2" viewBox="0 0 48 48" aria-hidden="true">
     <rect x="9" y="6" width="30" height="36" rx="3"/>
     <path d="M16 17 h11 M16 25 h16 M16 33 h7"/>
     <circle cx="35" cy="33" r="6" stroke-dasharray="2 3"/>
    </svg>
    <h3>Start from what you have already had</h3>
    <p>Check off the bloodwork you have had drawn. What comes back is not a list of results &mdash; it is the shape of what is still unmeasured.</p>
    <span class="v2gapbar" id="v2RouteBar" aria-hidden="true"></span>
    <span class="v2gapkey"><span>measured</span><span>never ordered</span></span>
    <span class="arr">Map my gaps &rarr;</span>
   </button>

   <button class="cxroute alt" id="cxRouteAtlas">
    <svg class="ic2" viewBox="0 0 48 48" aria-hidden="true">
     <circle cx="24" cy="24" r="5"/><circle cx="9" cy="13" r="3"/><circle cx="40" cy="15" r="3"/>
     <circle cx="12" cy="37" r="3"/><circle cx="37" cy="36" r="3"/><circle cx="24" cy="6" r="2.4"/>
    </svg>
    <h3>Open the atlas</h3>
    <div class="cxbig">
     <span><b id="cxCardSys">&hellip;</b> families</span>
     <span><b id="cxCardTests">&hellip;</b> markers</span>
    </div>
    <span class="cxviz viztests" id="cxVizBar" aria-hidden="true"></span>
    <span class="arr">Explore the map &rarr;</span>
   </button>

  </div>

  <section class="v2band">
   <h2>The six questions this is built to answer</h2>
   <p class="sub">Two of them work today. We say which, because a page arguing that missing information is information should be willing to name its own gaps.</p>
   <div class="v2q">
    <div class="v2qc"><h4>What do we know?</h4><p>Every marker, what it measures, who it usually comes up for, and where that wording came from.</p><span class="v2pill ok">built</span></div>
    <div class="v2qc"><h4>What don&rsquo;t we know?</h4><p>Which families are untouched, which markers have never been ordered for you.</p><span class="v2pill proto">new &mdash; gap map</span></div>
    <div class="v2qc"><h4>What&rsquo;s most likely happening?</h4><p>How a pattern of results reads against a condition, with every clause cited.</p><span class="v2pill proto">prototype</span></div>
    <div class="v2qc"><h4>What&rsquo;s worth measuring next?</h4><p>Screen first, then confirm &mdash; the next test that would actually resolve something.</p><span class="v2pill proto">prototype</span></div>
    <div class="v2qc"><h4>What can safely wait?</h4><p>Sourced screening intervals. Currently evidenced for three panels only.</p><span class="v2pill part">partial</span></div>
    <div class="v2qc"><h4>How has this changed?</h4><p>The same marker across years, read against the family it belongs to.</p><span class="v2pill no">not built</span></div>
   </div>
  </section>

  <section class="v2band">
   <h2>What a routine panel actually touches</h2>
   <p class="sub" id="v2MapSub">Every family of blood markers, sized by how many sit inside it.</p>
   <div class="v2mapwrap">
    <div class="v2mapleg">
     <span><i style="background:var(--teal)"></i>reached by a standard annual panel</span>
     <span><i style="background:#fff;border:1.5px dashed #c3ced0"></i>never reached by routine bloodwork</span>
     <span style="margin-left:auto;font-family:var(--font-mono);font-size:10px">circle area &prop; markers in family</span>
    </div>
    <svg id="v2Map" viewBox="0 0 900 330" role="img" aria-label="Families of blood markers sized by number of markers, shaded by whether a routine annual panel reaches them"></svg>
    <div class="v2famleg" id="v2FamLeg"></div>
   </div>
   <p class="v2mapnote" id="v2MapNote"></p>
  </section>

  <div class="v2honest" id="v2Honest"></div>

  <p class="cxfootnote">Educational only &mdash; not medical advice or a diagnosis. Everything links back to a named source so you can verify it. Feedback: <a href="mailto:blood@goinvo.com">blood@goinvo.com</a></p>
 </div>
</div>

<!-- ===== Family atlas (R4) — fixed cockpit, nothing reflows ===== -->
<div id="cxAtlas">
 <div class="atl-top">
  <button class="cxmenu" id="cxAtlasMenu">&larr; Menu</button>
  <span class="logo">What is your blood telling you<b>?</b></span>
  <span class="tag">the atlas</span>
  <span class="sp"></span>
  <span class="atl-hdrstat" id="atlHdrStat"></span>
 </div>

 <div class="atl-stage" id="atlStage">
  <svg class="atl-map" id="atlMap" role="img"
       aria-label="Families of blood markers, sized by how many markers each contains"></svg>

  <div class="atl-left">
   <section class="atl-panel atl-ctl">
    <h1>The atlas of blood</h1>
    <p id="atlLead"></p>
    <div class="atl-row"><span class="atl-lab">shade</span>
     <div class="atl-seg" id="atlShade">
      <button class="on" data-shade="panel">routine panel</button>
      <button data-shade="quoted">sources</button>
     </div>
    </div>
    <div class="atl-row"><span class="atl-lab">order</span>
     <div class="atl-seg" id="atlSort">
      <button class="on" data-sort="size">size</button>
      <button data-sort="gap">least covered</button>
      <button data-sort="name">A&ndash;Z</button>
     </div>
    </div>
   </section>

   <section class="atl-panel atl-index">
    <header><b id="atlIdxN">17</b> families<span class="sp"></span><span id="atlIdxHint">click to inspect</span></header>
    <div class="atl-idxscroll" id="atlIndex"></div>
   </section>
  </div>

  <section class="atl-panel atl-detail">
   <header id="atlDetHead">nothing selected</header>
   <div class="atl-dbody" id="atlDetBody"></div>
   <div class="atl-acts" id="atlDetActs"></div>
  </section>

  <section class="atl-panel atl-foot">
   <div class="atl-leg" id="atlLeg"></div>
   <p class="atl-note" id="atlNote"></p>
  </section>

  <div class="atl-scrim" id="atlScrim"></div>
  <section class="atl-sheet" id="atlSheet" aria-hidden="true">
   <div class="atl-shhead">
    <h2 id="atlShTitle"></h2>
    <p id="atlShSub"></p>
    <button class="atl-shclose" id="atlShClose" aria-label="Close">&times;</button>
   </div>
   <div class="atl-shtools">
    <input type="search" id="atlShFilter" placeholder="Filter markers in this family&hellip;" autocomplete="off">
    <span class="atl-shcount" id="atlShCount"></span>
   </div>
   <div class="atl-shlist" id="atlShList"></div>
   <div class="atl-shfoot">
    <span id="atlShNote"></span>
    <button id="atlShTable">Open in the full table &rarr;</button>
   </div>
  </section>
 </div>
</div>

<!-- ===== Gap map (R3) ===== -->
<div id="cxGaps">
 <div class="cxtop">
  <button class="cxmenu" id="cxGapsMenu">&larr; Menu</button>
  <span class="logo">What is your blood telling you<b>?</b></span>
  <span class="tag">what you have not measured</span>
 </div>
 <div class="cxwrap">
  <h1>What have you actually had measured?</h1>
  <p class="lead">Mark the bloodwork you have had drawn. What comes back is a map of the regions your results have never entered &mdash; because an unmeasured family is information, not an absence of it.</p>

  <div class="v2sec">
   <h2>Step 1 &nbsp;&middot;&nbsp; The routine panels</h2>
   <p class="sub">Most people have had some combination of these three and nothing beyond them. Component lists are quoted from MedlinePlus (NIH).</p>
   <div class="v2panels" id="v2Panels"></div>
   <div class="v2tools" style="margin-top:11px">
    <button class="v2tool" id="v2AllPanels">Mark all three</button>
    <button class="v2tool" id="v2ClearHad">Clear everything</button>
   </div>
  </div>

  <div class="v2sec">
   <h2>Step 2 &nbsp;&middot;&nbsp; Anything else you have had</h2>
   <p class="sub">Add individual markers by name &mdash; ferritin, TSH, vitamin D, whatever else has been drawn.</p>
   <div class="v2addwrap">
    <input id="v2Add" class="v2add" type="search" autocomplete="off" placeholder="Search a marker you have had&hellip;">
    <div class="v2addout" id="v2AddOut"></div>
   </div>
   <div class="v2chips" id="v2HadChips"></div>
  </div>

  <div class="v2sec">
   <h2>Step 3 &nbsp;&middot;&nbsp; The shape of what is missing</h2>
   <p class="sub">Families you have never entered come first. Open any family to read what sits inside it.</p>
   <div id="v2GapSum"></div>
   <div class="v2rows" id="v2GapRows"></div>
   <div class="v2caveat">
    <b>This is a map, not a to-do list.</b> Most of these markers are not tests anyone should have &mdash; a large share are infection-specific assays, therapeutic drug levels and specialist panels that only make sense given a particular question. An empty family means nothing has been looked at there, which is worth <em>knowing</em>; it does not mean something has been missed. Use it to ask better questions, not to order more tests.
   </div>
  </div>
 </div>
</div>

"""
NEW_LANDING = NEW_LANDING.replace("__FIG__", FIG)
s = s[:i0] + NEW_LANDING + s[i1:]
applied.append("E2 landing + new screens")

# ================================================================ E3: setMode
rep("""function setMode(m){
 $('cxRoute').classList.toggle('cx-on',m==='landing');
 $('cxApp').classList.toggle('cx-on',m==='feel');
 const app=$('app'); if(app) app.style.display=(m==='tests')?'grid':'none';
 window.scrollTo(0,0);
}""",
"""function setMode(m){
 $('cxRoute').classList.toggle('cx-on',m==='landing');
 $('cxApp').classList.toggle('cx-on',m==='feel');
 $('cxAtlas').classList.toggle('cx-on',m==='atlas');
 $('cxGaps').classList.toggle('cx-on',m==='gaps');
 const app=$('app'); if(app) app.style.display=(m==='tests')?'grid':'none';
 if(m==='atlas'&&window.__v2DrawAtlas) window.__v2DrawAtlas();
 if(m==='gaps'&&window.__v2DrawGaps) window.__v2DrawGaps();
 window.scrollTo(0,0);
}""", "E3 setMode")

# ================================================================ E4: route buttons + landing flourish
i0 = s.index("/* route landing + menu */")
i1 = s.index("$('cxMenuBtn').addEventListener('click',()=>setMode('landing'));")
V2JS = r"""/* route landing + menu */
$('cxRouteFeel').addEventListener('click',()=>{setMode('feel');show('home');});
$('cxRouteAtlas').addEventListener('click',()=>{ setMode('atlas'); });
$('cxRouteGaps').addEventListener('click',()=>{ setMode('gaps'); });
$('cxAtlasMenu').addEventListener('click',()=>setMode('landing'));
$('cxGapsMenu').addEventListener('click',()=>setMode('landing'));

/* ============================================================================
   v2 — atlas landing, family atlas, gap map.
   Every figure below is derived from the payload at run time; nothing is typed
   in by hand, so the page cannot drift from the dataset it is describing.
   ============================================================================ */
(function(){

 /* ---------- derived facts ---------- */
 const N_TOTAL   = TESTS.length;
 const N_BASE    = TESTS.reduce((a,t)=>a+(t.b?1:0),0);
 const N_NOCON   = TESTS.reduce((a,t)=>a+((t.k&&t.k.length)?0:1),0);
 const N_QUOTED  = TESTS.reduce((a,t)=>a+(t.v?1:0),0);
 const N_GEN     = N_TOTAL-N_QUOTED;
 const N_CROSS   = TESTS.reduce((a,t)=>a+(t.x?1:0),0);

 const FAM = GROUPS.map((label,i)=>({i,label,n:0,base:0,quoted:0}));
 TESTS.forEach(t=>{ const f=FAM[t.g]; f.n++; if(t.b)f.base++; if(t.v)f.quoted++; });
 const FAM_BASE0   = FAM.filter(f=>!f.base);
 const FAM_QUOTED0 = FAM.filter(f=>!f.quoted);
 const BIGGEST     = FAM.slice().sort((a,b)=>b.n-a.n)[0];
 const IRON        = FAM.find(f=>/iron/i.test(f.label));

 const SOURCES=(function(){
  const seen={}; TESTS.forEach(t=>{ if(t.v&&t.qs) seen[t.qs]=(seen[t.qs]||0)+1; });
  return Object.keys(seen).sort((a,b)=>seen[b]-seen[a]);
 })();
 function shortSrc(x){ return x.replace(/\s*[—-]\s*sourced via.*$/i,'').replace(/\s*\(NIH\)/,' (NIH)').trim(); }

 /* ---------- landing: hero + stats ---------- */
 $('v2Total').textContent=nfmt(N_TOTAL);
 $('v2Base').textContent=nfmt(N_BASE);
 const tn=$('cxCardTests'), sn=$('cxCardSys');
 if(tn) tn.textContent=nfmt(N_TOTAL);
 if(sn) sn.textContent=GROUPS.length;

 $('v2Stats').innerHTML=
   stat('a', nfmt(N_BASE), 'of '+nfmt(N_TOTAL),
        'measured by a standard annual panel &mdash; CBC, CMP and lipids. Everything else is a decision somebody has to make.')
  +stat('b', nfmt(N_NOCON), '',
        'markers that no symptom in this app currently points to. A quarter of the atlas has no way in.')
  +stat('c', FAM_QUOTED0.length, 'of '+GROUPS.length,
        'families with no source-quoted entry yet. Unsurveyed regions of our own map.');
 function stat(cls,big,small,txt){
  return '<div class="v2stat '+cls+'"><b>'+big+(small?' <i>'+small+'</i>':'')+'</b><span>'+txt+'</span></div>';
 }

 /* mini coverage bar on the gap route card */
 (function(){
  const el=$('v2RouteBar'); if(!el) return;
  const pct=Math.max(1.2,100*N_BASE/N_TOTAL);
  el.innerHTML='<i style="background:var(--teal);width:'+pct+'%"></i>'
              +'<i class="v2blocked" style="width:'+(100-pct)+'%"></i>';
 })();

 /* the small per-family bar chart on the atlas card (kept from v1) */
 (function(){
  const bar=$('cxVizBar'); if(!bar) return;
  const max=Math.max.apply(null,FAM.map(f=>f.n))||1;
  bar.innerHTML=FAM.map(f=>'<b style="height:'+Math.round(16+84*(f.n/max))+'%;background:'+
   SYSCOL[f.i%SYSCOL.length]+';animation-delay:'+(f.i*45)+'ms" title="'+esc(f.label)+' — '+nfmt(f.n)+'"></b>').join('');
 })();

 /* ---------- the family map ----------
    Deterministic circle packing: families are placed largest-first on a
    phyllotaxis spiral, each at the first position that clears every circle
    already down. No edges are drawn between families, because the dataset
    does not yet contain marker-to-marker relationships. */
 function packed(W,H){
  const max=Math.max.apply(null,FAM.map(f=>f.n))||1;
  const rOf=n=>11+47*Math.sqrt(n/max);
  const list=FAM.slice().sort((a,b)=>b.n-a.n);
  const out=[], cx=W/2, cy=H/2+2;
  list.forEach(f=>{
   const r=rOf(f.n);
   for(let k=0;k<12000;k++){
    const ang=k*2.399963267, d=3.1*Math.sqrt(k);
    const x=cx+d*Math.cos(ang)*3.05, y=cy+d*Math.sin(ang)*0.86;
    if(x-r<8||x+r>W-8||y-r<10||y+r>H-10) continue;
    let ok=true;
    for(let j=0;j<out.length;j++){
     const p=out[j];
     if(Math.hypot(x-p.x,y-p.y) < r+p.r+10){ ok=false; break; }
    }
    if(ok){ out.push({f:f,x:x,y:y,r:r}); return; }
   }
   out.push({f:f,x:cx,y:cy,r:r});
  });
  return out;
 }

 function drawMap(svgEl,shade){
  const W=900,H=330;
  const nodes=packed(W,H);
  svgEl.innerHTML=nodes.map(nd=>{
   const f=nd.f;
   const covered = shade==='quoted' ? f.quoted>0 : f.base>0;
   const fill    = covered?'var(--aqua)':'#fff';
   const stroke  = covered?'var(--teal)':'#c3ced0';
   const dash    = covered?'':' stroke-dasharray="3 3"';
   const num     = shade==='quoted'
     ? nfmt(f.quoted)+' / '+nfmt(f.n)
     : nfmt(f.base)+' / '+nfmt(f.n);
   let label='';
   if(nd.r>=19){
    const words=f.label.replace(' / ','/').split(' ');
    const l1=words.slice(0,2).join(' ');
    label='<text class="v2fam-t" x="'+nd.x.toFixed(1)+'" y="'+(nd.y-1).toFixed(1)+'" text-anchor="middle"'
        +(covered?' style="fill:var(--slate)"':'')+'>'+esc(l1)+'</text>'
        +'<text class="v2fam-n" x="'+nd.x.toFixed(1)+'" y="'+(nd.y+10).toFixed(1)+'" text-anchor="middle"'
        +(covered?' style="fill:var(--teal)"':'')+'>'+num+'</text>';
   }
   const tip = shade==='quoted'
     ? nfmt(f.quoted)+' of them quoted from a named source'
     : nfmt(f.base)+' of them reached by a routine annual panel';
   return '<g><title>'+esc(f.label)+' — '+nfmt(f.n)+' markers · '+tip+'</title>'
     +'<circle cx="'+nd.x.toFixed(1)+'" cy="'+nd.y.toFixed(1)+'" r="'+nd.r.toFixed(1)+'" fill="'+fill+'" stroke="'+stroke+'" stroke-width="'+(covered?2:1.2)+'"'+dash+'/>'
     +label+'</g>';
  }).join('');
  // trim the viewBox to what was actually used, so the map never renders inset
  const x0=Math.min.apply(null,nodes.map(n=>n.x-n.r))-10, x1=Math.max.apply(null,nodes.map(n=>n.x+n.r))+10;
  const y0=Math.min.apply(null,nodes.map(n=>n.y-n.r))-8,  y1=Math.max.apply(null,nodes.map(n=>n.y+n.r))+8;
  svgEl.setAttribute('viewBox',x0.toFixed(0)+' '+y0.toFixed(0)+' '+(x1-x0).toFixed(0)+' '+(y1-y0).toFixed(0));
 }

 function famLegend(el,shade){
  el.innerHTML=FAM.slice().sort((a,b)=>b.n-a.n).map(f=>{
   const covered = shade==='quoted' ? f.quoted>0 : f.base>0;
   return '<span><i style="background:'+(covered?'var(--teal)':'#fff')+';border:1px '+(covered?'solid var(--teal)':'dashed #c3ced0')+'"></i>'
     +esc(f.label)+' <b>'+nfmt(f.n)+'</b></span>';
  }).join('');
 }

 drawMap($('v2Map'),'panel');
 famLegend($('v2FamLeg'),'panel');
 $('v2MapSub').innerHTML='All '+GROUPS.length+' families of blood markers, sized by how many sit inside. '
   +'Filled where a standard annual panel reaches; hollow where routine bloodwork never goes. '
   +'<b>'+(GROUPS.length-FAM_BASE0.length)+' of '+GROUPS.length+'</b> families are lit.';
 $('v2MapNote').innerHTML=
   (IRON?'<b>'+esc(IRON.label)+': '+IRON.base+' of '+IRON.n+'.</b> Routine bloodwork does not enter this family at all &mdash; the CBC can hint at iron deficiency, but the confirming markers sit outside the annual panel. ':'')
  +'No lines are drawn between families here, and that is deliberate: only '+N_CROSS+' of '+nfmt(N_TOTAL)
  +' markers currently carry a link to any other. Until that relationship layer exists this map shows regions, not roads.';

 /* ---------- landing honesty band ---------- */
 $('v2Honest').innerHTML=
  '<h4>What this atlas does not know yet</h4>'
 +'<div class="v2covbar"><i style="background:var(--teal);width:'+(100*N_QUOTED/N_TOTAL).toFixed(1)+'%"></i>'
 +'<i class="v2blocked" style="flex:1"></i></div>'
 +'<p style="margin:0">'+nfmt(N_QUOTED)+' entries are quoted verbatim from a named authority &mdash; '
 +SOURCES.slice(0,4).map(x=>esc(shortSrc(x))).join(', ')+' and others &mdash; with a link so you can check. '
 +'The other '+nfmt(N_GEN)+' were written by an AI model from the test&rsquo;s official LOINC name and category, '
 +'and every one links to its LOINC record. '+FAM_QUOTED0.length+' of '+GROUPS.length+' families have no quoted entry at all; '
 +'the largest family, '+esc(BIGGEST.label.toLowerCase())+', has '+BIGGEST.quoted+' quoted out of '+nfmt(BIGGEST.n)+'. '
 +'We label which is which on every row, because the difference matters more than the total.</p>';

 /* ---------- open a family in the test table ---------- */
 function openFamily(i){
  if(window.__cxEnsureTests) window.__cxEnsureTests();
  setMode('tests');
  const sel=document.getElementById('tblSys');
  if(sel) sel.value=String(i);
  const tv=document.querySelector('#viewTog [data-view="table"]');
  if(tv) tv.click();
  if(sel) sel.dispatchEvent(new Event('change'));
 }

 /* ================= ATLAS COCKPIT =================
    Layout is fixed: panels are absolutely positioned and never change size.
    pack() runs once per stage size and caches positions; paint() only swaps
    colours, so toggling shade never moves a circle. */
 let atlShade='panel', atlSort='size', atlSel=null, atlHot=null;
 let atlNodes=null, atlKey='';

 function atlBounds(W,H){
  // keep circles clear of the floating panels; measured, not guessed
  const st=$('atlStage');
  const box=el=>{ const r=el.getBoundingClientRect(), s=st.getBoundingClientRect();
                  return {l:r.left-s.left, r:r.right-s.left, t:r.top-s.top, b:r.bottom-s.top}; };
  let L=18, R=W-18, T=18, B=H-18;
  const left=st.querySelector('.atl-left'), det=st.querySelector('.atl-detail'), foot=st.querySelector('.atl-foot');
  if(left && left.offsetParent) L=Math.max(L, box(left).r+18);
  if(det  && det.offsetParent)  R=Math.min(R, box(det).l-18);
  if(foot && foot.offsetParent) B=Math.min(B, box(foot).t-16);
  if(R-L<220){ L=18; R=W-18; }          // very narrow: use the whole stage
  return {L:L,R:R,T:T,B:B};
 }

 function atlPack(){
  const st=$('atlStage'), W=st.clientWidth, H=st.clientHeight;
  const key=W+'x'+H;
  if(atlKey===key && atlNodes) return atlNodes;
  const b=atlBounds(W,H);
  const cx=(b.L+b.R)/2, cy=(b.T+b.B)/2;
  const spanX=(b.R-b.L)/2, spanY=(b.B-b.T)/2;
  const max=Math.max.apply(null,FAM.map(f=>f.n))||1;
  // area-conserving scale: grow the circles until they fill ~46% of the region,
  // so the map uses the space it is given at any window size
  const base=n=>13+52*Math.sqrt(n/max);
  const baseArea=FAM.reduce((a,f)=>a+Math.PI*base(f.n)*base(f.n),0);
  const region=(b.R-b.L)*(b.B-b.T);
  const scale=Math.max(.5,Math.min(2.4,Math.sqrt(0.46*region/baseArea)));
  const rOf=n=>base(n)*scale;
  const list=FAM.slice().sort((a,b2)=>b2.n-a.n);
  const out=[];
  list.forEach(f=>{
   const r=rOf(f.n);
   for(let k=0;k<30000;k++){
    const ang=k*2.399963267, d=Math.sqrt(k/3000);
    const x=cx+Math.cos(ang)*d*spanX*1.25, y=cy+Math.sin(ang)*d*spanY*1.25;
    if(x-r<b.L||x+r>b.R||y-r<b.T||y+r>b.B) continue;
    let ok=true;
    for(let j=0;j<out.length;j++){
     const p=out[j];
     if(Math.hypot(x-p.x,y-p.y) < r+p.r+11){ ok=false; break; }
    }
    if(ok){ out.push({f:f,x:x,y:y,r:r}); return; }
   }
   out.push({f:f,x:cx,y:cy,r:r});
  });
  $('atlMap').setAttribute('viewBox','0 0 '+W+' '+H);
  atlKey=key; atlNodes=out;
  return out;
 }

 function atlPaint(){
  const nodes=atlPack();
  $('atlMap').innerHTML=nodes.map(nd=>{
   const f=nd.f;
   const lit   = atlShade==='quoted' ? f.quoted>0 : f.base>0;
   const hit   = atlShade==='quoted' ? f.quoted   : f.base;
   // deliberately no dimming of the unselected: the shape of what is unmeasured
   // is the point of the map, and it should stay readable while you inspect one family
   const cls   = ['fam', lit?'lit':'', atlSel===f.i?'sel':'', atlHot===f.i?'hot':''].filter(Boolean).join(' ');
   const num   = nfmt(hit)+' / '+nfmt(f.n);
   const words = f.label.replace(' / ','/').split(' ');
   const short = words.length>2 ? words.slice(0,2).join(' ') : f.label;
   const label = nd.r>=26
     ? '<text class="fam-t" x="'+nd.x.toFixed(1)+'" y="'+(nd.y-1).toFixed(1)+'" text-anchor="middle">'+esc(short)+'</text>'
       +'<text class="fam-n" x="'+nd.x.toFixed(1)+'" y="'+(nd.y+12).toFixed(1)+'" text-anchor="middle">'+num+'</text>'
     : '';
   return '<g class="'+cls+'" data-fam="'+f.i+'">'
    +'<title>'+esc(f.label)+' — '+nfmt(f.n)+' markers, '+num+' '
      +(atlShade==='quoted'?'source-quoted':'in a routine annual panel')+'</title>'
    +'<circle cx="'+nd.x.toFixed(1)+'" cy="'+nd.y.toFixed(1)+'" r="'+nd.r.toFixed(1)+'" '
      +'fill="'+(lit?'var(--aqua)':'#fff')+'" stroke="'+(lit?'var(--teal)':'#c3ced0')+'" '
      +'stroke-width="'+(lit?2:1.3)+'"'+(lit?'':' stroke-dasharray="3 3"')+'/>'
    +label+'</g>';
  }).join('');
 }

 function atlDrawIndex(){
  const list=FAM.slice();
  if(atlSort==='size') list.sort((a,b)=>b.n-a.n);
  else if(atlSort==='name') list.sort((a,b)=>a.label.localeCompare(b.label));
  else list.sort((a,b)=>{
   const ca=atlShade==='quoted'?a.quoted/a.n:a.base/a.n;
   const cb=atlShade==='quoted'?b.quoted/b.n:b.base/b.n;
   return ca-cb || b.n-a.n;
  });
  $('atlIndex').innerHTML=list.map(f=>{
   const hit=atlShade==='quoted'?f.quoted:f.base;
   const pct=hit?Math.max(4,100*hit/f.n):0;
   const col=atlShade==='quoted'?'var(--ok)':'var(--teal)';
   return '<button class="atl-ir'+(atlSel===f.i?' sel':'')+'" data-fam="'+f.i+'">'
    +'<span class="n" title="'+esc(f.label)+'">'+esc(f.label)+'</span>'
    +'<span class="b">'+(pct?'<i style="background:'+col+';width:'+pct+'%"></i>':'')
      +'<i class="v2blocked" style="flex:1"></i></span>'
    +'</button>';
  }).join('');
 }

 function atlDrawDetail(){
  const head=$('atlDetHead'), body=$('atlDetBody'), acts=$('atlDetActs');
  if(atlSel===null){
   head.textContent='the whole atlas';
   body.innerHTML='<p class="atl-dt" style="margin-bottom:8px">'+nfmt(N_TOTAL)+' markers</p>'
    +'<p class="atl-dsub">across '+GROUPS.length+' families</p>'
    +'<div class="atl-cov"><div class="k"><span>in a routine annual panel</span><b>'+nfmt(N_BASE)+' / '+nfmt(N_TOTAL)+'</b></div>'
    +'<div class="bar"><i style="background:var(--teal);width:'+Math.max(1,100*N_BASE/N_TOTAL)+'%"></i><i class="v2blocked" style="flex:1"></i></div></div>'
    +'<div class="atl-cov"><div class="k"><span>quoted from a named source</span><b>'+nfmt(N_QUOTED)+' / '+nfmt(N_TOTAL)+'</b></div>'
    +'<div class="bar"><i style="background:var(--ok);width:'+Math.max(1,100*N_QUOTED/N_TOTAL)+'%"></i><i class="v2blocked" style="flex:1"></i></div></div>'
    +'<div class="atl-samp"><p class="h">reading this map</p><p class="atl-empty">'
    +'Each circle is a family, sized by how many markers sit inside it. '
    +'<b>'+(GROUPS.length-FAM_BASE0.length)+' of '+GROUPS.length+'</b> are reached by a standard annual panel; the rest are regions '
    +'routine bloodwork never enters.<br><br>Pick a family on the left, or click a circle.</p></div>';
   acts.innerHTML='<button class="atl-btn" disabled>Select a family to browse it</button>';
   return;
  }
  const f=FAM[atlSel];
  const sample=[];
  for(let i=0;i<TESTS.length && sample.length<6;i++){
   if(TESTS[i].g===f.i && (TESTS[i].v || TESTS[i].b)) sample.push(TESTS[i]);
  }
  if(sample.length<6) for(let i=0;i<TESTS.length && sample.length<6;i++){
   if(TESTS[i].g===f.i && sample.indexOf(TESTS[i])<0) sample.push(TESTS[i]);
  }
  head.innerHTML='family <b>'+(FAM.slice().sort((a,b)=>b.n-a.n).findIndex(x=>x.i===f.i)+1)+'</b> of '+GROUPS.length;
  body.innerHTML='<h2 class="atl-dt">'+esc(f.label)+'</h2>'
   +'<p class="atl-dsub">'+nfmt(f.n)+' markers in this family</p>'
   +'<div class="atl-big">'+nfmt(f.base)+'<small>reached by a routine annual panel</small></div>'
   +'<div class="atl-cov"><div class="k"><span>routine panel</span><b'+(f.base?'':' class="zero"')+'>'+nfmt(f.base)+' / '+nfmt(f.n)+'</b></div>'
   +'<div class="bar">'+(f.base?'<i style="background:var(--teal);width:'+Math.max(3,100*f.base/f.n)+'%"></i>':'')+'<i class="v2blocked" style="flex:1"></i></div></div>'
   +'<div class="atl-cov"><div class="k"><span>source-quoted</span><b'+(f.quoted?'':' class="zero"')+'>'+nfmt(f.quoted)+' / '+nfmt(f.n)+'</b></div>'
   +'<div class="bar">'+(f.quoted?'<i style="background:var(--ok);width:'+Math.max(3,100*f.quoted/f.n)+'%"></i>':'')+'<i class="v2blocked" style="flex:1"></i></div></div>'
   +(f.base?'':'<p class="atl-empty" style="margin:13px 0 0;color:var(--accent);font-size:11.5px">Routine bloodwork does not enter this family at all.</p>')
   +'<div class="atl-samp"><p class="h">what sits inside</p><ul>'
   +sample.map(t=>'<li>'+esc(t.n.split('[')[0].trim())+(t.a?' <i>'+esc(t.a)+'</i>':'')+'</li>').join('')
   +'</ul></div>';
  acts.innerHTML='<button class="atl-btn" data-sheet="'+f.i+'">Browse '+nfmt(f.n)+' markers</button>'
   +'<button class="atl-btn ghost" data-table="'+f.i+'">Open in the full table &rarr;</button>';
 }

 function atlDrawChrome(){
  $('atlHdrStat').textContent=nfmt(N_TOTAL)+' markers · '+GROUPS.length+' families · '
   +nfmt(N_BASE)+' in a routine panel';
  $('atlLead').innerHTML='Everything science can currently measure in blood, grouped into '
   +GROUPS.length+' families.';
  $('atlIdxN').textContent=GROUPS.length;
  $('atlLeg').innerHTML= atlShade==='quoted'
   ? '<span><i style="background:var(--aqua);border:1.5px solid var(--teal)"></i>has a source-quoted entry</span>'
     +'<span><i style="background:#fff;border:1.5px dashed #c3ced0"></i>nothing quoted yet</span>'
   : '<span><i style="background:var(--aqua);border:1.5px solid var(--teal)"></i>reached by a routine annual panel</span>'
     +'<span><i style="background:#fff;border:1.5px dashed #c3ced0"></i>never reached by routine bloodwork</span>';
  $('atlNote').innerHTML='Circle area is proportional to the markers inside. '
   +'<b>No lines are drawn between families</b>, and that is deliberate — only '+N_CROSS+' of '
   +nfmt(N_TOTAL)+' markers carry a link to any other, so this shows regions, not roads.';
 }

 function atlSelect(i){
  atlSel = (i===atlSel) ? null : i;
  atlDrawIndex(); atlDrawDetail(); atlPaint();
 }

 window.__v2DrawAtlas=function(){
  atlDrawChrome(); atlDrawIndex(); atlDrawDetail();
  // stage has zero size until the screen is shown, so pack on the next frame
  requestAnimationFrame(()=>{ atlKey=''; atlPaint(); });
 };

 /* ---- controls ---- */
 $('atlShade').addEventListener('click',function(e){
  const b=e.target.closest('[data-shade]'); if(!b) return;
  atlShade=b.dataset.shade;
  [].forEach.call(this.children,x=>x.classList.toggle('on',x===b));
  atlDrawChrome(); atlDrawIndex(); atlDrawDetail(); atlPaint();   // positions unchanged
 });
 $('atlSort').addEventListener('click',function(e){
  const b=e.target.closest('[data-sort]'); if(!b) return;
  atlSort=b.dataset.sort;
  [].forEach.call(this.children,x=>x.classList.toggle('on',x===b));
  atlDrawIndex();
 });

 /* ---- index <-> map cross-highlight ---- */
 $('atlIndex').addEventListener('click',e=>{ const b=e.target.closest('[data-fam]'); if(b) atlSelect(+b.dataset.fam); });
 $('atlIndex').addEventListener('mouseover',e=>{ const b=e.target.closest('[data-fam]'); if(!b) return;
  if(atlHot!==+b.dataset.fam){ atlHot=+b.dataset.fam; atlPaint(); } });
 $('atlIndex').addEventListener('mouseleave',()=>{ if(atlHot!==null){ atlHot=null; atlPaint(); } });
 $('atlMap').addEventListener('click',e=>{ const g=e.target.closest('[data-fam]'); if(g) atlSelect(+g.dataset.fam); });
 $('atlMap').addEventListener('mouseover',e=>{ const g=e.target.closest('[data-fam]'); const v=g?+g.dataset.fam:null;
  if(v!==atlHot){ atlHot=v; atlPaint(); const row=$('atlIndex').querySelector('[data-fam="'+v+'"]');
   [].forEach.call($('atlIndex').children,x=>x.classList.remove('hot')); if(row) row.classList.add('hot'); } });
 $('atlDetActs').addEventListener('click',e=>{
  const s2=e.target.closest('[data-sheet]'); if(s2){ atlOpenSheet(+s2.dataset.sheet); return; }
  const t=e.target.closest('[data-table]'); if(t) openFamily(+t.dataset.table);
 });
 window.addEventListener('resize',function(){
  clearTimeout(window.__atlRT);
  window.__atlRT=setTimeout(function(){ if($('cxAtlas').classList.contains('cx-on')){ atlKey=''; atlPaint(); } },160);
 });

 /* ---- overlay sheet: markers inside one family ---- */
 const SHEET_CAP=300;
 let shFam=null;
 function atlOpenSheet(i){
  shFam=i; const f=FAM[i];
  $('atlShTitle').textContent=f.label;
  $('atlShSub').textContent=nfmt(f.n)+' markers · '+nfmt(f.base)+' in a routine annual panel · '
   +nfmt(f.quoted)+' source-quoted';
  $('atlShFilter').value='';
  atlSheetList('');
  $('atlScrim').classList.add('on');
  $('atlSheet').classList.add('on');
  $('atlSheet').setAttribute('aria-hidden','false');
 }
 function atlCloseSheet(){
  $('atlScrim').classList.remove('on');
  $('atlSheet').classList.remove('on');
  $('atlSheet').setAttribute('aria-hidden','true');
 }
 function atlSheetList(q){
  q=(q||'').trim().toLowerCase();
  const rows=[]; let total=0;
  for(let i=0;i<TESTS.length;i++){
   const t=TESTS[i];
   if(t.g!==shFam) continue;
   if(q && t.n.toLowerCase().indexOf(q)<0 && !(t.a&&t.a.toLowerCase().indexOf(q)>=0)) continue;
   total++;
   if(rows.length>=SHEET_CAP) continue;
   const url=(t.r&&t.r.length)?t.r[t.r.length-1][0]:null;
   rows.push('<div class="atl-mr"><span class="mn">'
    +(url?'<a href="'+url+'" target="_blank" rel="noopener">'+esc(t.n.split('[')[0].trim())+'</a>'
         :esc(t.n.split('[')[0].trim()))
    +(t.a?'<i>'+esc(t.a)+'</i>':'')+'</span><span class="mt">'
    +(t.b?'<span class="atl-tg panel">annual panel</span>':'')
    +(t.v?'<span class="atl-tg q">quoted</span>':'<span class="atl-tg g">ai-generated</span>')
    +'</span></div>');
  }
  $('atlShList').innerHTML=rows.join('') ||
   '<div style="padding:26px;text-align:center;color:var(--dim);font-size:12.5px">No marker matches that.</div>';
  $('atlShCount').textContent=nfmt(total)+' shown';
  $('atlShNote').textContent = total>SHEET_CAP
   ? 'Showing the first '+SHEET_CAP+' of '+nfmt(total)+' — filter to narrow.'
   : 'Every row links to its LOINC record.';
 }
 $('atlShClose').addEventListener('click',atlCloseSheet);
 $('atlScrim').addEventListener('click',atlCloseSheet);
 $('atlShTable').addEventListener('click',()=>{ atlCloseSheet(); openFamily(shFam); });
 let shT=null;
 $('atlShFilter').addEventListener('input',function(){
  clearTimeout(shT); const v=this.value; shT=setTimeout(()=>atlSheetList(v),120);
 });
 document.addEventListener('keydown',function(e){
  if(e.key==='Escape' && $('atlSheet').classList.contains('on')) atlCloseSheet();
 });

 /* ================= GAP MAP ================= */
 const HAD_KEY='v2.had';
 let had=new Set();
 try{ const raw=localStorage.getItem(HAD_KEY); if(raw) JSON.parse(raw).forEach(i=>{ if(TESTS[i]) had.add(i); }); }catch(err){}
 function saveHad(){ try{ localStorage.setItem(HAD_KEY,JSON.stringify(Array.from(had))); }catch(err){} }

 const PANEL_IDX=PANELS.map(p=>p.linked.map(l=>l.i));

 function drawPanels(){
  $('v2Panels').innerHTML=PANELS.map((p,pi)=>{
   const idx=PANEL_IDX[pi], on=idx.every(i=>had.has(i));
   return '<button class="v2pc'+(on?' on':'')+'" data-panel="'+pi+'">'
    +'<span class="pn">'+esc(p.name)+'</span>'
    +'<span class="pq">&ldquo;'+esc(p.quote)+'&rdquo;</span>'
    +'<span class="pc">'+esc(p.src)+' &middot; '+idx.length+' components</span>'
    +'<span class="'+(on?'pmark':'pc')+'">'+(on?'✓ marked as done':'click to mark as done')+'</span>'
    +'</button>';
  }).join('');
 }

 function drawChips(){
  const extra=Array.from(had).filter(i=>!TESTS[i].b);
  $('v2HadChips').innerHTML = extra.length
   ? extra.map(i=>'<button class="v2chip" data-drop="'+i+'">'+esc(TESTS[i].n.split('[')[0].trim())+'</button>').join('')
   : '<span style="font-size:12px;color:var(--dim)">Nothing added beyond the panels above.</span>';
 }

 function drawGaps(){
  const per=GROUPS.map(()=>0);
  had.forEach(i=>{ per[TESTS[i].g]++; });
  const nHad=had.size;
  const empty=FAM.filter(f=>!per[f.i]);

  $('v2GapSum').innerHTML='<div class="v2sum"><h3>'
   +'<span class="big">'+nfmt(nHad)+'</span> of '+nfmt(N_TOTAL)+' markers measured</h3>'
   +'<p>'+(nHad
      ? '<b>'+empty.length+' of '+GROUPS.length+'</b> families have nothing measured in them at all. '
        +'That is not a gap in your care &mdash; it is the shape of what your bloodwork has never been asked about. '
        +'The families below are ordered so the untouched ones come first.'
      : 'Nothing marked yet. Use the panels above &mdash; most people have had at least one of them &mdash; and the list below will redraw.')
   +'</p></div>';

  const list=FAM.slice().sort((a,b)=>{
   const ea=per[a.i]?1:0, eb=per[b.i]?1:0;
   return ea-eb || b.n-a.n;
  });
  $('v2GapRows').innerHTML=list.map(f=>{
   const c=per[f.i], pct=c?Math.max(1.5,100*c/f.n):0;
   return '<button class="v2row" data-fam="'+f.i+'">'
    +'<span class="rn">'+esc(f.label)+'</span>'
    +'<span class="rb">'+(c?'<i style="background:var(--teal);width:'+pct+'%"></i>':'')+'<i class="v2blocked" style="flex:1"></i></span>'
    +'<span class="rc'+(c?'':' zero')+'">'+(c?nfmt(c)+' of '+nfmt(f.n)+' measured':'0 of '+nfmt(f.n)+' — never entered')+'</span>'
    +'<span class="ra">open &rarr;</span>'
    +'</button>';
  }).join('');
 }

 window.__v2DrawGaps=function(){ drawPanels(); drawChips(); drawGaps(); };

 $('v2Panels').addEventListener('click',function(e){
  const b=e.target.closest('[data-panel]'); if(!b) return;
  const idx=PANEL_IDX[+b.dataset.panel], on=idx.every(i=>had.has(i));
  idx.forEach(i=>{ on?had.delete(i):had.add(i); });
  saveHad(); window.__v2DrawGaps();
 });
 $('v2AllPanels').addEventListener('click',function(){
  PANEL_IDX.forEach(idx=>idx.forEach(i=>had.add(i)));
  saveHad(); window.__v2DrawGaps();
 });
 $('v2ClearHad').addEventListener('click',function(){
  had.clear(); saveHad(); window.__v2DrawGaps();
 });
 $('v2HadChips').addEventListener('click',function(e){
  const b=e.target.closest('[data-drop]'); if(!b) return;
  had.delete(+b.dataset.drop); saveHad(); window.__v2DrawGaps();
 });
 $('v2GapRows').addEventListener('click',function(e){
  const b=e.target.closest('[data-fam]'); if(b) openFamily(+b.dataset.fam);
 });

 /* marker search for "anything else you have had" */
 let addT=null;
 $('v2Add').addEventListener('input',function(){
  clearTimeout(addT);
  const q=this.value.trim().toLowerCase();
  const out=$('v2AddOut');
  if(q.length<2){ out.classList.remove('on'); out.innerHTML=''; return; }
  addT=setTimeout(function(){
   const hits=[];
   for(let i=0;i<TESTS.length && hits.length<9;i++){
    const t=TESTS[i];
    if(had.has(i)) continue;
    if(t.n.toLowerCase().indexOf(q)>=0 || (t.a&&t.a.toLowerCase().indexOf(q)===0)) hits.push(i);
   }
   out.innerHTML = hits.length
    ? hits.map(i=>'<button data-add="'+i+'">'+esc(TESTS[i].n.split('[')[0].trim())
        +'<small>'+esc(GROUPS[TESTS[i].g])+'</small></button>').join('')
    : '<button disabled style="color:var(--dim);cursor:default">No marker matches that.</button>';
   out.classList.add('on');
  },120);
 });
 $('v2AddOut').addEventListener('click',function(e){
  const b=e.target.closest('[data-add]'); if(!b) return;
  had.add(+b.dataset.add); saveHad();
  $('v2Add').value=''; this.classList.remove('on'); this.innerHTML='';
  window.__v2DrawGaps();
 });
 document.addEventListener('click',function(e){
  if(!e.target.closest('.v2addwrap')) $('v2AddOut').classList.remove('on');
 });

})();

"""
s = s[:i0] + V2JS + s[i1:]
applied.append("E4 landing js + atlas + gaps")

# ================================================================ E5: history / popstate
rep("""  if(r.m==='tests'){ if(window.__cxEnsureTests)window.__cxEnsureTests(); _cxSetMode('tests'); cxRouteState.m='tests'; }
  else if(r.m==='landing'){ _cxSetMode('landing'); cxRouteState.m='landing'; cxRouteState.s='home'; }""",
"""  if(r.m==='tests'){ if(window.__cxEnsureTests)window.__cxEnsureTests(); _cxSetMode('tests'); cxRouteState.m='tests'; }
  else if(r.m==='atlas'||r.m==='gaps'){ _cxSetMode(r.m); cxRouteState.m=r.m; cxRouteState.s='home'; }
  else if(r.m==='landing'){ _cxSetMode('landing'); cxRouteState.m='landing'; cxRouteState.s='home'; }""",
    "E5 popstate")

rep(" if(h[0]==='tests'){ if(window.__cxEnsureTests)window.__cxEnsureTests(); setMode('tests'); }",
    " if(h[0]==='tests'){ if(window.__cxEnsureTests)window.__cxEnsureTests(); setMode('tests'); }\n else if(h[0]==='atlas'||h[0]==='gaps'){ setMode(h[0]); }",
    "E6 hash router")

io.open(DST,"w",encoding="utf8").write(s)
print("applied:", *applied, sep="\n  - ")
print("\nbytes: %d -> %d (+%d)" % (orig_len, len(s), len(s)-orig_len))
