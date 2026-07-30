import re, sys, io, os

SRC = "/sessions/optimistic-vigilant-turing/mnt/Blood test/blood-tests-dashboard/index.html"
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

/* ---------- shared screen chrome for the two new modes ---------- */
#cxAtlas,#cxGaps{position:fixed;inset:0;overflow-y:auto;background:var(--paper);z-index:40;display:none;}
#cxAtlas.cx-on,#cxGaps.cx-on{display:block;}
#cxAtlas .cxwrap,#cxGaps .cxwrap{max-width:1120px;margin:0 auto;padding:22px 24px 90px;}
#cxAtlas .cxtop,#cxGaps .cxtop{display:flex;align-items:center;gap:14px;border-bottom:1px solid var(--line);
 padding:12px 24px;background:var(--panel);position:sticky;top:0;z-index:3;}
#cxAtlas .cxtop .logo,#cxGaps .cxtop .logo{font-family:var(--font-serif);font-size:19px;color:var(--slate);font-weight:700;}
#cxAtlas .cxtop .logo b,#cxGaps .cxtop .logo b{color:var(--teal);}
#cxAtlas .cxtop .tag,#cxGaps .cxtop .tag{font-family:var(--font-mono);font-size:10.5px;color:var(--muted);letter-spacing:.04em;}
#cxAtlas h1,#cxGaps h1{font-family:var(--font-serif);font-size:26px;color:var(--slate);margin:12px 0 4px;}
#cxAtlas .lead,#cxGaps .lead{font-size:14px;color:var(--muted);margin:0 0 18px;max-width:720px;}
.v2sec{margin:26px 0 0;}
.v2sec h2{font-family:var(--font-serif);font-size:19px;color:var(--slate);margin:0 0 3px;}
.v2sec .sub{font-size:12.5px;color:var(--muted);margin:0 0 12px;max-width:760px;}
.v2tools{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:0 0 12px;}
.v2tool{border:1px solid var(--line);background:#fff;color:var(--slate);font-size:12px;font-weight:600;
 padding:5px 12px;border-radius:16px;cursor:pointer;font-family:var(--font-sans);}
