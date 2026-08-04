#!/usr/bin/env python3
"""
Builds index-v3.html — the ripple atlas.

Reads the catalogue payload out of index.html and emits a compact standalone
build (no 6,192-row table), so the file stays small and fast.

Flow:  annual panel marker -> concerns it can represent -> tests that would
       follow it up, with sourced relationship notes on how markers connect.

Every relationship note in REL below is a verbatim quote from a page that was
actually fetched, with its URL. Nothing here is paraphrased or inferred.

    python3 pipeline/build_v3.py
"""
import io, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "index.html")
DST  = os.path.join(ROOT, "index-v3.html")

s = io.open(SRC, encoding="utf8").read()
i = s.index('id="payload" type="application/json">') + len('id="payload" type="application/json">')
D = json.loads(s[i:s.index("</script>", i)])
TESTS, GROUPS, CONCERNS, CGROUPS, PANELS = D["tests"], D["groups"], D["concerns"], D["cgroups"], D["panels"]

def unquote(t):
    """Strip wrapping quote marks of any flavour.

    The catalogue stores descriptions already wrapped in quotes, and the panel
    renders them in a <q> element which adds its own — so the straight-quote
    strip we had left curly ones through and produced a doubled mark.
    """
    return (t or "").strip().strip('"\u201c\u201d\u2018\u2019\'').strip()



# ---------------------------------------------------------------------------
# 1. the 26 annual-panel markers, with a stable slug each
# ---------------------------------------------------------------------------
SLUG = {
 "Red Blood Cell count":"rbc", "White Blood Cell count":"wbc", "Platelet count":"plt",
 "Hemoglobin":"hgb", "Hematocrit":"hct", "Red Blood Cell indices":"mcv",
 "Complete Blood Count":"cbc",
 "Blood glucose":"glucose", "Calcium":"calcium",
 "Sodium [Moles/volume] in Serum or Plasma":"sodium",
 "Potassium [Mass/volume] in Serum or Plasma":"potassium",
 "Bicarbonate [Moles/volume] in Serum or Plasma":"bicarb",
 "Chloride [Moles/volume] in Serum or Plasma":"chloride",
 "Albumin":"albumin", "Total protein":"tp", "Alkaline phosphatase":"alp",
 "Alanine aminotransferase":"alt", "Aspartate aminotransferase":"ast",
 "Bilirubin":"bili", "Blood Urea Nitrogen":"bun", "Creatinine":"creat",
 "Total cholesterol":"tc", "LDL cholesterol":"ldl", "HDL cholesterol":"hdl",
 "Triglycerides":"trig", "Lipid panel (cholesterol)":"lipid",
}
ABBR = {"rbc":"RBC","wbc":"WBC","plt":"PLT","hgb":"Hgb","hct":"Hct","mcv":"MCV","cbc":"CBC",
 "glucose":"Glu","calcium":"Ca","sodium":"Na","potassium":"K","bicarb":"HCO₃","chloride":"Cl",
 "albumin":"Alb","tp":"TP","alp":"ALP","alt":"ALT","ast":"AST","bili":"TBIL","bun":"BUN",
 "creat":"Cr","tc":"TC","ldl":"LDL","hdl":"HDL","trig":"TG","lipid":"Lipids"}

idx_by_slug, markers = {}, {}
for k, t in enumerate(TESTS):
    if t.get("b") and t["n"] in SLUG:
        sl = SLUG[t["n"]]
        idx_by_slug[sl] = k
        markers[sl] = {
            "slug": sl, "name": t["n"], "abbr": ABBR[sl], "grp": GROUPS[t["g"]],
            "k": t.get("k") or [], "q": unquote(t.get("q")),
            "qs": t.get("qs") or "", "v": 1 if t.get("v") else 0,
            "url": (t.get("r") or [["", ""]])[0][0],
        }
missing = set(SLUG.values()) - set(markers)
assert not missing, "unmapped panel markers: %s" % missing

PANEL_ORDER = []
for p in PANELS:
    slugs = [SLUG[TESTS[l["i"]]["n"]] for l in p["linked"] if TESTS[l["i"]]["n"] in SLUG]
    PANEL_ORDER.append({"id": p["id"], "name": p["name"], "quote": p["quote"],
                        "src": p["src"], "url": p["url"], "slugs": slugs})

# ---------------------------------------------------------------------------
# 2. concerns, and the tests that would follow each one up
# ---------------------------------------------------------------------------
def analyte(name):
    """Collapse a LOINC long name to the thing being measured.

    LOINC carries one code per unit, specimen and method. The property sits in
    brackets — "Lead [Mass/volume] in Blood" — but the specimen and method are
    often bare text, so "Carboxyhemoglobin/Hemoglobin.total in Venous blood"
    and "... in Arterial blood" are two codes for one measurement. Stripping
    the bracket, the trailing "in <specimen>" and any "by <method>" leaves the
    analyte, which is what a reader means by "the test".
    """
    n = name.split("[")[0]
    n = re.sub(r"\s+by\s+.*$", "", n, flags=re.I)
    n = re.sub(r"\s+in\s+(?:the\s+)?[A-Z].*$", "", n)
    return n.strip(" /,") or name.strip()


