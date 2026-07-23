/* ================= CONDITION EXPLORER MODULE (cx-*) ================= */
/* Injected into index.html. Namespaced under #cxApp with cx- classes so it
   cannot collide with the existing dashboard's CSS/DOM. Data authored from
   verbatim MedlinePlus/NIH quotes; connective logic flagged "reasoned". */
(function(){
"use strict";

/* ---- concern (feeling) -> conditions. Each mapping is backed by a sourced
   symptom in the target condition's src list. This is the Route-1 spine. ---- */
const CONCERNS=[
 {id:"fatigue", label:"Tired / low energy",       conds:["ida","b12","hypo","hyper","t2d","ckd","liver"]},
 {id:"cold",    label:"Always cold",              conds:["ida","hypo"]},
 {id:"pale",    label:"Pale skin",                conds:["ida","b12"]},
 {id:"breath",  label:"Short of breath",          conds:["ida","b12"]},
 {id:"tingling",label:"Tingling or numbness",     conds:["b12","t2d"]},
 {id:"memory",  label:"Brain fog / forgetful",    conds:["b12"]},
 {id:"mood",    label:"Low mood / irritable",     conds:["b12","hypo","hyper"]},
 {id:"weightg", label:"Weight gain",              conds:["hypo"]},
 {id:"weightl", label:"Losing weight unexpectedly",conds:["hyper","t2d"]},
 {id:"dryhair", label:"Dry skin / thinning hair", conds:["hypo"]},
 {id:"heat",    label:"Can't tolerate heat",      conds:["hyper"]},
 {id:"palp",    label:"Racing / irregular heartbeat",conds:["hyper"]},
 {id:"thirst",  label:"Very thirsty",             conds:["t2d"]},
 {id:"pee",     label:"Urinating more or less",   conds:["t2d","ckd"]},
 {id:"blurry",  label:"Blurry vision",            conds:["t2d"]},
 {id:"swelling",label:"Swollen legs / ankles",    conds:["ckd"]},
 {id:"jaundice",label:"Yellow skin or eyes",      conds:["liver"]},
 {id:"itch",    label:"Itchy skin",               conds:["ckd","liver"]},
 {id:"jointsw", label:"Sudden hot, swollen joint",conds:["gout"]},
 {id:"bonepain",label:"Bone pain",                conds:["vitd"]},
 {id:"muscle",  label:"Muscle weakness / aches",  conds:["vitd","hyper"]},
 {id:"fever",   label:"Unexplained fever",        conds:["inflam"]},
 {id:"stiff",   label:"Joint stiffness / pain",   conds:["inflam","gout","hypo","vitd"]}
];

/* helper for a NHLBI/MedlinePlus source object */
const CONDITIONS=[
/* 1 */ {
 id:"ida", label:"Iron-deficiency anemia", grp:"Energy & blood",
 one:"Not enough iron to build healthy red blood cells — the most common type of anemia.",
 symptoms:["Fatigue","Dizziness or lightheadedness","Cold hands and feet","Pale skin","Shortness of breath","Restless legs (if untreated)"],
 markers:[
  {slug:"hemoglobin",name:"Hemoglobin",abbr:"Hgb",panel:true,step:"screen",abn:"low",sig:"Low hemoglobin is the core sign of anemia — too little oxygen-carrying protein."},
  {slug:"hematocrit",name:"Hematocrit",abbr:"Hct",panel:true,step:"screen",abn:"low",sig:"The share of blood made of red cells; falls alongside hemoglobin."},
  {slug:"mcv",name:"Mean corpuscular volume",abbr:"MCV",panel:true,step:"screen",abn:"low",reasoned:true,sig:"Red-cell size. In iron deficiency the cells typically run small (low MCV)."},
  {slug:"ferritin",name:"Ferritin",abbr:"serum ferritin",panel:false,step:"confirm",abn:"low",sig:"Stored iron. Low ferritin is the most specific confirmation of depleted iron stores."},
  {slug:"iron",name:"Serum iron",abbr:"Fe",panel:false,step:"confirm",abn:"low",sig:"Iron circulating right now; low in iron deficiency."},
  {slug:"tibc",name:"Total iron-binding capacity",abbr:"TIBC",panel:false,step:"confirm",abn:"high",sig:"How much the blood can carry; rises as stores empty, so saturation drops."}
 ],
 confirm:"ferritin", support:["hemoglobin"],
 reads:{
  strong:"Low iron stores (low ferritin) with low hemoglobin is the classic picture of iron-deficiency anemia. Worth taking to a clinician, who can look for <em>why</em> iron is low.",
  supportive:"Low ferritin points to depleted iron stores, which fits iron deficiency even before anemia is obvious. A clinician can confirm and look for a cause.",
  partial:"The signals are mixed — some fit iron deficiency and some don't. Exactly the kind of pattern that needs a clinician, not an app.",
  against:"These results don't fit an iron-deficiency pattern (iron stores look adequate). If you still feel tired, the cause is likely elsewhere."
 },
 src:[
  {k:"q",quote:"To help diagnose iron-deficiency anemia, your doctor will order a blood test to check your complete blood count (CBC), hemoglobin levels, blood iron levels, and ferritin levels.",who:"NHLBI — Iron-Deficiency Anemia",url:"https://www.nhlbi.nih.gov/health/anemia/iron-deficiency-anemia"},
  {k:"q",quote:"More serious iron-deficiency anemia may cause common symptoms of anemia, such as tiredness, shortness of breath, or chest pain. Other symptoms include: Fatigue; Dizziness or lightheadedness; Cold hands and feet; Pale skin.",who:"NHLBI — Iron-Deficiency Anemia",url:"https://www.nhlbi.nih.gov/health/anemia/iron-deficiency-anemia"},
  {k:"q",quote:"Lower than normal ferritin levels may mean you have iron deficiency anemia, or another condition related to low iron levels.",who:"MedlinePlus — Ferritin Blood Test",url:"https://medlineplus.gov/lab-tests/ferritin-blood-test/"},
  {k:"inf",quote:"Treating the CBC as the screen and ferritin as the confirm, and reading MCV as 'small cells,' is standard clinical practice rather than a single quoted sentence — so it is flagged reasoned.",who:"Reasoned from the sourced facts above",url:""}
 ]
},
/* 2 */ {
 id:"b12", label:"Vitamin B12–deficiency anemia", grp:"Energy & blood",
 one:"Too little vitamin B12 to make healthy red blood cells — and, untreated, a nerve problem too.",
 symptoms:["Fatigue","Paleness","Shortness of breath","Dizziness","Tingling feelings or pain","Confusion / forgetfulness","Glossitis (sore, smooth tongue)"],
 markers:[
  {slug:"hemoglobin",name:"Hemoglobin",abbr:"Hgb",panel:true,step:"screen",abn:"low",sig:"A complete blood count measures hemoglobin; low hemoglobin signals anemia."},
  {slug:"mcv",name:"Mean corpuscular volume",abbr:"MCV",panel:true,step:"screen",abn:"high",reasoned:true,sig:"Red-cell size. In B12 deficiency the cells typically run large (high MCV) — the opposite of iron deficiency."},
  {slug:"b12",name:"Vitamin B12 level",abbr:"cobalamin",panel:false,step:"confirm",abn:"low",sig:"Measures B12 in the blood. Low confirms deficiency — though a normal level doesn't fully rule it out."},
  {slug:"mma",name:"Methylmalonic acid",abbr:"MMA",panel:false,step:"cause",abn:"high",reasoned:true,sig:"Rises when B12 is functionally low; sometimes used when the B12 level is borderline."}
 ],
 confirm:"b12", support:["hemoglobin"],
 reads:{
  strong:"Low hemoglobin with a low vitamin B12 level fits B12-deficiency anemia. A clinician can confirm and, importantly, find the cause — often a problem absorbing B12, not diet.",
  supportive:"A low vitamin B12 level points to deficiency even before anemia is obvious. Worth confirming with a clinician.",
  partial:"Mixed signals. NHLBI notes B12 can read normal even when the deficiency is real, so a normal level doesn't fully rule it out — a clinician's call.",
  against:"These results don't fit a B12-deficiency pattern. If symptoms persist, the cause is likely elsewhere."
 },
 src:[
  {k:"q",quote:"Vitamin B12–deficiency anemia … develops when your body can't make enough healthy red blood cells because it doesn't have enough vitamin B12.",who:"NHLBI — Vitamin B12–Deficiency Anemia",url:"https://www.nhlbi.nih.gov/health/anemia/vitamin-b12-deficiency-anemia"},
  {k:"q",quote:"You may have the typical symptoms of anemia at first, such as fatigue, paleness, shortness of breath, headaches, or dizziness. If left untreated, you may start to notice brain and nervous system symptoms … Tingling feelings or pain … Confusion, slower thinking, forgetfulness, and memory loss … Glossitis, which is a painful, smooth, red tongue.",who:"NHLBI — Vitamin B12–Deficiency Anemia",url:"https://www.nhlbi.nih.gov/health/anemia/vitamin-b12-deficiency-anemia"},
  {k:"q",quote:"To screen for vitamin B12–deficiency anemia, your healthcare provider may order blood tests to see whether you have low hemoglobin or vitamin B12 levels … You may still have the condition even if your vitamin B12 levels are normal.",who:"NHLBI — Vitamin B12–Deficiency Anemia",url:"https://www.nhlbi.nih.gov/health/anemia/vitamin-b12-deficiency-anemia"},
  {k:"inf",quote:"That B12-deficiency red cells run large (high MCV) and that methylmalonic acid rises when B12 is functionally low are standard clinical readings not stated in the quoted NHLBI text — so both are flagged reasoned.",who:"Reasoned from the sourced facts above",url:""}
 ]
},
/* 3 */ {
 id:"hypo", label:"Hypothyroidism (underactive thyroid)", grp:"Hormones & metabolism",
 one:"A thyroid making too little hormone, so many body functions slow down.",
 symptoms:["Fatigue","Weight gain","Very sensitive to cold","Joint and muscle pain","Dry skin","Dry, thinning hair","Depression","Constipation"],
 markers:[
  {slug:"tsh",name:"Thyroid-stimulating hormone",abbr:"TSH",panel:false,step:"screen",abn:"high",sig:"When thyroid hormone is low, the pituitary makes more TSH to push the thyroid — so a high TSH is the first flag."},
  {slug:"ft4",name:"Free thyroxine",abbr:"Free T4",panel:false,step:"confirm",abn:"low",sig:"The thyroid hormone itself. Low free T4 with a high TSH confirms an underactive thyroid."},
  {slug:"tpo",name:"Thyroid antibodies",abbr:"TPO / anti-thyroid",panel:false,step:"cause",abn:"high",sig:"Points to the cause — Hashimoto's disease, the most common cause of hypothyroidism."}
 ],
 confirm:"ft4", support:["tsh"],
 reads:{
  strong:"A high TSH with a low free T4 is the pattern of an underactive thyroid. A clinician can confirm and check antibodies to see if it's Hashimoto's, the most common cause.",
  supportive:"A low free T4 fits an underactive thyroid; pairing it with TSH sharpens the picture. Worth a clinician's review.",
  partial:"A raised TSH with a still-normal free T4 can mean an early or 'subclinical' underactive thyroid — exactly the borderline a clinician should interpret.",
  against:"Thyroid levels look in range here; hypothyroidism is unlikely to be the explanation for how you feel."
 },
 src:[
  {k:"q",quote:"A TSH test is used to find out how well your thyroid is working. It can tell if you have hyperthyroidism (too much thyroid hormone) or hypothyroidism (too little thyroid hormone) in your blood. But a TSH test can't show what is causing a thyroid problem.",who:"MedlinePlus — TSH Test",url:"https://medlineplus.gov/lab-tests/tsh-thyroid-stimulating-hormone-test/"},
  {k:"q",quote:"If the thyroid hormone level in your blood is too low, your pituitary gland makes larger amounts of TSH to tell your thyroid to work harder.",who:"MedlinePlus — TSH Test",url:"https://medlineplus.gov/lab-tests/tsh-thyroid-stimulating-hormone-test/"},
  {k:"q",quote:"Hypothyroidism … The symptoms may include: Fatigue; Weight gain; Being very sensitive to cold; Joint and muscle pain; Dry skin; Dry, thinning hair … Depression; Constipation. Because hypothyroidism develops slowly, many people don't notice symptoms of the disease for months or even years.",who:"MedlinePlus — TSH Test",url:"https://medlineplus.gov/lab-tests/tsh-thyroid-stimulating-hormone-test/"},
  {k:"q",quote:"If your test results aren't normal, your provider will probably order other thyroid blood tests … T4 thyroid hormone test … Thyroid antibodies test to help diagnose an autoimmune thyroid disorder, such as … Hashimoto's disease, that the most common cause of hypothyroidism.",who:"MedlinePlus — TSH Test",url:"https://medlineplus.gov/lab-tests/tsh-thyroid-stimulating-hormone-test/"},
  {k:"inf",quote:"Ordering TSH as the screen, free T4 as the confirm, and antibodies as the cause-finder is standard practice assembled from the sourced facts above — a sequence, not a single quote — so it is flagged reasoned.",who:"Reasoned from the sourced facts above",url:""}
 ]
},
/* 4 */ {
 id:"hyper", label:"Hyperthyroidism (overactive thyroid)", grp:"Hormones & metabolism",
 one:"A thyroid making more hormone than the body needs, so functions speed up.",
 symptoms:["Nervousness or irritability","Fatigue","Muscle weakness","Trouble tolerating heat","Trouble sleeping","Tremor in the hands","Rapid, irregular heartbeat","Weight loss"],
 markers:[
  {slug:"tsh",name:"Thyroid-stimulating hormone",abbr:"TSH",panel:false,step:"screen",abn:"low",sig:"With too much thyroid hormone, the pituitary makes little or no TSH — so a low TSH is the first flag."},
  {slug:"ft4",name:"Free thyroxine",abbr:"Free T4",panel:false,step:"confirm",abn:"high",sig:"The thyroid hormone itself. High free T4 (or T3) with a low TSH points to an overactive thyroid."},
  {slug:"trab",name:"Thyroid antibodies (TRAb)",abbr:"TRAb",panel:false,step:"cause",abn:"high",sig:"Points to the cause — Graves' disease, the most common cause of hyperthyroidism."}
 ],
 confirm:"ft4", support:["tsh"],
 reads:{
  strong:"A low TSH with a high free T4 is the pattern of an overactive thyroid. A clinician can confirm and check antibodies for Graves' disease, the most common cause.",
  supportive:"A high free T4 fits an overactive thyroid; pairing it with a low TSH sharpens the picture. Worth a clinician's review.",
  partial:"A low TSH with a still-normal free T4 can be an early or 'subclinical' overactive thyroid — a borderline a clinician should interpret.",
  against:"Thyroid levels look in range here; hyperthyroidism is unlikely to be the explanation for how you feel."
 },
 src:[
  {k:"q",quote:"Hyperthyroidism, or overactive thyroid, happens when your thyroid gland makes more thyroid hormones than your body needs.",who:"MedlinePlus / NIDDK — Hyperthyroidism",url:"https://medlineplus.gov/hyperthyroidism.html"},
  {k:"q",quote:"The symptoms of hyperthyroidism can vary from person to person and may include: Nervousness or irritability; Fatigue; Muscle weakness; Trouble tolerating heat; Trouble sleeping; Tremor, usually in your hands; Rapid and irregular heartbeat; … Weight loss; Mood swings.",who:"MedlinePlus / NIDDK — Hyperthyroidism",url:"https://medlineplus.gov/hyperthyroidism.html"},
  {k:"q",quote:"If your thyroid hormone level is too high, the pituitary gland makes little or no TSH.",who:"MedlinePlus — TSH Test",url:"https://medlineplus.gov/lab-tests/tsh-thyroid-stimulating-hormone-test/"},
  {k:"q",quote:"In general, T4 results that are higher than normal may be a sign of: Hyperthyroidism … A T4 test alone can't provide enough information to diagnose thyroid problems. So, it's usually done with a TSH blood test.",who:"MedlinePlus — Thyroxine (T4) Test",url:"https://medlineplus.gov/lab-tests/thyroxine-t4-test/"},
  {k:"q",quote:"If not treated, hyperthyroidism can cause serious problems with your heart, bones, muscles, menstrual cycle, and fertility.",who:"MedlinePlus / NIDDK — Hyperthyroidism",url:"https://medlineplus.gov/hyperthyroidism.html"},
  {k:"inf",quote:"Sequencing TSH as screen, free T4 as confirm, and TRAb as cause-finder is standard practice assembled from the sourced facts — a sequence, not one quote — so it is flagged reasoned.",who:"Reasoned from the sourced facts above",url:""}
 ]
},
/* 5 */ {
 id:"t2d", label:"Type 2 diabetes (and prediabetes)", grp:"Hormones & metabolism",
 one:"Blood sugar running higher than normal because cells don't respond well to insulin. Often silent for years.",
 symptoms:["Feeling very thirsty","Urinating more often","Feeling very hungry","Fatigue","Blurry vision","Numbness or tingling in the feet or hands","Losing weight without trying"],
 markers:[
  {slug:"glucose",name:"Fasting blood glucose",abbr:"FPG",panel:true,step:"screen",abn:"high",sig:"Blood sugar after fasting; part of a routine metabolic panel. A high value is the first flag."},
  {slug:"hba1c",name:"Hemoglobin A1C",abbr:"A1C",panel:false,step:"confirm",abn:"high",sig:"Average blood sugar over ~3 months, in one non-fasting sample. Diagnoses prediabetes and diabetes."},
  {slug:"ogtt",name:"Oral glucose tolerance test",abbr:"OGTT",panel:false,step:"confirm",abn:"high",sig:"Sometimes used to confirm prediabetes or type 2 diabetes."}
 ],
 confirm:"hba1c", support:["glucose"],
 reads:{
  strong:"A high fasting glucose together with a high A1C fits type 2 diabetes. A1C at or above 6.5% is the diabetes range; 5.7–6.4% is prediabetes. A clinician confirms and guides next steps.",
  supportive:"A raised A1C points to prediabetes or diabetes (5.7–6.4% prediabetes; 6.5%+ diabetes). Worth confirming with a clinician.",
  partial:"A high fasting glucose with a still-normal A1C is a borderline worth repeating and reviewing with a clinician.",
  against:"Glucose and A1C look in the normal range here; diabetes is unlikely to explain how you feel."
 },
 src:[
  {k:"q",quote:"Type 2 diabetes. This is the most common form of diabetes. If you have type 2 diabetes, your body may still be able to make insulin, but your cells don't respond well to insulin.",who:"MedlinePlus — Diabetes",url:"https://medlineplus.gov/diabetes.html"},
  {k:"q",quote:"The symptoms of diabetes may include: Feeling very thirsty; Feeling very hungry; Urinating (peeing) more often, including at night; Fatigue; Blurry vision; Numbness or tingling in the feet or hands; Sores that do not heal; Losing weight without trying. With type 2 diabetes, the symptoms often develop slowly, over several years … so mild that you might not even notice them.",who:"MedlinePlus — Diabetes",url:"https://medlineplus.gov/diabetes.html"},
  {k:"q",quote:"A hemoglobin A1C (HbA1c) test provides information about your average blood glucose levels over the past 3 months … An A1C test can diagnose prediabetes and diabetes.",who:"MedlinePlus — Blood Glucose Test",url:"https://medlineplus.gov/lab-tests/blood-glucose-test/"},
  {k:"q",quote:"A1C: A normal level is below 5.7% … Prediabetes is between 5.7 to 6.4% … Type 2 diabetes is above 6.5%. Fasting plasma glucose: A normal level is 99 or below … Prediabetes is 100 to 125 … Type 2 diabetes is 126 and above.",who:"MedlinePlus — Prediabetes",url:"https://medlineplus.gov/prediabetes.html"},
  {k:"q",quote:"Over time, high blood glucose levels can lead to serious health conditions … If you have prediabetes, you are more likely to develop type 2 diabetes, heart disease, and stroke.",who:"MedlinePlus — Diabetes / Prediabetes",url:"https://medlineplus.gov/prediabetes.html"},
  {k:"inf",quote:"Using fasting glucose as the screen and A1C as the confirm is one common route (the sources present them as alternative diagnostic tests); the ordering is reasoned.",who:"Reasoned from the sourced facts above",url:""}
 ]
},
/* 6 */ {
 id:"chol", label:"High cholesterol", grp:"Heart & circulation",
 one:"Too much cholesterol in the blood, which can build up in arteries. Usually has no symptoms at all.",
 silent:"There are usually no signs or symptoms of high cholesterol — it's found on a blood test, not by how you feel.",
 symptoms:["(usually none — high cholesterol is silent)","Found on a routine blood test","Risk rises quietly over years"],
 markers:[
  {slug:"totchol",name:"Total cholesterol",abbr:"total",panel:true,step:"screen",abn:"high",sig:"All the cholesterol in your blood; part of the routine lipid panel."},
  {slug:"ldl",name:"LDL cholesterol",abbr:"LDL",panel:true,step:"confirm",abn:"high",sig:"The 'bad' cholesterol that builds plaque. A healthy adult target is under 100 mg/dL."},
  {slug:"hdl",name:"HDL cholesterol",abbr:"HDL",panel:true,step:"screen",abn:"low",sig:"The 'good' cholesterol; here, lower is worse (under 40 mg/dL is considered low)."},
  {slug:"trig",name:"Triglycerides",abbr:"TG",panel:true,step:"screen",abn:"high",sig:"A blood fat measured in the same panel; high levels add to risk."}
 ],
 confirm:"ldl", support:["totchol"],
 reads:{
  strong:"LDL above the healthy target (under 100 mg/dL for adults), with a high total cholesterol, is the high-cholesterol pattern. It's silent but raises heart-disease risk — a clinician weighs it with your other risks.",
  supportive:"An LDL above the adult target of 100 mg/dL is the number that most drives risk. Worth reviewing with a clinician.",
  partial:"Some lipid numbers are off and some aren't — a clinician reads the whole panel together with your other risk factors.",
  against:"These lipid numbers are within the healthy targets. High cholesterol isn't indicated here."
 },
 src:[
  {k:"q",quote:"If you have too much cholesterol in your blood, it can combine with other substances in the blood to form plaque. Plaque sticks to the walls of your arteries. This buildup of plaque is known as atherosclerosis.",who:"MedlinePlus — Cholesterol",url:"https://medlineplus.gov/cholesterol.html"},
  {k:"q",quote:"There are usually no signs or symptoms that you have high cholesterol. A blood test can measure your cholesterol levels.",who:"MedlinePlus — Cholesterol",url:"https://medlineplus.gov/cholesterol.html"},
  {k:"q",quote:"A cholesterol test is a blood test that measures the amount of cholesterol and triglycerides (a type of fat) in your blood. Other names for a cholesterol test: Lipid profile, Lipid panel.",who:"MedlinePlus — Cholesterol Levels",url:"https://medlineplus.gov/lab-tests/cholesterol-levels/"},
  {k:"q",quote:"Men age 20 or older … LDL | Less than 100 mg/dL … HDL | Greater than or equal to 60 mg/dL is best. Levels less than 40 mg/dL are considered low.",who:"MedlinePlus — Cholesterol Levels (healthy-level table)",url:"https://medlineplus.gov/lab-tests/cholesterol-levels/"},
  {k:"q",quote:"High cholesterol can lead to heart disease, the number one cause of death in the United States.",who:"MedlinePlus — Cholesterol Levels",url:"https://medlineplus.gov/lab-tests/cholesterol-levels/"},
  {k:"inf",quote:"MedlinePlus frames its numbers as healthy-level targets rather than a single 'high' cutoff, and treats the lipid panel as one test; calling LDL the confirm and reading values 'above target' is reasoned.",who:"Reasoned from the sourced facts above",url:""}
 ]
},
/* 7 */ {
 id:"vitd", label:"Vitamin D deficiency", grp:"Bones & joints",
 one:"Not enough vitamin D to keep bones and muscles healthy; can be low even without symptoms.",
 symptoms:["Bone pain","Muscle weakness or aches","Soft or deformed bones","Weak bones and fractures","(can be low with no symptoms at all)"],
 markers:[
  {slug:"vitd",name:"25-hydroxyvitamin D",abbr:"25(OH)D",panel:false,step:"confirm",abn:"low",sig:"The blood form that best reflects your vitamin D. Reported as Deficient / Insufficient / Sufficient — not a routine test for everyone."}
 ],
 confirm:"vitd", support:[],
 reads:{
  strong:"A low 25(OH)D means your vitamin D is deficient — low enough to affect bones and general health. A clinician can advise on replacement and check for a cause.",
  supportive:"A low 25(OH)D means your vitamin D is deficient — low enough to affect bones and general health. A clinician can advise on replacement and check for a cause.",
  partial:"A borderline vitamin D result is best interpreted by a clinician alongside your bone health and risk factors.",
  against:"Your vitamin D looks sufficient. Deficiency isn't indicated here."
 },
 src:[
  {k:"q",quote:"Vitamin D deficiency means that your body is not getting enough vitamin D to stay healthy.",who:"MedlinePlus — Vitamin D Deficiency",url:"https://medlineplus.gov/vitaminddeficiency.html"},
  {k:"q",quote:"Have signs or symptoms of a condition that may be related to vitamin D deficiency such as: Bone pain; Muscle weakness or aches; Soft or deformed bones; Weak bones and fractures (broken bones).",who:"MedlinePlus — Vitamin D Test",url:"https://medlineplus.gov/lab-tests/vitamin-d-test/"},
  {k:"q",quote:"Most vitamin D blood tests measure the level of 25(OH)D in your blood because that's the most accurate way to see if you have enough vitamin D … Routine vitamin D testing is not recommended for everyone.",who:"MedlinePlus — Vitamin D Test",url:"https://medlineplus.gov/lab-tests/vitamin-d-test/"},
  {k:"q",quote:"Deficient, which means very low vitamin D levels that are likely to affect your bones and general health … Insufficient, which means low vitamin D levels that may weaken your bones and affect your health, even if you don't have symptoms.",who:"MedlinePlus — Vitamin D Test (result categories)",url:"https://medlineplus.gov/lab-tests/vitamin-d-test/"},
  {k:"q",quote:"Vitamin D deficiency can lead to a loss of bone density, which can contribute to osteoporosis and fractures (broken bones).",who:"MedlinePlus — Vitamin D Deficiency",url:"https://medlineplus.gov/vitaminddeficiency.html"},
  {k:"inf",quote:"MedlinePlus reports vitamin D as categories (Deficient/Insufficient/Sufficient) with no numeric ng/mL cutoff; mapping a 'low' result to 'deficient' is reasoned.",who:"Reasoned from the sourced facts above",url:""}
 ]
},
/* 8 */ {
 id:"ckd", label:"Chronic kidney disease", grp:"Kidney & liver",
 one:"Kidneys that filter blood less well than they should — usually silent until it's advanced.",
 silent:"Many people have no symptoms until kidney disease is advanced; blood and urine tests are the only way to know.",
 symptoms:["(often none early on)","Swelling in legs, feet, ankles or face","Urinating more or less than usual","Dry, itchy skin","Fatigue","Nausea","Loss of appetite"],
 markers:[
  {slug:"creatinine",name:"Creatinine",abbr:"Cr",panel:true,step:"screen",abn:"high",sig:"A waste product the kidneys clear; a routine panel measures it. High can signal reduced filtering."},
  {slug:"egfr",name:"Estimated GFR",abbr:"eGFR",panel:true,step:"screen",abn:"low",sig:"How fast the kidneys filter, calculated from creatinine. A below-normal eGFR may mean kidney disease."},
  {slug:"bun",name:"Blood urea nitrogen",abbr:"BUN",panel:true,step:"screen",abn:"high",sig:"Another kidney waste product on the routine panel."},
  {slug:"acr",name:"Urine albumin (ACR)",abbr:"uACR",panel:false,step:"confirm",abn:"high",sig:"Albumin in the urine can be one of the first signs of kidney disease — a test you usually have to request."}
 ],
 confirm:"acr", support:["egfr","creatinine"],
 reads:{
  strong:"A below-normal eGFR (or high creatinine) together with albumin in the urine fits kidney disease. MedlinePlus advises repeating the urine test — two of three abnormal over months suggests early CKD. A clinician confirms.",
  supportive:"Albumin in the urine can be one of the first signs of kidney disease. It's usually repeated over months and reviewed by a clinician.",
  partial:"Some kidney numbers are off and some aren't — a clinician reads them together and usually repeats the urine test before concluding.",
  against:"Kidney filtering and urine albumin look normal here. Chronic kidney disease isn't indicated."
 },
 src:[
  {k:"q",quote:"Chronic kidney disease (CKD) means that your kidneys are damaged and can't filter blood as they should. This damage can cause wastes to build up in your body.",who:"MedlinePlus — Chronic Kidney Disease",url:"https://medlineplus.gov/chronickidneydisease.html"},
  {k:"q",quote:"The kidney damage occurs slowly over many years. Many people don't have any symptoms until their kidney disease is very advanced. Blood and urine tests are the only way to know if you have kidney disease.",who:"MedlinePlus — Chronic Kidney Disease",url:"https://medlineplus.gov/chronickidneydisease.html"},
  {k:"q",quote:"Creatinine levels in blood are often used to calculate how fast your kidneys filter waste out of your blood. This is called an estimated glomerular filtration rate (eGFR) … An eGFR that's below normal or low may mean that you may have kidney disease.",who:"MedlinePlus — Creatinine / GFR Test",url:"https://medlineplus.gov/lab-tests/glomerular-filtration-rate-gfr-test/"},
  {k:"q",quote:"Albumin in urine may be one of the first signs of kidney disease … If two out of three tests show abnormal levels of albumin in your urine, you may have early-stage kidney disease.",who:"MedlinePlus — Microalbumin Creatinine Ratio",url:"https://medlineplus.gov/lab-tests/microalbumin-creatinine-ratio/"},
  {k:"q",quote:"Treatments cannot cure kidney disease, but they may slow kidney disease … Sometimes it can lead to kidney failure. If your kidneys fail, you will need dialysis or a kidney transplantation.",who:"MedlinePlus — Chronic Kidney Disease",url:"https://medlineplus.gov/chronickidneydisease.html"},
  {k:"inf",quote:"Treating creatinine/eGFR/BUN as the routine screen and urine albumin as the added confirming/early marker is a sequence assembled from the sourced facts — flagged reasoned.",who:"Reasoned from the sourced facts above",url:""}
 ]
},
/* 9 */ {
 id:"liver", label:"Liver injury (raised liver enzymes)", grp:"Kidney & liver",
 one:"Signs on a blood test that the liver may be inflamed or damaged. Often picked up before symptoms.",
 silent:"Liver injury can be present with no symptoms — the routine metabolic panel screens for it.",
 symptoms:["(sometimes none)","Yellowing of skin or eyes (jaundice)","Nausea and vomiting","Fatigue and weakness","Swelling / pain in the abdomen","Dark urine or light stool","Frequent itching"],
 markers:[
  {slug:"alt",name:"Alanine transaminase",abbr:"ALT",panel:true,step:"confirm",abn:"high",sig:"A liver enzyme on the routine panel; a high level is a fairly specific sign of liver inflammation."},
  {slug:"ast",name:"Aspartate aminotransferase",abbr:"AST",panel:true,step:"screen",abn:"high",sig:"Another liver enzyme on the panel; often rises with ALT."},
  {slug:"alp",name:"Alkaline phosphatase",abbr:"ALP",panel:true,step:"screen",abn:"high",sig:"Rises more with bile-duct problems; part of the panel."},
  {slug:"bilirubin",name:"Bilirubin",abbr:"bili",panel:true,step:"screen",abn:"high",sig:"A waste product the liver clears; high bilirubin can cause jaundice."}
 ],
 confirm:"alt", support:["ast"],
 reads:{
  strong:"Raised ALT with a raised AST is the pattern of an inflamed liver (hepatitis). Liver tests alone can't say the cause, so a clinician will usually order more tests to find it.",
  supportive:"A raised ALT points to liver inflammation. On its own it doesn't give the cause — a clinician follows up with more tests.",
  partial:"Some liver enzymes are up and some aren't — MedlinePlus notes these patterns are complex and best read by a clinician.",
  against:"Your liver enzymes look normal here. Liver injury isn't indicated on these numbers."
 },
 src:[
  {k:"q",quote:"Some of these tests can show how well your liver is working and others can show whether your liver may be damaged by liver disease or injury.",who:"MedlinePlus — Liver Function Tests",url:"https://medlineplus.gov/lab-tests/liver-function-tests/"},
  {k:"q",quote:"Symptoms of liver disease can vary, but they often include swelling of the abdomen and legs, bruising easily, changes in the color of your stool and urine, and jaundice, or yellowing of the skin and eyes. Sometimes there are no symptoms.",who:"MedlinePlus — Liver Diseases",url:"https://medlineplus.gov/liverdiseases.html"},
  {k:"q",quote:"Many liver function tests are included in a common blood test called a comprehensive metabolic panel (CMP). Your provider often orders a CMP as part of your routine checkup to screen for liver and other diseases.",who:"MedlinePlus — Liver Function Tests",url:"https://medlineplus.gov/lab-tests/liver-function-tests/"},
  {k:"q",quote:"In general, the results of your liver function tests can tell you if: Your liver is inflamed, which means you have hepatitis … But liver function tests alone usually can't diagnose specific diseases. So, if your results are abnormal, you'll usually need other tests to find the exact cause.",who:"MedlinePlus — Liver Function Tests",url:"https://medlineplus.gov/lab-tests/liver-function-tests/"},
  {k:"inf",quote:"Naming ALT the confirm and AST a supporting screen reflects common practice; MedlinePlus stresses the pattern is read as a whole, so this simplification is flagged reasoned.",who:"Reasoned from the sourced facts above",url:""}
 ]
},
/* 10 */ {
 id:"gout", label:"Gout / high uric acid", grp:"Bones & joints",
 one:"Uric acid building up and forming crystals in a joint, causing sudden, intense attacks.",
 symptoms:["Intense joint pain (often the big toe)","Swelling","Redness","Warmth","Flares often start suddenly at night","(no symptoms between flares)"],
 markers:[
  {slug:"uric_acid",name:"Uric acid (blood)",abbr:"urate",panel:false,step:"screen",abn:"high",sig:"Measures uric acid in the blood. High levels (hyperuricemia) can form crystals — but many people with high levels never get gout."},
  {slug:"joint_fluid",name:"Joint fluid analysis",abbr:"synovial fluid",panel:false,step:"confirm",abn:"high",reasoned:true,sig:"Not a blood test — fluid from the sore joint checked for uric-acid crystals; the most definitive confirmation of gout."}
 ],
 confirm:"uric_acid", support:[],
 reads:{
  strong:"A high blood uric acid fits gout, especially with a sudden hot, swollen joint. But high uric acid alone doesn't prove it — MedlinePlus notes many people have high levels without problems, and gout is usually confirmed from joint fluid.",
  supportive:"A high blood uric acid fits gout, especially with a sudden hot, swollen joint. But high uric acid alone doesn't prove it — MedlinePlus notes many people have high levels without problems, and gout is usually confirmed from joint fluid.",
  partial:"Uric acid is a clue, not a verdict — a clinician weighs it with your symptoms and, ideally, joint fluid.",
  against:"Your blood uric acid isn't high here. Note gout can still occur with normal levels, so persistent joint attacks are worth a clinician's look."
 },
 src:[
  {k:"q",quote:"Gout is a common type of inflammatory arthritis. It causes pain, swelling, and redness in one or more joints … Gout happens when too much uric acid (urate) builds up in your body over a long time.",who:"MedlinePlus — Gout",url:"https://medlineplus.gov/gout.html"},
  {k:"q",quote:"Gout flares often start suddenly at night, and the symptoms in the affected joint often include: Intense pain, which may be bad enough to wake you up; Swelling; Redness; Warmth … In between flares, you usually don't have symptoms.",who:"MedlinePlus — Gout",url:"https://medlineplus.gov/gout.html"},
  {k:"q",quote:"A uric acid blood test may be used to: Help diagnose gout, usually when done with a synovial fluid analysis.",who:"MedlinePlus — Uric Acid Test",url:"https://medlineplus.gov/lab-tests/uric-acid-test/"},
  {k:"q",quote:"If your results show a high level of uric acid in your blood or urine, it doesn't always mean you have a condition that needs treatment. Many people have high levels of uric acid without having health problems.",who:"MedlinePlus — Uric Acid Test",url:"https://medlineplus.gov/lab-tests/uric-acid-test/"},
  {k:"q",quote:"Over time, if left untreated, your flares may happen more often and last longer … you can develop tophi … They can also cause bone and soft tissue damage and misshapen joints.",who:"MedlinePlus — Gout",url:"https://medlineplus.gov/gout.html"},
  {k:"inf",quote:"The joint-fluid test is not a blood test; it is shown as the definitive confirm per MedlinePlus, and the blood uric acid is treated as the screen — flagged reasoned.",who:"Reasoned from the sourced facts above",url:""}
 ]
},
/* 11 */ {
 id:"inflam", label:"Inflammation (raised CRP / ESR)", grp:"Immune & inflammation",
 one:"A blood signal that inflammation is present somewhere — useful, but it doesn't say where or why.",
 symptoms:["Fever or chills","Rapid heart rate","Unexplained weight loss","Joint stiffness","Neck or shoulder pain","Loss of appetite"],
 markers:[
  {slug:"crp",name:"C-reactive protein",abbr:"CRP",panel:false,step:"confirm",abn:"high",sig:"Made by the liver in response to inflammation. A high CRP means inflammation somewhere — not what or where."},
  {slug:"esr",name:"Erythrocyte sedimentation rate",abbr:"ESR",panel:false,step:"screen",abn:"high",sig:"Another inflammation marker, often done with CRP. Faster rates mean more inflammation."}
 ],
 confirm:"crp", support:["esr"],
 reads:{
  strong:"A high CRP (often with a high ESR) means inflammation is present in your body. Crucially, it doesn't say the cause or location — a clinician reads it alongside your symptoms and other tests to find the source.",
  supportive:"A high CRP means inflammation is present somewhere. It's a starting point, not a diagnosis — a clinician looks for the cause.",
  partial:"Inflammation markers can be mildly off for many reasons; a clinician interprets them with the rest of the picture.",
  against:"Your inflammation markers look normal here — though a normal result doesn't completely rule out a condition that causes inflammation."
 },
 src:[
  {k:"q",quote:"A c-reactive protein test measures the level of c-reactive protein (CRP) in a sample of your blood. Your liver makes CRP in response to inflammation.",who:"MedlinePlus — C-Reactive Protein (CRP) Test",url:"https://medlineplus.gov/lab-tests/c-reactive-protein-crp-test/"},
  {k:"q",quote:"By measuring the levels of c-reactive protein in your blood, a CRP test can tell your health care provider how much inflammation you have in your body. High CRP levels may mean you have an acute or chronic health condition, such as: Infections from bacteria or viruses … Autoimmune disorders, such as lupus, rheumatoid arthritis, and vasculitis.",who:"MedlinePlus — C-Reactive Protein (CRP) Test",url:"https://medlineplus.gov/lab-tests/c-reactive-protein-crp-test/"},
  {k:"q",quote:"Your CRP test results tell you how much inflammation you have in your body, but not what's causing it or where it is. To make a diagnosis, your provider will look at your CRP results along with the results of other tests, your symptoms, and medical history.",who:"MedlinePlus — C-Reactive Protein (CRP) Test",url:"https://medlineplus.gov/lab-tests/c-reactive-protein-crp-test/"},
  {k:"q",quote:"A value of 0.8-1.0 milligrams per deciliter (mg/dL) or lower is thought to be a healthy amount. Any increases above normal may mean you have inflammation in your body.",who:"MedlinePlus — C-Reactive Protein (CRP) Test",url:"https://medlineplus.gov/lab-tests/c-reactive-protein-crp-test/"},
  {k:"q",quote:"A C-reactive protein (CRP) test is commonly done with an ESR to provide more information … it's possible to have a condition that causes inflammation and still have a normal ESR result.",who:"MedlinePlus — Erythrocyte Sedimentation Rate (ESR)",url:"https://medlineplus.gov/lab-tests/erythrocyte-sedimentation-rate-esr/"},
  {k:"inf",quote:"Pairing CRP (confirm) with ESR (screen) reflects common practice; both are non-specific, so the reads stay deliberately hedged — the sequencing is reasoned.",who:"Reasoned from the sourced facts above",url:""}
 ]
}
];

const CGROUPS=["Energy & blood","Hormones & metabolism","Heart & circulation","Kidney & liver","Bones & joints","Immune & inflammation"];
const PANEL_SLUGS=["hemoglobin","hematocrit","mcv","glucose","creatinine","egfr","bun","alt","ast","alp","bilirubin","totchol","ldl","hdl","trig"];
const byId=id=>CONDITIONS.find(c=>c.id===id);

/* expose for tests */
if(typeof module!=="undefined"){ module.exports={CONCERNS,CONDITIONS,CGROUPS,PANEL_SLUGS}; }
})();