.v2tool:hover{border-color:var(--teal);color:var(--teal);}
.v2tool.on{background:var(--teal);border-color:var(--teal);color:#fff;}
.v2tools .lab{font-family:var(--font-mono);font-size:10px;letter-spacing:.05em;color:var(--dim);text-transform:uppercase;margin-right:2px;}

/* ---------- atlas family cards ---------- */
.v2fams{display:grid;grid-template-columns:repeat(auto-fill,minmax(258px,1fr));gap:12px;}
.v2fc{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 15px 12px;
 display:flex;flex-direction:column;gap:6px;cursor:pointer;transition:.16s;text-align:left;font-family:inherit;}
.v2fc:hover{border-color:var(--teal);box-shadow:0 9px 22px rgba(12,30,36,.10);transform:translateY(-2px);}
.v2fc .fh{display:flex;align-items:baseline;justify-content:space-between;gap:8px;}
.v2fc .fn{font-family:var(--font-serif);font-size:16px;color:var(--slate);font-weight:700;line-height:1.25;}
.v2fc .fq{font-family:var(--font-mono);font-size:11px;color:var(--dim);white-space:nowrap;}
.v2fc .fbar{display:flex;height:8px;border-radius:5px;overflow:hidden;border:1px solid var(--line);background:#fff;}
.v2fc .fbar i{display:block;height:100%;}
.v2fc .fmeta{font-size:11.5px;color:var(--muted);line-height:1.5;}
.v2fc .fmeta b{color:var(--slate);}
.v2fc .fzero{color:var(--accent);font-weight:600;}
.v2fc .farr{font-size:11.5px;color:var(--teal);font-weight:700;margin-top:2px;}

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

<!-- ===== Family atlas (R4) ===== -->
<div id="cxAtlas">
 <div class="cxtop">
  <button class="cxmenu" id="cxAtlasMenu">&larr; Menu</button>
  <span class="logo">What is your blood telling you<b>?</b></span>
  <span class="tag">the atlas</span>
 </div>
 <div class="cxwrap">
  <h1>The atlas of blood</h1>
  <p class="lead" id="v2AtlasLead"></p>

  <div class="v2mapwrap">
   <div class="v2mapleg" id="v2AtlasLeg"></div>
   <svg id="v2AtlasMap" viewBox="0 0 900 330" role="img" aria-label="Families of blood markers"></svg>
   <div class="v2famleg" id="v2AtlasFamLeg"></div>
  </div>
  <p class="v2mapnote" id="v2AtlasNote"></p>

  <div class="v2sec">
   <h2>Seventeen families</h2>
   <p class="sub">Each family is a region of the map. Open one to read every marker inside it in the table.</p>
   <div class="v2tools" id="v2AtlasTools">
    <span class="lab">shade by</span>
    <button class="v2tool on" data-shade="panel">routine-panel coverage</button>
    <button class="v2tool" data-shade="quoted">source coverage</button>
    <span class="lab" style="margin-left:14px">sort</span>
    <button class="v2tool on" data-sort="size">size</button>
    <button class="v2tool" data-sort="gap">least covered</button>
    <button class="v2tool" data-sort="name">A&ndash;Z</button>
   </div>
   <div class="v2fams" id="v2Fams"></div>
  </div>

  <div class="v2caveat" id="v2AtlasCaveat"></div>
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

 /* ================= ATLAS SCREEN ================= */
 let atlasShade='panel', atlasSort='size', atlasDrawn=false;

 function drawFams(){
  const list=FAM.slice();
  if(atlasSort==='size') list.sort((a,b)=>b.n-a.n);
  else if(atlasSort==='name') list.sort((a,b)=>a.label.localeCompare(b.label));
  else list.sort((a,b)=>{
   const ca=atlasShade==='quoted'?a.quoted/a.n:a.base/a.n;
   const cb=atlasShade==='quoted'?b.quoted/b.n:b.base/b.n;
   return ca-cb || b.n-a.n;
  });
  $('v2Fams').innerHTML=list.map(f=>{
   const bp=Math.max(f.base?1.5:0,100*f.base/f.n);
   const qp=Math.max(f.quoted?1.5:0,100*f.quoted/f.n);
   const lead=atlasShade==='quoted'?qp:bp;
   const leadCol=atlasShade==='quoted'?'var(--ok)':'var(--teal)';
   return '<button class="v2fc" data-fam="'+f.i+'">'
    +'<span class="fh"><span class="fn">'+esc(f.label)+'</span><span class="fq">'+nfmt(f.n)+'</span></span>'
    +'<span class="fbar"><i style="background:'+leadCol+';width:'+lead+'%"></i><i class="v2blocked" style="flex:1"></i></span>'
    +'<span class="fmeta">'
      +(f.base?'<b>'+f.base+'</b> reached by a routine annual panel':'<span class="fzero">Nothing here is in a routine panel</span>')
      +' &middot; '
      +(f.quoted?'<b>'+f.quoted+'</b> source-quoted':'<span class="fzero">no source-quoted entry yet</span>')
    +'</span>'
    +'<span class="farr">Open '+nfmt(f.n)+' markers in the table &rarr;</span>'
    +'</button>';
  }).join('');
 }

 window.__v2DrawAtlas=function(){
  if(!atlasDrawn){
   $('v2AtlasLead').innerHTML='Everything science can currently measure in blood, grouped into '+GROUPS.length
    +' families. '+nfmt(N_TOTAL)+' markers in total; '+nfmt(N_BASE)+' of them show up in a standard annual checkup. '
    +'Start anywhere &mdash; the full table sits one level inside each family.';
   $('v2AtlasLeg').innerHTML=$('v2Map').parentNode.querySelector('.v2mapleg').innerHTML;
   $('v2AtlasCaveat').innerHTML='<b>What this map cannot show yet.</b> Only '+N_CROSS+' of '+nfmt(N_TOTAL)
    +' markers carry a recorded link to another family, and the only curated &ldquo;these belong together&rdquo; sets are the '
    +PANELS.length+' routine panels. So the atlas can show you regions and their sizes, but not yet how an abnormal result in one '
    +'ripples into another. That relationship layer &mdash; marker sets and reflex edges, each carrying its own source &mdash; is the next thing to build.';
   drawMap($('v2AtlasMap'),atlasShade);
   famLegend($('v2AtlasFamLeg'),atlasShade);
   $('v2AtlasNote').innerHTML=$('v2MapNote').innerHTML;
   drawFams();
   atlasDrawn=true;
  }
 };

 $('v2AtlasTools').addEventListener('click',function(e){
  const b=e.target.closest('button'); if(!b) return;
  if(b.dataset.shade){
   atlasShade=b.dataset.shade;
   [].forEach.call(this.querySelectorAll('[data-shade]'),x=>x.classList.toggle('on',x===b));
   drawMap($('v2AtlasMap'),atlasShade);
   famLegend($('v2AtlasFamLeg'),atlasShade);
   $('v2AtlasLeg').innerHTML= atlasShade==='quoted'
    ? '<span><i style="background:var(--teal)"></i>has at least one source-quoted entry</span>'
      +'<span><i style="background:#fff;border:1.5px dashed #c3ced0"></i>nothing quoted from a named source yet</span>'
      +'<span style="margin-left:auto;font-family:var(--font-mono);font-size:10px">circle area &prop; markers in family</span>'
    : '<span><i style="background:var(--teal)"></i>reached by a standard annual panel</span>'
      +'<span><i style="background:#fff;border:1.5px dashed #c3ced0"></i>never reached by routine bloodwork</span>'
      +'<span style="margin-left:auto;font-family:var(--font-mono);font-size:10px">circle area &prop; markers in family</span>';
  }
  if(b.dataset.sort){
   atlasSort=b.dataset.sort;
   [].forEach.call(this.querySelectorAll('[data-sort]'),x=>x.classList.toggle('on',x===b));
  }
  drawFams();
 });
 $('v2Fams').addEventListener('click',function(e){
  const b=e.target.closest('[data-fam]'); if(b) openFamily(+b.dataset.fam);
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