base_idx = {k for k, t in enumerate(TESTS) if t.get("b")}
panel_concerns = sorted({c for m in markers.values() for c in m["k"]})

concerns = {}
for ci, c in enumerate(CONCERNS):
    tagged = [k for k, t in enumerate(TESTS) if ci in (t.get("k") or [])]
    outside = [k for k in tagged if k not in base_idx]
    outside.sort(key=lambda k: (-(TESTS[k].get("v") or 0), -(TESTS[k].get("t") or 0), len(TESTS[k]["n"])))
    # De-duplicate by analyte. LOINC carries one code per unit and method, so
    # "Lead [Presence] in Blood", "Lead [Mass/volume] in Blood" and
    # "Lead [Moles/volume] in Blood" are three rows for one test. Truncating at
    # the first "[" for display collapsed them into a list that read as
    # "Lead, Lead, Lead". Keep the best-ranked row per analyte and count the
    # rest as variants. `outside` is already in rank order, so the first
    # occurrence is the representative.
    byAnalyte = {}
    for k in outside:
        name = analyte(TESTS[k]["n"])
        if name in byAnalyte:
            byAnalyte[name]["nv"] += 1
            continue
        byAnalyte[name] = {
            "n": name,
            "a": TESTS[k].get("a") or "",
            "g": GROUPS[TESTS[k]["g"]],
            "v": 1 if TESTS[k].get("v") else 0,
            "u": (TESTS[k].get("r") or [["", ""]])[-1][0],
            "q": unquote(TESTS[k].get("q"))[:260],
            "qs": TESTS[k].get("qs") or "",
            "cs": TESTS[k].get("k") or [],
            "t": TESTS[k].get("t", 0),      # how commonly ordered: 18 common .. -3 obscure
            "nv": 1,
        }
    distinct = list(byAnalyte.values())

    # Family rollup over EVERY distinct marker, not just the carried top 40, so
    # the counts a reader sees are the true ones. `common` is the catalogue's
    # own ordering tier: 8 and above is a test a general clinician orders.
    fams, order_seen = {}, []
    for t in distinct:
        f = fams.get(t["g"])
        if not f:
            f = fams[t["g"]] = {"g": t["g"], "n": 0, "c": 0}
            order_seen.append(t["g"])
        f["n"] += 1
        if t["t"] >= 8:
            f["c"] += 1
    famList = sorted(fams.values(), key=lambda f: (-f["c"], -f["n"], f["g"]))

    concerns[ci] = {
        "id": c["id"], "label": c["label"], "grp": c["grp"],
        "inPanel": ci in panel_concerns,
        "nTagged": len(tagged),
        "nOutside": len(outside),        # LOINC rows outside the panel
        "nDistinct": len(distinct),      # distinct markers among them
        "from": [m["slug"] for m in markers.values() if ci in m["k"]],
        # 8 drawn on the map; up to 40 carried so the panel can expand.
        "next": distinct[:40],
        "fams": famList,
    }

# ---------------------------------------------------------------------------
# 3. RELATIONSHIP NOTES — every one a verbatim quote from a fetched page
# ---------------------------------------------------------------------------
def R(a, b, when, quote, src, url, kind="relationship"):
    return {"a": a, "b": b, "when": when, "q": quote, "s": src, "u": url, "k": kind}

