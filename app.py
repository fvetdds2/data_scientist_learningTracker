import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Job-Ready Tracker · Dollada",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Data file ─────────────────────────────────────────────────────────────────
DATA_FILE = "progress_data.json"

WEEKS = [
    {
        "num": 1,
        "title": "BigQuery + FHIR Basics",
        "color": "#1D9E75",
        "bg": "#E1F5EE",
        "tag": "GCP · Clinical Standards",
        "target_hrs": 10,
        "milestone": "Resume updated — BigQuery & FHIR R4 lines upgraded with GitHub proof",
        "skills_unlocked": ["GCP (BigQuery)", "FHIR R4 (hands-on)"],
        "sessions": [
            {"day": "Mon · 1 hr",  "tasks": [
                "Create free GCP account at console.cloud.google.com",
                "Enable BigQuery free tier (1 TB queries/month free)"
            ]},
            {"day": "Tue · 1 hr",  "tasks": [
                "Open BigQuery public dataset: bigquery-public-data.cms_medicare",
                "Run 3 queries — GROUP BY diagnosis code, count patients"
            ]},
            {"day": "Wed · 1 hr",  "tasks": [
                "Query CDC BRFSS or CMS dataset — practice window functions: RANK() OVER PARTITION BY",
                "Save query results and note any interesting clinical patterns"
            ]},
            {"day": "Thu · 1 hr",  "tasks": [
                "Read FHIR R4 quick intro: hl7.org/fhir/summary.html (30 min)",
                "Bookmark HAPI FHIR public test server: hapi.fhir.org"
            ]},
            {"day": "Sat · 3 hrs", "tasks": [
                "BigQuery: write a clinical query joining 2+ CMS tables, save results",
                "HAPI FHIR: run GET /Patient, GET /Condition, GET /Observation via browser or curl",
                "Parse one FHIR JSON response in a Jupyter notebook with Python"
            ]},
            {"day": "Sun · 3 hrs", "tasks": [
                "Update resume skills: replace 'FHIR/HL7 (learning)' → 'FHIR R4 (hands-on, HAPI server)'",
                "Update resume skills: add 'GCP (BigQuery, Healthcare data)' under Cloud & MLOps",
                "Commit BigQuery queries + FHIR notebook to GitHub"
            ]},
        ]
    },
    {
        "num": 2,
        "title": "MLflow + Docker — Prove What's on the Resume",
        "color": "#5F5E5A",
        "bg": "#F1EFE8",
        "tag": "MLOps · Containerization",
        "target_hrs": 10,
        "milestone": "MLflow + Docker both verified with GitHub commits — two unverified lines now proven",
        "skills_unlocked": ["MLflow (experiment tracking)", "Docker (containerized app)"],
        "sessions": [
            {"day": "Mon · 1 hr",  "tasks": [
                "Open existing Breast Cancer XGBoost project in Jupyter",
                "pip install mlflow — add mlflow.start_run() wrapper around training loop"
            ]},
            {"day": "Tue · 1 hr",  "tasks": [
                "Log params (n_estimators, max_depth) and metrics (AUC, Brier) with mlflow.log_*",
                "Run 'mlflow ui' in terminal — open localhost:5000 and screenshot the run"
            ]},
            {"day": "Wed · 1 hr",  "tasks": [
                "Install Docker Desktop if not already installed",
                "Read docs.docker.com/get-started — first 2 sections only (30 min)"
            ]},
            {"day": "Thu · 1 hr",  "tasks": [
                "Write Dockerfile for Streamlit Breast Cancer app (FROM python:3.10-slim, COPY, RUN pip, CMD)",
                "Run: docker build -t breast-cancer-app . — verify it builds without errors"
            ]},
            {"day": "Sat · 3 hrs", "tasks": [
                "docker run -p 8501:8501 breast-cancer-app — confirm Streamlit loads in browser",
                "Fix any dependency issues — add/update requirements.txt as needed",
                "Add MLflow screenshot and Docker instructions to project README.md"
            ]},
            {"day": "Sun · 3 hrs", "tasks": [
                "Commit Dockerfile + requirements.txt to Breast Cancer GitHub repo",
                "Update resume: Docker line → 'Docker (containerized Streamlit ML app — GitHub)'",
                "Update resume: MLflow line → 'MLflow (experiment tracking, AUC logged — GitHub)'"
            ]},
        ]
    },
    {
        "num": 3,
        "title": "AWS Cloud Practitioner — Study Sprint",
        "color": "#BA7517",
        "bg": "#FAEEDA",
        "tag": "AWS · Certification",
        "target_hrs": 10,
        "milestone": "All 8 modules complete — practice exam taken, weak areas identified, ready to book",
        "skills_unlocked": ["AWS Cloud Practitioner (cert pending)"],
        "sessions": [
            {"day": "Mon · 1.5 hr", "tasks": [
                "AWS Skill Builder free tier: enroll 'AWS Cloud Practitioner Essentials'",
                "Complete Module 1: Introduction to Amazon Web Services"
            ]},
            {"day": "Tue · 1.5 hr", "tasks": [
                "Complete Module 2: Compute in the Cloud (EC2, Lambda, Fargate)",
                "Complete Module 3: Global Infrastructure and Reliability"
            ]},
            {"day": "Wed · 1.5 hr", "tasks": [
                "Complete Module 4: Networking (VPC, subnets, security groups, Route 53)",
                "Complete Module 5: Storage and Databases (S3, RDS, DynamoDB)"
            ]},
            {"day": "Thu · 1.5 hr", "tasks": [
                "Complete Module 6: Security (IAM, MFA, HIPAA-eligible services — key for healthcare!)",
                "Note Amazon HealthLake + Comprehend Medical: the clinical DS services interviewers ask about"
            ]},
            {"day": "Sat · 2 hrs", "tasks": [
                "Complete Module 7: Monitoring and Analytics (CloudWatch, CloudTrail)",
                "Complete Module 8: Pricing and Support (Free tier, on-demand, reserved)"
            ]},
            {"day": "Sun · 2 hrs", "tasks": [
                "Take AWS Skill Builder Practice Exam — note every wrong answer",
                "Review weak areas — focus on IAM, S3 storage classes, and pricing model questions"
            ]},
        ]
    },
    {
        "num": 4,
        "title": "AWS Exam + Clinical NLP Project Kickoff",
        "color": "#BA7517",
        "bg": "#FAEEDA",
        "tag": "AWS Exam · MIMIC-III · NLP Setup",
        "target_hrs": 10,
        "milestone": "AWS cert done · MIMIC access approved · GitHub repo live with project scaffold",
        "skills_unlocked": ["AWS Cloud Practitioner (certified)", "MIMIC-III (credentialed access)"],
        "sessions": [
            {"day": "Mon · 2 hrs", "tasks": [
                "AWS Skill Builder: final review of modules where you scored below 80%",
                "Flashcard review: 6 pillars of Well-Architected Framework (must know for exam)"
            ]},
            {"day": "Tue · 2 hrs", "tasks": [
                "Take second full practice exam — aim for 80%+ before booking real exam",
                "Book AWS Cloud Practitioner exam at Pearson VUE ($100, online proctored, ~2 hr slot)"
            ]},
            {"day": "Wed · EXAM", "tasks": [
                "Sit the AWS Cloud Practitioner exam (65 questions, 90 min, passing score 700/1000)",
                "Add 'AWS Cloud Practitioner (result pending)' to resume immediately after exam"
            ]},
            {"day": "Thu · 1 hr", "tasks": [
                "Submit MIMIC-III credentialing form at physionet.org (if not done yet)",
                "Start CITI training: 'Data or Specimens Only Research' course (~2 hrs total)"
            ]},
            {"day": "Sat · 3 hrs", "tasks": [
                "Finish CITI training + submit PhysioNet credentialing application",
                "Set up conda env: conda create -n clinical-nlp python=3.10",
                "pip install transformers datasets torch pandas scikit-learn streamlit xgboost mlflow shap"
            ]},
            {"day": "Sun · 2 hrs", "tasks": [
                "Create GitHub repo: clinical-nlp-readmission with proper folder structure",
                "Push empty scaffold: data/, notebooks/, src/, app/, models/ — add data/ to .gitignore"
            ]},
        ]
    },
    {
        "num": 5,
        "title": "Clinical NLP — Data Pipeline + BioBERT NER",
        "color": "#534AB7",
        "bg": "#EEEDFE",
        "tag": "MIMIC-III · BioBERT · HuggingFace",
        "target_hrs": 10,
        "milestone": "Data pipeline complete — entities extracted from discharge notes, features ready for modeling",
        "skills_unlocked": ["HuggingFace Transformers (BioBERT NER)", "Clinical NLP pipeline"],
        "sessions": [
            {"day": "Mon · 1 hr", "tasks": [
                "MIMIC access should arrive — download NOTEEVENTS.csv.gz + ADMISSIONS.csv.gz",
                "Load in pandas, print shapes and column names to understand structure"
            ]},
            {"day": "Tue · 1 hr", "tasks": [
                "Filter notes: notes[notes['CATEGORY'] == 'Discharge summary'] — print count",
                "Load ADMISSIONS, sort by SUBJECT_ID + ADMITTIME, calculate DAYS_TO_READMIT"
            ]},
            {"day": "Wed · 1 hr", "tasks": [
                "Create READMIT_30 binary label (days <= 30), merge with notes on HADM_ID",
                "Print class balance — expect ~18–22% positive readmission rate"
            ]},
            {"day": "Thu · 1 hr", "tasks": [
                "from transformers import pipeline — load 'blaze999/Medical-NER' model",
                "Run NER on 5 sample notes — print entities with type (PROBLEM/TREATMENT/TEST) and score"
            ]},
            {"day": "Sat · 3 hrs", "tasks": [
                "Write batched extract_entities() function — process 5,000-note sample",
                "Add PROBLEM / TREATMENT / TEST count columns to dataframe",
                "Save discharge_with_entities.csv (5,000 rows for fast iteration)"
            ]},
            {"day": "Sun · 3 hrs", "tasks": [
                "Build TF-IDF features: TfidfVectorizer(max_features=5000, ngram_range=(1,2), sublinear_tf=True)",
                "Combine TF-IDF + entity counts with scipy.sparse.hstack into X_combined",
                "Commit notebooks/01_data_pipeline.ipynb to GitHub with cell outputs visible"
            ]},
        ]
    },
    {
        "num": 6,
        "title": "Clinical NLP — XGBoost Model + SHAP + Streamlit App",
        "color": "#534AB7",
        "bg": "#EEEDFE",
        "tag": "XGBoost · SHAP · Streamlit deployment",
        "target_hrs": 10,
        "milestone": "Public GitHub repo live — Streamlit app running, real AUC score on resume bullet",
        "skills_unlocked": ["Clinical ML (readmission prediction)", "SHAP explainability", "Streamlit (clinical NLP app)"],
        "sessions": [
            {"day": "Mon · 1 hr", "tasks": [
                "Train XGBoost with scale_pos_weight=4 (handles class imbalance) — log run in MLflow",
                "Print AUC on holdout set — target 0.72–0.78 (clinical benchmark is ~0.70)"
            ]},
            {"day": "Tue · 1 hr", "tasks": [
                "Generate calibration curve: sklearn.calibration.calibration_curve",
                "Save calibration_curve.png to models/ folder — this is a portfolio artifact"
            ]},
            {"day": "Wed · 1 hr", "tasks": [
                "Run SHAP TreeExplainer on 500-row test sample (use .toarray() for sparse matrix)",
                "shap.summary_plot(max_display=20) — save shap_summary.png — note top clinical terms"
            ]},
            {"day": "Thu · 1 hr", "tasks": [
                "Start app/app.py: st.title, st.text_area for discharge note input",
                "Load models with @st.cache_resource — NER pipeline + XGBoost + TF-IDF + scaler"
            ]},
            {"day": "Sat · 3 hrs", "tasks": [
                "Complete Streamlit app: entity extraction display + risk score with color coding",
                "Add disclaimer: 'Research purposes only — not validated for clinical use'",
                "streamlit run app/app.py — test end-to-end with a sample discharge note"
            ]},
            {"day": "Sun · 3 hrs", "tasks": [
                "Write README.md: AUC result, SHAP chart image, methodology, quickstart instructions",
                "Commit everything — joblib.dump models, data/ confirmed in .gitignore",
                "Update resume clinical NLP bullet with real AUC number from your run"
            ]},
        ]
    },
    {
        "num": 7,
        "title": "Vertex AI Deployment + Resume Final Polish + Apply",
        "color": "#1D9E75",
        "bg": "#E1F5EE",
        "tag": "GCP Vertex AI · Resume v4 · Applications",
        "target_hrs": 10,
        "milestone": "Live Vertex AI endpoint · Resume v4 submitted · First 3 applications sent — JOB READY",
        "skills_unlocked": ["GCP Vertex AI (deployed endpoint)", "Job applications active"],
        "sessions": [
            {"day": "Mon · 1 hr", "tasks": [
                "Enable Vertex AI API in GCP console — pip install google-cloud-aiplatform",
                "Read Vertex AI prediction docs: cloud.google.com/vertex-ai/docs/predictions (15 min)"
            ]},
            {"day": "Tue · 1 hr", "tasks": [
                "Write predictor.py wrapping XGBoost model for custom prediction container",
                "Upload model artifact (xgb_model.pkl) to a GCS bucket"
            ]},
            {"day": "Wed · 1 hr", "tasks": [
                "Deploy model to Vertex AI Endpoint (use n1-standard-2 — delete endpoint after testing to save cost)",
                "Send test prediction request via Python SDK — confirm JSON response returns probability"
            ]},
            {"day": "Sat · 4 hrs", "tasks": [
                "Screenshot live Vertex AI endpoint dashboard — add to README and LinkedIn",
                "Update resume: 'Deployed clinical NLP readmission model to GCP Vertex AI endpoint'",
                "Final resume audit: remove ALL 'in progress' / 'learning' hedges — replace with evidence",
                "Verify every Cloud & MLOps skill line has a GitHub link, cert number, or project name"
            ]},
            {"day": "Sun · 3 hrs", "tasks": [
                "Apply to 3 target roles: HCA Healthcare (Clinical DS), Trella Health (DS), Vanderbilt DS",
                "Tailor cover letter: lead with 'PhD + DVM + clinical NLP pipeline on MIMIC-III, AUC 0.XX'",
                "Send LinkedIn connection requests to hiring managers — reference shared Nashville healthcare interest"
            ]},
        ]
    },
]

