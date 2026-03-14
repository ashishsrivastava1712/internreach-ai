import streamlit as st
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv(override=True)

st.set_page_config(
    page_title="InternReach AI",
    page_icon="📬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Cal+Sans&display=swap');

* { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem 2rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f0f10 !important;
    border-right: 1px solid #1e1e22 !important;
    min-width: 220px !important;
}
[data-testid="stSidebar"] * { color: #fff !important; }
.sidebar-logo {
    padding: 1.5rem 1.2rem 1rem;
    border-bottom: 1px solid #1e1e22;
    margin-bottom: 1rem;
}
.sidebar-logo h2 {
    font-size: 1.05rem;
    font-weight: 700;
    color: #fff;
    margin: 0;
    letter-spacing: -0.02em;
}
.sidebar-logo p {
    font-size: 0.72rem;
    color: #666 !important;
    margin: 3px 0 0;
}
.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.55rem 1.2rem;
    border-radius: 8px;
    margin: 2px 0.6rem;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 500;
    color: #888 !important;
    transition: all 0.15s;
    text-decoration: none;
}
.nav-item:hover { background: #1a1a1e; color: #fff !important; }
.nav-item.active { background: #1a1a1e; color: #fff !important; }
.nav-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #444;
    flex-shrink: 0;
}
.nav-dot.green  { background: #22c55e; }
.nav-dot.blue   { background: #3b82f6; }
.nav-dot.purple { background: #a855f7; }
.nav-dot.orange { background: #f97316; }
.sidebar-section {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #444 !important;
    padding: 1rem 1.2rem 0.3rem;
}
.sidebar-divider {
    height: 1px;
    background: #1e1e22;
    margin: 0.8rem 1.2rem;
}
.sidebar-status {
    margin: 1rem 1.2rem 0;
    padding: 0.75rem 1rem;
    background: #14251a;
    border: 1px solid #1a3a25;
    border-radius: 8px;
    font-size: 0.75rem;
    color: #22c55e !important;
}
.sidebar-status span { color: #666 !important; display: block; font-size: 0.68rem; margin-top: 2px; }

/* ── Main area ── */
body { background: #f8f8fa !important; }
.main { background: #f8f8fa; }

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}
.page-header h1 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #0f0f10;
    margin: 0;
    letter-spacing: -0.03em;
}
.page-header p {
    font-size: 0.82rem;
    color: #888;
    margin: 3px 0 0;
}
.header-badge {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #16a34a;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
}

/* ── Stat cards ── */
.stats-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.stat-card {
    flex: 1;
    background: #fff;
    border: 1px solid #e8e8ec;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
}
.stat-card.blue::before   { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.stat-card.green::before  { background: linear-gradient(90deg, #22c55e, #4ade80); }
.stat-card.purple::before { background: linear-gradient(90deg, #a855f7, #c084fc); }
.stat-card.orange::before { background: linear-gradient(90deg, #f97316, #fb923c); }
.stat-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 6px;
}
.stat-num {
    font-size: 2rem;
    font-weight: 700;
    color: #0f0f10;
    line-height: 1;
    letter-spacing: -0.04em;
}
.stat-sub {
    font-size: 0.72rem;
    color: #aaa;
    margin-top: 4px;
}

/* ── Cards ── */
.card {
    background: #fff;
    border: 1px solid #e8e8ec;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.card-header {
    font-size: 0.85rem;
    font-weight: 600;
    color: #0f0f10;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.card-icon {
    width: 28px; height: 28px;
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
}
.card-icon.blue   { background: #eff6ff; }
.card-icon.green  { background: #f0fdf4; }
.card-icon.purple { background: #faf5ff; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #fff;
    border: 1px solid #e8e8ec;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    margin-bottom: 1.2rem;
    width: fit-content;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    font-weight: 500;
    color: #888;
    padding: 0.45rem 1rem;
    border-radius: 7px;
    border: none;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    color: #0f0f10 !important;
    background: #f3f4f6 !important;
    font-weight: 600 !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
    border-radius: 10px !important;
    height: 6px !important;
}
.stProgress > div {
    background: #e8e8ec !important;
    border-radius: 10px !important;
    height: 6px !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    background: #0f0f10 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.5rem !important;
    letter-spacing: -0.01em !important;
    transition: all 0.15s !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.15) !important;
}
.stButton > button:hover {
    background: #222 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploadDropzone"] {
    border: 2px dashed #d1d5db !important;
    border-radius: 10px !important;
    background: #fafafa !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: #3b82f6 !important;
    background: #eff6ff !important;
}

/* ── Inputs ── */
.stTextInput input {
    border-radius: 8px !important;
    border: 1px solid #e2e8f0 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 0.8rem !important;
    background: #fff !important;
}
.stTextInput input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
}

/* ── Checkbox ── */
.stCheckbox label {
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #374151 !important;
}

/* ── Email preview ── */
.email-card {
    background: #fff;
    border: 1px solid #e8e8ec;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 0.8rem;
}
.email-card-header {
    padding: 0.8rem 1.2rem;
    border-bottom: 1px solid #f3f4f6;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #fafafa;
}
.email-card-company {
    font-weight: 600;
    font-size: 0.85rem;
    color: #0f0f10;
}
.email-card-hr {
    font-size: 0.75rem;
    color: #888;
    margin-top: 1px;
}
.email-card-body {
    padding: 1rem 1.2rem;
    font-size: 0.83rem;
    color: #374151;
    line-height: 1.75;
    white-space: pre-wrap;
}
.pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
}
.pill-blue   { background: #eff6ff; color: #3b82f6; }
.pill-green  { background: #f0fdf4; color: #16a34a; }
.pill-yellow { background: #fefce8; color: #ca8a04; }

/* ── Loading animation ── */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
.loading-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #3b82f6;
    margin: 0 2px;
    animation: pulse 1.2s ease-in-out infinite;
}
.loading-dot:nth-child(2) { animation-delay: 0.2s; background: #8b5cf6; }
.loading-dot:nth-child(3) { animation-delay: 0.4s; background: #06b6d4; }

/* ── Alerts ── */
.stAlert { border-radius: 10px !important; border: none !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #fafafa !important;
    border: 1px solid #e8e8ec !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #e8e8ec !important;
    border-radius: 10px !important;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

from src.database.db_manager import DBManager as DatabaseManager
from src.parsing.resume_parser import parse_resume
from src.parsing.hr_data_loader import load_hr_contacts
from src.llm.email_generator import generate_email
from src.rag.vector_store import build_vector_store
from ui.analytics_dashboard import render_analytics_tab

db = DatabaseManager()

# ── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h2>📬 InternReach AI</h2>
        <p>Outreach Automation</p>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "",
        ["Upload Data", "Run Campaign", "Analytics", "Settings"],
        label_visibility="collapsed"
    )

    st.markdown("""
    <div class="sidebar-divider"></div>
    <div class="sidebar-section">Status</div>
    <div class="sidebar-status">
        ● Groq Llama 70B
        <span>Connected · Free tier</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="padding: 0 1.2rem; font-size: 0.72rem; color: #444;">
        <div style="margin-bottom:6px;">
            <span style="color:#666;">Candidate</span><br>
            <span style="color:#aaa;">{os.getenv('CANDIDATE_NAME','Ashish Srivastava')}</span>
        </div>
        <div>
            <span style="color:#666;">Model</span><br>
            <span style="color:#aaa;">{os.getenv('LLM_MODEL','llama-3.3-70b-versatile')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Pages ───────────────────────────────────────────────────

# ══════════════════════════
# PAGE 1 — Upload
# ══════════════════════════
if page == "Upload Data":
    st.markdown("""
    <div class="page-header">
        <div>
            <h1>Upload Data</h1>
            <p>Add your resume and HR contacts to get started</p>
        </div>
        <span class="header-badge">Step 1 of 2</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown('<div class="card"><div class="card-header"><div class="card-icon blue">📄</div> Resume</div>', unsafe_allow_html=True)
        resume_file = st.file_uploader("Upload PDF or DOCX", type=["pdf","docx"], key="r_up")
        if resume_file:
            path = f"data/{resume_file.name}"
            os.makedirs("data", exist_ok=True)
            with open(path, "wb") as f:
                f.write(resume_file.read())
            with st.spinner("Parsing resume..."):
                time.sleep(0.5)
                try:
                    info = parse_resume(path)
                    if isinstance(info, dict):
                        skills = info.get('skills', [])
                        st.success(f"✅ Parsed — {info.get('name','')}")
                        st.markdown(f"**Skills found:** {', '.join(skills[:8])}")
                    build_vector_store(path)
                    st.success("✅ Vector store ready")
                except Exception as e:
                    st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><div class="card-header"><div class="card-icon green">📊</div> HR Contacts</div>', unsafe_allow_html=True)
        hr_file = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx","xls"], key="h_up")
        if hr_file:
            path = f"data/{hr_file.name}"
            os.makedirs("data", exist_ok=True)
            with open(path, "wb") as f:
                f.write(hr_file.read())
            with st.spinner("Loading contacts..."):
                time.sleep(0.3)
                try:
                    hrs = load_hr_contacts(path)
                    # Save to DB — persistent across restarts!
                    saved = 0
                    for hr in hrs:
                        try:
                            db.add_hr_contact(hr)
                            saved += 1
                        except:
                            pass
                    st.success(f"✅ {len(hrs)} contacts loaded & {saved} saved to DB")
                    st.dataframe(
                        [{"Company": h["company"], "HR": h["hr_name"], "Domain": h["domain"]} for h in hrs],
                        use_container_width=True, hide_index=True
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════
# PAGE 2 — Campaign
# ══════════════════════════
elif page == "Run Campaign":
    st.markdown("""
    <div class="page-header">
        <div>
            <h1>Run Campaign</h1>
            <p>Generate and send personalized internship emails</p>
        </div>
        <span class="header-badge">Groq · Llama 70B</span>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        c1, c2, c3 = st.columns([3, 3, 1])
        with c1:
            hr_path = st.text_input("HR Contacts", value="data/hr_contacts.xlsx")
        with c2:
            resume_path = st.text_input("Resume", value="data/resume.pdf")
        with c3:
            st.markdown("<br>", unsafe_allow_html=True)
            dry_run = st.checkbox("Dry Run", value=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀  Launch Campaign"):
        try:
            with st.spinner(""):
                st.markdown("""
                <div style="display:flex;align-items:center;gap:10px;padding:1rem;background:#fff;border:1px solid #e8e8ec;border-radius:10px;margin-bottom:1rem;">
                    <span class="loading-dot"></span>
                    <span class="loading-dot"></span>
                    <span class="loading-dot"></span>
                    <span style="font-size:0.85rem;color:#555;font-weight:500;">Initializing campaign...</span>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.8)

            # Try file first, fallback to DB
            try:
                hrs = load_hr_contacts(hr_path)
            except:
                hrs = db.get_all_hr_contacts() if hasattr(db, 'get_all_hr_contacts') else []
                if hrs:
                    st.info(f"📦 Loaded {len(hrs)} contacts from database")

            # Stats row
            st.markdown(f"""
            <div class="stats-row">
                <div class="stat-card blue">
                    <div class="stat-label">Contacts</div>
                    <div class="stat-num">{len(hrs)}</div>
                    <div class="stat-sub">HR targets loaded</div>
                </div>
                <div class="stat-card purple">
                    <div class="stat-label">Mode</div>
                    <div class="stat-num" style="font-size:1.3rem;">{"DRY RUN" if dry_run else "LIVE"}</div>
                    <div class="stat-sub">{"Preview only" if dry_run else "Sending emails"}</div>
                </div>
                <div class="stat-card green">
                    <div class="stat-label">Model</div>
                    <div class="stat-num" style="font-size:1rem;letter-spacing:-0.02em;">Llama 70B</div>
                    <div class="stat-sub">via Groq · Free</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            progress_bar = st.progress(0)
            status_box   = st.empty()
            results = []
            email_data = []

            for i, hr in enumerate(hrs):
                pct = (i) / len(hrs)
                progress_bar.progress(pct)
                status_box.markdown(f"""
                <div style="padding:0.75rem 1rem;background:#fff;border:1px solid #e8e8ec;border-radius:8px;font-size:0.83rem;color:#555;">
                    <span class="loading-dot"></span>
                    <span class="loading-dot"></span>
                    <span class="loading-dot"></span>
                    &nbsp; Generating for <b style="color:#0f0f10;">{hr['company']}</b> — {hr['hr_name']} &nbsp;
                    <span style="color:#aaa;">({i+1}/{len(hrs)})</span>
                </div>
                """, unsafe_allow_html=True)

                email = generate_email(hr)
                results.append({
                    "Company": hr["company"],
                    "HR Name": hr["hr_name"],
                    "Subject": email.get("subject",""),
                    "Status":  "dry-run" if dry_run else "sent"
                })
                email_data.append((hr, email))
                time.sleep(0.3)

            progress_bar.progress(1.0)
            status_box.empty()

            st.success(f"✅  Campaign complete — {len(results)} emails {'previewed' if dry_run else 'sent'}")
            st.dataframe(results, use_container_width=True, hide_index=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Email Previews**")

            for hr, email in email_data:
                with st.expander(f"📧  {hr['company']}  ·  {hr['hr_name']}"):
                    st.markdown(f"""
                    <div class="email-card">
                        <div class="email-card-header">
                            <div>
                                <div class="email-card-company">{hr['company']}</div>
                                <div class="email-card-hr">To: {hr['hr_name']} · {hr.get('email','')}</div>
                            </div>
                            <span class="pill {'pill-yellow' if dry_run else 'pill-green'}">
                                {'● dry run' if dry_run else '● sent'}
                            </span>
                        </div>
                        <div style="padding:0.6rem 1.2rem;background:#f8faff;border-bottom:1px solid #f3f4f6;font-size:0.8rem;color:#555;">
                            <b>Subject:</b> {email.get('subject','')}
                        </div>
                        <div class="email-card-body">{email.get('body','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")

# ══════════════════════════
# PAGE 3 — Analytics
# ══════════════════════════
elif page == "Analytics":
    st.markdown("""
    <div class="page-header">
        <div>
            <h1>Analytics</h1>
            <p>Campaign performance and reply tracking</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    render_analytics_tab(db)

# ══════════════════════════
# PAGE 4 — Settings
# ══════════════════════════
elif page == "Settings":
    st.markdown("""
    <div class="page-header">
        <div>
            <h1>Settings</h1>
            <p>API configuration and environment</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-header"><div class="card-icon blue">🔑</div> API Config</div>
            <table style="width:100%;font-size:0.83rem;border-collapse:collapse;">
                <tr><td style="padding:6px 0;color:#888;width:90px;">Model</td><td style="color:#0f0f10;font-weight:500;">{os.getenv('LLM_MODEL','llama-3.3-70b-versatile')}</td></tr>
                <tr><td style="padding:6px 0;color:#888;">Base URL</td><td style="color:#0f0f10;font-size:0.75rem;">{os.getenv('OPENAI_BASE_URL','https://api.groq.com/openai/v1')}</td></tr>
                <tr><td style="padding:6px 0;color:#888;">API Key</td><td style="color:#22c55e;font-weight:600;">● Connected</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-header"><div class="card-icon purple">👤</div> Candidate</div>
            <table style="width:100%;font-size:0.83rem;border-collapse:collapse;">
                <tr><td style="padding:6px 0;color:#888;width:90px;">Name</td><td style="color:#0f0f10;font-weight:500;">{os.getenv('CANDIDATE_NAME','Ashish Srivastava')}</td></tr>
                <tr><td style="padding:6px 0;color:#888;">Email</td><td style="color:#0f0f10;">{os.getenv('CANDIDATE_EMAIL','ashish171200@gmail.com')}</td></tr>
                <tr><td style="padding:6px 0;color:#888;">Delay</td><td style="color:#0f0f10;">{os.getenv('GENERATION_DELAY','5')}s between emails</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-header"><div class="card-icon green">📁</div> Data Files</div>', unsafe_allow_html=True)
    data_files = os.listdir("data") if os.path.exists("data") else []
    if data_files:
        for f in data_files:
            size = os.path.getsize(f"data/{f}") // 1024
            st.markdown(f'<div style="padding:5px 0;font-size:0.83rem;color:#374151;border-bottom:1px solid #f3f4f6;">📄 {f} <span style="color:#aaa;float:right;">{size} KB</span></div>', unsafe_allow_html=True)
    else:
        st.caption("No files in data/")
    st.markdown('</div>', unsafe_allow_html=True)