MP = "MedlinePlus (NIH)"
REL = [
 R("hgb","hct","any",
   "Abnormal levels of red blood cells, hemoglobin, or hematocrit may be a sign of dehydration, anemia, heart disease, or too little iron in your body.",
   MP, "https://medlineplus.gov/lab-tests/complete-blood-count-cbc/"),
 R("hgb","ferritin","low",
   "You may also need this test if the results of other blood tests show that you have low levels of hematocrit (the amount of your blood that is made up of red blood cells) or hemoglobin (the protein that carries oxygen throughout the body).",
   MP, "https://medlineplus.gov/lab-tests/ferritin-blood-test/", "next-test"),
 R("mcv","ferritin","low",
   "If your red blood cells are smaller than normal, it may mean you have: Iron deficiency anemia, the most common form of anemia. It happens when you don't have enough iron in your body.",
   MP, "https://medlineplus.gov/lab-tests/red-blood-cell-rbc-indices/"),
 R("mcv","b12","high",
   "If your red blood cells are larger than normal, it may mean you have: Anemia caused by a vitamin B deficiency",
   MP, "https://medlineplus.gov/lab-tests/red-blood-cell-rbc-indices/"),
 R("bili","rbc","any",
   "Bilirubin is a yellowish substance made during your body's normal process of breaking down old red blood cells.",
   MP, "https://medlineplus.gov/lab-tests/bilirubin-blood-test/"),
 R("bili","alt","any",
   "If your liver is healthy, it will remove most of the bilirubin from your body through your bile ducts (the tubes that carry bile from your liver).",
   MP, "https://medlineplus.gov/lab-tests/bilirubin-blood-test/"),
 R("albumin","alt","any",
   "This is the main protein in your blood. It's made in your liver.",
   MP, "https://medlineplus.gov/lab-tests/comprehensive-metabolic-panel-cmp/"),
 R("albumin","creat","abnormal",
   "An albumin blood test is used to check your general health and nutrition, and to see how well your liver and kidneys are working. If your liver is damaged or you're not well nourished, your liver may not make enough albumin. If your kidneys are damaged, they may let albumin pass from your blood into your urine (pee).",
   MP, "https://medlineplus.gov/lab-tests/albumin-blood-test/"),
 R("tp","albumin","any",
   "There are two major types of protein in the blood: albumin and globulin. Albumin makes up most of the protein in the blood, while the rest are called globulins.",
   MP, "https://medlineplus.gov/lab-tests/total-protein-and-albumin-globulin-a-g-ratio/"),
 R("alt","ast","any",
   "Your ALT is usually measured along with another liver enzyme called AST as part of a liver function panel. Since ALT is mostly found in the liver, an ALT test checks more specifically for liver damage.",
   MP, "https://medlineplus.gov/lab-tests/alt-blood-test/"),
 R("ast","alt","any",
   "It is found mainly in your liver but also in your heart, muscles, and other tissues.",
   MP, "https://medlineplus.gov/lab-tests/ast-test/"),
 R("alp","alt","high",
   "ALP is found in all your body tissues, but higher amounts can be found in your liver, bile ducts, and bones. Each part of your body makes a different type of ALP.",
   MP, "https://medlineplus.gov/lab-tests/alkaline-phosphatase/"),
 R("alp","liverpanel","high",
   "If your test results show high ALP levels, your provider may order other tests to help figure out what's causing the problem.",
   MP, "https://medlineplus.gov/lab-tests/alkaline-phosphatase/", "next-test"),
 R("calcium","albumin","any",
   "\"Bound calcium\" is attached to proteins in your blood. \"Free calcium\" is not attached to proteins. It's also called ionized calcium. This form of blood calcium is active in many body functions.",
   MP, "https://medlineplus.gov/lab-tests/calcium-blood-test/"),
 R("calcium","ionized","abnormal",
   "An ionized calcium test is more difficult to do, so it's usually ordered if the results of a total calcium test aren't normal.",
   MP, "https://medlineplus.gov/lab-tests/calcium-blood-test/", "next-test"),
 R("calcium","tp","low",
   "Results from a total calcium test that are lower than normal (hypocalcemia) may be a sign of: Low blood protein levels, which may be caused by liver disease or malnutrition",
   MP, "https://medlineplus.gov/lab-tests/calcium-blood-test/"),
 R("calcium","pth","abnormal",
   "You may need a PTH test if you: Had a calcium test that showed your blood calcium levels aren't normal.",
   MP, "https://medlineplus.gov/lab-tests/parathyroid-hormone-pth-test/", "next-test"),
 R("calcium","phosphate","any",
   "When blood calcium levels increase, phosphate levels decrease. And when calcium levels decrease, phosphate levels increase.",
   MP, "https://medlineplus.gov/lab-tests/phosphate-in-blood/"),
 R("calcium","vitd","any",
   "Vitamin D helps your body absorb calcium to build healthy bones and teeth.",
   MP, "https://medlineplus.gov/lab-tests/vitamin-d-test/"),
 R("calcium","magnesium","abnormal",
   "A magnesium blood test may also be used to help find the cause of abnormal levels of other minerals, including calcium, potassium, and phosphorus. That's because magnesium plays a role in how your body absorbs these minerals.",
   MP, "https://medlineplus.gov/lab-tests/magnesium-blood-test/", "next-test"),
 R("creat","bun","any",
   "Creatinine blood levels measured as part of a CMP or a BMP may be compared with the level of BUN (blood urea nitrogen) that's measured in the same test. This can help find out the cause of a kidney problem.",
   MP, "https://medlineplus.gov/lab-tests/creatinine-test/"),
 R("creat","egfr","any",
   "Creatinine levels in blood are often used to calculate how fast your kidneys filter waste out of your blood. This is called an estimated glomerular filtration rate (eGFR).",
   MP, "https://medlineplus.gov/lab-tests/creatinine-test/"),
 R("creat","kidney","abnormal",
   "If your results are abnormal, a single high creatinine test can't diagnose a specific condition. You will likely need to be retested and/or have other tests, too.",
   MP, "https://medlineplus.gov/lab-tests/creatinine-test/", "next-test"),
 R("glucose","a1c","high",
   "If you're checking it at home, you are measuring what your blood glucose level is at that time. An A1C test gives you an average level of your blood glucose level over the past two to three months.",
   MP, "https://medlineplus.gov/lab-tests/hemoglobin-a1c-hba1c-test/", "next-test"),
 R("ldl","trig","any",
   "The LDL listed on your results may say \"calculated.\" This means that your LDL level is an estimate based on your total cholesterol, HDL, and triglycerides.",
   MP, "https://medlineplus.gov/lab-tests/cholesterol-levels/"),
 R("trig","vldl","any",
   "VLDL isn't usually included in routine cholesterol tests because it's difficult to measure. Because VLDL contains a certain percentage of triglycerides, a lab can use your triglycerides level to estimate your VLDL level.",
   MP, "https://medlineplus.gov/lab-tests/cholesterol-levels/"),
 R("trig","apob","high",
   "If your blood triglyceride levels are borderline, your provider may order another blood test called apolipoprotein B or \"apo B.\" The results of this test can help your provider understand how high your risk of heart and blood vessel problems may be.",
   MP, "https://medlineplus.gov/lab-tests/triglycerides-test/", "next-test"),
 R("cbc","panel","any",
   "A complete blood count is only one tool your provider uses to learn about your health. Your provider will consider your medical history, symptoms, and other factors to make a diagnosis. You may also need additional tests.",
   MP, "https://medlineplus.gov/lab-tests/complete-blood-count-cbc/"),
 R("panel","panel","abnormal",
   "In general, if you have one or more results that aren't normal, it may be a sign of a health condition. For example, high blood glucose may be a sign of diabetes. You will likely need more tests to confirm or rule out a specific diagnosis.",
   MP, "https://medlineplus.gov/lab-tests/comprehensive-metabolic-panel-cmp/"),
]
# names for the off-panel markers a relationship can point at
OFFPANEL = {
 "ferritin":"Ferritin", "b12":"Vitamin B12", "ionized":"Ionized calcium", "pth":"Parathyroid hormone",
 "phosphate":"Phosphate", "vitd":"Vitamin D", "magnesium":"Magnesium", "egfr":"Estimated GFR",
 "a1c":"Hemoglobin A1c", "vldl":"VLDL cholesterol", "apob":"Apolipoprotein B",
 "liverpanel":"Liver function tests", "kidney":"Further kidney tests", "panel":"Your annual panel",
}
for r in REL:
    for side in ("a", "b"):
        assert r[side] in markers or r[side] in OFFPANEL, "unknown marker %r" % r[side]