# ── Persistence helpers ───────────────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    default = {
        "start_date": str(date.today()),
        "tasks": {},
        "hours_log": {},
        "notes": {},
        "week_notes": {}
    }
    save_data(default)
    return default

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def task_key(week_num, session_idx, task_idx):
    return f"w{week_num}_s{session_idx}_t{task_idx}"

def total_tasks():
    return sum(len(t) for w in WEEKS for s in w["sessions"] for t in [s["tasks"]])

def completed_tasks(data):
    return sum(1 for v in data["tasks"].values() if v)

def week_tasks_total(week_num):
    w = next(x for x in WEEKS if x["num"] == week_num)
    return sum(len(s["tasks"]) for s in w["sessions"])

def week_tasks_done(data, week_num):
    return sum(1 for k, v in data["tasks"].items() if k.startswith(f"w{week_num}_") and v)

def week_complete(data, week_num):
    return week_tasks_done(data, week_num) == week_tasks_total(week_num)

def hours_logged(data, week_num):
    return sum(data["hours_log"].get(f"w{week_num}_d{d}", 0) for d in range(7))

# ── Load state ────────────────────────────────────────────────────────────────
data = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧬 Job-Ready Tracker")
    st.markdown("**Dollada Srisai, PhD DVM**")
    st.divider()

    start = date.fromisoformat(data["start_date"])
    today = date.today()
    elapsed = (today - start).days
    current_week = min(elapsed // 7 + 1, 7)

    st.markdown(f"**Started:** {start.strftime('%b %d, %Y')}")
    st.markdown(f"**Current week:** Week {current_week} of 7")
    target_end = start + timedelta(weeks=7)
    days_left = (target_end - today).days
    if days_left > 0:
        st.markdown(f"**Target end:** {target_end.strftime('%b %d')} · {days_left} days left")
    else:
        st.markdown("**🎉 Target date reached!**")

    st.divider()
    total = total_tasks()
    done = completed_tasks(data)
    pct = int(done / total * 100) if total else 0
    st.markdown(f"**Overall progress:** {pct}%")
    st.progress(pct / 100)
    st.caption(f"{done} of {total} tasks complete")

    st.divider()

    if st.button("🔄 Reset all progress", type="secondary", use_container_width=True):
        if st.session_state.get("confirm_reset"):
            data = {
                "start_date": str(date.today()),
                "tasks": {},
                "hours_log": {},
                "notes": {},
                "week_notes": {}
            }
            save_data(data)
            st.session_state["confirm_reset"] = False
            st.rerun()
        else:
            st.session_state["confirm_reset"] = True
            st.warning("Click Reset again to confirm.")

    new_start = st.date_input("Change start date:", value=start)
    if new_start != start:
        data["start_date"] = str(new_start)
        save_data(data)
        st.rerun()

# ── Main tabs ─────────────────────────────────────────────────────────────────
tab_dash, tab_weeks, tab_resume, tab_log = st.tabs([
    "📊 Dashboard", "📅 Weekly Tasks", "📄 Resume Checklist", "📝 Hours Log"
])

# ═══════════════════════════════════════════════════════════════════════
# TAB 1: DASHBOARD
# ═══════════════════════════════════════════════════════════════════════
with tab_dash:
    st.markdown("### Overview")

    c1, c2, c3, c4 = st.columns(4)
    weeks_done = sum(1 for w in WEEKS if week_complete(data, w["num"]))
    total_hrs_logged = sum(
        data["hours_log"].get(f"w{w['num']}_d{d}", 0)
        for w in WEEKS for d in range(7)
    )
    skills_unlocked = sum(
        len(w["skills_unlocked"]) for w in WEEKS if week_complete(data, w["num"])
    )

    with c1:
        st.metric("Weeks Complete", f"{weeks_done} / 7")
    with c2:
        st.metric("Tasks Done", f"{completed_tasks(data)} / {total_tasks()}")
    with c3:
        st.metric("Hours Logged", f"{total_hrs_logged:.1f}")
    with c4:
        st.metric("Skills Unlocked", str(skills_unlocked))

    st.divider()

    # ── Per-week progress chart ──────────────────────────────────────────
    st.markdown("#### Progress by week")
    week_nums, week_pcts, week_colors, week_labels = [], [], [], []
    for w in WEEKS:
        done_w = week_tasks_done(data, w["num"])
        total_w = week_tasks_total(w["num"])
        pct_w = int(done_w / total_w * 100) if total_w else 0
        week_nums.append(f"Wk {w['num']}")
        week_pcts.append(pct_w)
        week_colors.append(w["color"] if pct_w < 100 else "#1D9E75")
        week_labels.append(w["title"])

    fig = go.Figure(go.Bar(
        x=week_nums,
        y=week_pcts,
        marker_color=week_colors,
        text=[f"{p}%" for p in week_pcts],
        textposition="outside",
        customdata=week_labels,
        hovertemplate="<b>%{customdata}</b><br>Progress: %{y}%<extra></extra>"
    ))
    fig.update_layout(
        yaxis=dict(range=[0, 115], title="% complete", showgrid=True, gridcolor="#f0f0f0"),
        xaxis=dict(title=""),
        plot_bgcolor="white",
        paper_bgcolor="rgba(0,0,0,0)",
        height=280,
        margin=dict(t=20, b=10, l=40, r=20),
        font=dict(size=13)
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Week status cards ───────────────────────────────────────────────
    st.markdown("#### Week status")
    cols = st.columns(7)
    for i, w in enumerate(WEEKS):
        done_w = week_tasks_done(data, w["num"])
        total_w = week_tasks_total(w["num"])
        pct_w = int(done_w / total_w * 100)
        is_current = w["num"] == current_week
        complete = pct_w == 100

        with cols[i]:
            status = "✅" if complete else ("🔵" if is_current else "⚪")
            st.markdown(
                f"""<div style='text-align:center;padding:10px 4px;border:1px solid {"#1D9E75" if complete else ("#534AB7" if is_current else "#e0e0e0")};
                border-radius:10px;background:{"#E1F5EE" if complete else ("#EEEDFE" if is_current else "white")}'>
                <div style='font-size:18px'>{status}</div>
                <div style='font-size:11px;font-weight:600;color:{"#085041" if complete else "#333"}'> Week {w["num"]}</div>
                <div style='font-size:10px;color:#888'>{pct_w}%</div>
                </div>""",
                unsafe_allow_html=True
            )

    st.divider()

    # ── Milestone tracker ────────────────────────────────────────────────
    st.markdown("#### Milestones")
    for w in WEEKS:
        complete = week_complete(data, w["num"])
        icon = "✅" if complete else "◻️"
        color = w["color"] if complete else "#aaa"
        st.markdown(
            f"<div style='display:flex;align-items:flex-start;gap:10px;padding:8px 0;"
            f"border-bottom:1px solid #f0f0f0'>"
            f"<span style='font-size:16px'>{icon}</span>"
            f"<div><span style='font-size:12px;font-weight:600;color:{color}'>Week {w['num']}: </span>"
            f"<span style='font-size:12px;color:#555'>{w['milestone']}</span></div></div>",
            unsafe_allow_html=True
        )

# ═══════════════════════════════════════════════════════════════════════
# TAB 2: WEEKLY TASKS
# ═══════════════════════════════════════════════════════════════════════
with tab_weeks:

    week_choice = st.selectbox(
        "Jump to week:",
        options=[f"Week {w['num']} — {w['title']}" for w in WEEKS],
        index=min(current_week - 1, 6)
    )
    selected_num = int(week_choice.split()[1])
    w = next(x for x in WEEKS if x["num"] == selected_num)

    done_w = week_tasks_done(data, selected_num)
    total_w = week_tasks_total(selected_num)
    pct_w = int(done_w / total_w * 100)

    # Header row
    hcol1, hcol2, hcol3 = st.columns([3, 1, 1])
    with hcol1:
        st.markdown(
            f"<h3 style='margin:0'>Week {w['num']}: {w['title']}</h3>"
            f"<span style='font-size:12px;background:{w['bg']};color:{w['color']};"
            f"padding:3px 10px;border-radius:8px'>{w['tag']}</span>",
            unsafe_allow_html=True
        )
    with hcol2:
        st.metric("Tasks done", f"{done_w}/{total_w}")
    with hcol3:
        st.metric("Progress", f"{pct_w}%")

    st.progress(pct_w / 100)

    # Quick complete all button
    qcol1, qcol2 = st.columns([1, 4])
    with qcol1:
        if st.button("✅ Mark all done", use_container_width=True):
            for si, session in enumerate(w["sessions"]):
                for ti in range(len(session["tasks"])):
                    data["tasks"][task_key(selected_num, si, ti)] = True
            save_data(data)
            st.rerun()
    with qcol2:
        if st.button("↩ Clear week", use_container_width=True):
            for si, session in enumerate(w["sessions"]):
                for ti in range(len(session["tasks"])):
                    data["tasks"][task_key(selected_num, si, ti)] = False
            save_data(data)
            st.rerun()

    st.divider()

    # Sessions and tasks
    changed = False
    for si, session in enumerate(w["sessions"]):
        day_done = all(
            data["tasks"].get(task_key(selected_num, si, ti), False)
            for ti in range(len(session["tasks"]))
        )
        day_icon = "✅" if day_done else "📅"
        st.markdown(
            f"<div style='font-size:13px;font-weight:600;color:{w['color']};margin:12px 0 6px'>"
            f"{day_icon} {session['day']}</div>",
            unsafe_allow_html=True
        )
        for ti, task in enumerate(session["tasks"]):
            key = task_key(selected_num, si, ti)
            current_val = data["tasks"].get(key, False)
            new_val = st.checkbox(task, value=current_val, key=f"cb_{key}")
            if new_val != current_val:
                data["tasks"][key] = new_val
                changed = True

    if changed:
        save_data(data)
        st.rerun()

    st.divider()

    # Milestone box
    is_complete = week_complete(data, selected_num)
    if is_complete:
        st.success(f"🎉 **Week {w['num']} complete!** {w['milestone']}")
        st.markdown("**Skills unlocked this week:**")
        for skill in w["skills_unlocked"]:
            st.markdown(f"&nbsp;&nbsp;&nbsp;✅ `{skill}`")
    else:
        st.info(f"🎯 **Milestone:** {w['milestone']}")

    # Week notes
    st.divider()
    st.markdown("**Week notes / blockers:**")
    note_key = f"week_{selected_num}_note"
    current_note = data["week_notes"].get(str(selected_num), "")
    new_note = st.text_area(
        "Notes (saved automatically):",
        value=current_note,
        height=100,
        key=note_key,
        label_visibility="collapsed",
        placeholder="Any blockers, insights, or things to remember this week..."
    )
    if new_note != current_note:
        data["week_notes"][str(selected_num)] = new_note
        save_data(data)

# ═══════════════════════════════════════════════════════════════════════
# TAB 3: RESUME CHECKLIST
# ═══════════════════════════════════════════════════════════════════════
with tab_resume:
    st.markdown("### Resume update checklist")
    st.caption("Each item below should be updated as soon as the associated week is complete. "
               "Green = week done, update your resume NOW.")

    resume_items = [
        {
            "week": 1,
            "section": "Cloud & MLOps",
            "old": "FHIR/HL7 (learning)",
            "new": "FHIR R4 (hands-on, HAPI public server — GitHub)",
        },
        {
            "week": 1,
            "section": "Cloud & MLOps",
            "old": "(GCP not listed)",
            "new": "GCP (BigQuery — queried CMS Medicare public dataset — GitHub)",
        },
        {
            "week": 2,
            "section": "Cloud & MLOps",
            "old": "Docker (containerization basics)",
            "new": "Docker (containerized Streamlit ML app — Dockerfile on GitHub)",
        },
        {
            "week": 2,
            "section": "Cloud & MLOps",
            "old": "MLflow (experiment tracking)",
            "new": "MLflow (tracked AUC, Brier score, params across XGBoost runs — GitHub)",
        },
        {
            "week": 4,
            "section": "Certifications",
            "old": "AWS (in progress: Solutions Architect)",
            "new": "AWS Certified Cloud Practitioner — [cert number] — [month year]",
        },
        {
            "week": 6,
            "section": "Data Science Projects",
            "old": "(placeholder NLP project)",
            "new": "Clinical NLP: 30-Day Readmission Risk from Discharge Notes — BioBERT NER + XGBoost (AUC: 0.XX) · MIMIC-III · Streamlit · SHAP — GitHub",
        },
        {
            "week": 7,
            "section": "Cloud & MLOps",
            "old": "GCP (BigQuery, Healthcare data)",
            "new": "GCP (BigQuery, Healthcare API, Vertex AI — deployed clinical NLP endpoint)",
        },
        {
            "week": 7,
            "section": "NLP (in progress)",
            "old": "HuggingFace Transformers, spaCy, clinical text analysis (MIMIC-III)",
            "new": "HuggingFace Transformers (BioBERT NER on MIMIC-III discharge notes — GitHub)",
        },
    ]

    for idx, item in enumerate(resume_items):
        w_done = week_complete(data, item["week"])
        done_key = f"resume_done_{idx}"
        is_manually_done = data["tasks"].get(done_key, False)

        col_icon, col_content, col_check = st.columns([0.4, 5, 1])
        with col_icon:
            if w_done or is_manually_done:
                st.markdown("🟢")
            else:
                wn = item["week"]
                st.markdown(f"⬜")

        with col_content:
            st.markdown(
                f"<div style='font-size:11px;color:#888;margin-bottom:2px'>"
                f"After Week {item['week']} · {item['section']}</div>"
                f"<div style='font-size:12px'>"
                f"<span style='color:#c00;text-decoration:line-through'>{item['old']}</span>"
                f" → <span style='color:#1D9E75;font-weight:500'>{item['new']}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

        with col_check:
            checked = st.checkbox("Done", value=is_manually_done,
                                  key=f"rc_{done_key}", label_visibility="collapsed")
            if checked != is_manually_done:
                data["tasks"][done_key] = checked
                save_data(data)
                st.rerun()

        st.markdown("<hr style='margin:6px 0;border:none;border-top:1px solid #f5f5f5'>",
                    unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 4: HOURS LOG
# ═══════════════════════════════════════════════════════════════════════
with tab_log:
    st.markdown("### Hours log")
    st.caption("Track actual hours worked each day. Goal: 10 hrs/week.")

    log_changed = False
    total_per_week = []

    for w in WEEKS:
        done_w = week_tasks_done(data, w["num"])
        total_w = week_tasks_total(w["num"])
        wk_hrs = sum(data["hours_log"].get(f"w{w['num']}_d{d}", 0.0) for d in range(7))
        total_per_week.append(wk_hrs)

        with st.expander(
            f"Week {w['num']} — {w['title']}  ·  "
            f"{wk_hrs:.1f} / {w['target_hrs']} hrs  ·  "
            f"{done_w}/{total_w} tasks",
            expanded=(w["num"] == current_week)
        ):
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day_defaults = [1.0, 1.0, 1.0, 1.0, 0.0, 3.0, 3.0]

            cols = st.columns(7)
            for d, (dname, default) in enumerate(zip(day_names, day_defaults)):
                hkey = f"w{w['num']}_d{d}"
                current_hr = data["hours_log"].get(hkey, 0.0)
                with cols[d]:
                    new_hr = st.number_input(
                        dname[:3],
                        min_value=0.0, max_value=8.0, step=0.5,
                        value=float(current_hr),
                        key=f"hr_{hkey}"
                    )
                    if new_hr != current_hr:
                        data["hours_log"][hkey] = new_hr
                        log_changed = True

            bar_pct = min(wk_hrs / w["target_hrs"], 1.0)
            color = "#1D9E75" if bar_pct >= 1.0 else w["color"]
            st.markdown(
                f"<div style='background:#f0f0f0;border-radius:4px;height:6px;margin-top:6px'>"
                f"<div style='width:{bar_pct*100:.0f}%;background:{color};height:100%;border-radius:4px'></div>"
                f"</div><div style='font-size:11px;color:#888;margin-top:3px'>"
                f"{wk_hrs:.1f} hrs logged of {w['target_hrs']} target</div>",
                unsafe_allow_html=True
            )

    if log_changed:
        save_data(data)

    st.divider()
    st.markdown("#### Hours logged per week")
    fig2 = go.Figure(go.Bar(
        x=[f"Wk {w['num']}" for w in WEEKS],
        y=total_per_week,
        marker_color=[w["color"] for w in WEEKS],
        text=[f"{h:.1f}h" for h in total_per_week],
        textposition="outside"
    ))
    fig2.add_hline(y=10, line_dash="dash", line_color="#aaa",
                   annotation_text="10 hr target", annotation_position="right")
    fig2.update_layout(
        yaxis=dict(range=[0, 14], title="Hours", showgrid=True, gridcolor="#f0f0f0"),
        plot_bgcolor="white",
        paper_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(t=20, b=10, l=40, r=60),
        font=dict(size=13),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

    total_all = sum(total_per_week)
    target_all = 70
    st.markdown(
        f"**Total hours logged:** {total_all:.1f} / {target_all}  ·  "
        f"{'On track 🟢' if total_all >= (current_week * 10 * 0.8) else 'Behind pace 🟡'}"
    )