# ---------------------------------------------------------------------------
PAY = {
 "panels": PANEL_ORDER,
 "markers": markers,
 "concerns": concerns,
 "cgroups": CGROUPS,
 "rel": REL,
 "off": OFFPANEL,
 "meta": {
   "total": len(TESTS), "base": len(base_idx),
   "nConcerns": len(CONCERNS), "panelConcerns": len(panel_concerns),
   "quoted": sum(1 for t in TESTS if t.get("v")),
   "offPanelForPanelConcerns": sum(concerns[c]["nOutside"] for c in panel_concerns),
 },
}

TPL = io.open(os.path.join(ROOT, "pipeline", "v3_template.html"), encoding="utf8").read()
out = TPL.replace("__PAYLOAD__", json.dumps(PAY, ensure_ascii=False, separators=(",", ":")))
io.open(DST, "w", encoding="utf8").write(out)

m = PAY["meta"]
print("index-v3.html  %.0f KB" % (len(out) / 1024.0))
print("  %d panel markers · %d panels" % (len(markers), len(PANEL_ORDER)))
print("  %d concerns (%d reachable from the annual panel)" % (m["nConcerns"], m["panelConcerns"]))
print("  %d sourced relationship notes" % len(REL))
print("  %s follow-up tests sit outside the panel for those concerns" % format(m["offPanelForPanelConcerns"], ","))
print("  %d distinct follow-up markers carried (cap 40 per concern)" % sum(len(c["next"]) for c in concerns.values()))
print("  families per concern: median %d, max %d" % (sorted(len(c["fams"]) for c in concerns.values())[len(concerns)//2], max(len(c["fams"]) for c in concerns.values())))
print("  commonly-ordered markers per concern: median %d, max %d" % (
    sorted(sum(f["c"] for f in c["fams"]) for c in concerns.values())[len(concerns)//2],
    max(sum(f["c"] for f in c["fams"]) for c in concerns.values())))
print("  de-duplicated from %d LOINC rows" % sum(sum(t["nv"] for t in c["next"]) for c in concerns.values()))
