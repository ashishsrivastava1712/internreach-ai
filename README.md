# InternReach AI

Most students send the same generic internship email to every company. Recruiters can tell. InternReach AI fixes that — it reads your resume, understands each company's domain, and writes a different, specific email for every HR contact. Then it sends them from your Gmail, tracks who replied, and follows up with the ones who didn't.

Built as a final-year project exploring practical applications of RAG, LLMs, and automation.

---

## What it does

You give it two things: your resume and a list of HR contacts. It handles everything else.

For each company, the system pulls the most relevant parts of your resume using vector search, feeds that context to an LLM, and generates an email that actually mentions your specific projects and skills in relation to that company's domain. Before sending, a second LLM call scores the email on personalization, professionalism, and relevance — if the average falls below 7/10, it regenerates. Only good emails go out.

After sending, it monitors your inbox for replies. Contacts that haven't responded in 15 days get a follow-up automatically.

---

## Tech stack

| Layer | Technology |
|---|---|
| Language model | OpenRouter API — GPT-4o-mini, Llama 3, Mistral |
| Embeddings | sentence-transformers/all-mpnet-base-v2 |
| Vector search | FAISS |
| Orchestration | LangChain |
| Email delivery | Gmail SMTP via App Password |
| Storage | SQLite + SQLAlchemy |
| Scheduling | APScheduler |
| Interface | Streamlit |

---

## Project structure

```
internreach-ai/
│
├── src/
│   ├── llm/
│   │   ├── email_generator.py        RAG + LLM email generation with retry logic
│   │   ├── email_quality_scorer.py   Scores emails 1-10, triggers regeneration
│   │   ├── followup_generator.py     Generates context-aware follow-up emails
│   │   └── prompt_builder.py         Prompt templates
│   │
│   ├── rag/
│   │   ├── vector_store.py           FAISS index build + load
│   │   ├── embedder.py               Sentence transformer wrapper
│   │   └── retriever.py              Top-k chunk retrieval
│   │
│   ├── parsing/
│   │   ├── resume_parser.py          Extracts name, skills, projects from PDF/DOCX
│   │   └── hr_data_loader.py         Reads HR contacts from Excel
│   │
│   ├── email/
│   │   ├── gmail_client.py           Gmail API + SMTP client
│   │   └── reply_monitor.py          Inbox polling for replies
│   │
│   ├── database/
│   │   ├── models.py                 SQLAlchemy table definitions
│   │   └── db_manager.py             CRUD operations, stats queries
│   │
│   └── scheduler/
│       └── followup_scheduler.py     APScheduler job definitions
│
├── ui/
│   ├── streamlit_app.py              Web interface — setup, campaign, analytics
│   └── analytics_dashboard.py       Plotly charts and export
│
├── data/                             Your resume and HR contacts (gitignored)
├── exports/                          Generated PDF and Excel reports
├── main.py                           CLI entry point
├── config.yaml                       Model and pipeline configuration
└── requirements.txt
```

---

## Running locally

**1. Clone and set up environment**

```bash
git clone https://github.com/isroasaws-cell/internreach-ai.git
cd internreach-ai

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux

pip install -r requirements.txt
```

**2. Configure**

```bash
cp .env.example .env
```

Open `.env` and fill in:

```env
OPENAI_API_KEY=your_openrouter_key_here
OPENAI_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-4o-mini
SCORER_MODEL=openai/gpt-4o-mini
CANDIDATE_NAME=Your Full Name
CANDIDATE_EMAIL=your_email@gmail.com
GENERATION_DELAY=5
```

Get a free API key at [openrouter.ai](https://openrouter.ai). After signing up, go to Settings → Privacy and turn off "ZDR Endpoints Only" — this is required to use free models.

**3. Prepare your data**

Place your resume at `data/resume.pdf` and your HR contacts at `data/hr_contacts.xlsx`.

The Excel file needs four columns:

| HR Name | HR Email | Company Name | Domain |
|---|---|---|---|
| Priya Sharma | priya@techcorp.com | TechCorp | AI/ML |
| Raj Mehta | raj@finsync.com | FinSync | FinTech |

**4. Run**

```bash
# See what emails would be generated — nothing is sent
python main.py --mode campaign --dry-run

# Send for real
python main.py --mode campaign

# Check inbox for replies
python main.py --mode check_replies

# Send follow-ups to non-replies (15+ days)
python main.py --mode followups

# Print campaign stats
python main.py --mode stats

# Open the dashboard
streamlit run ui/streamlit_app.py
```

---

## Deploying to Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **Create app**, select this repo, set main file to `ui/streamlit_app.py`
4. Open **Settings → Secrets** and paste:

```toml
OPENAI_API_KEY = "your_openrouter_key"
OPENAI_BASE_URL = "https://openrouter.ai/api/v1"
LLM_MODEL = "openai/gpt-4o-mini"
SCORER_MODEL = "openai/gpt-4o-mini"
GENERATION_DELAY = "5"
```

5. Hit **Deploy**. It'll be live in a few minutes.

---

## How the pipeline works

```
Resume
  │
  ▼
Parse skills, projects, experience
  │
  ▼
Build FAISS vector index (sentence-transformers embeddings)
  │
  ▼
For each HR contact:
  │
  ├─ Retrieve top-3 resume chunks most relevant to their domain
  │
  ├─ LLM writes email referencing those specific chunks
  │
  ├─ Second LLM call scores: Personalization + Professionalism + Relevance
  │     └─ Average < 7.0 → regenerate (up to 3 attempts)
  │
  └─ Send via Gmail SMTP, log to SQLite (msg_id, thread_id, score, timestamp)
          │
          ▼
    Poll inbox daily for replies → update status
          │
          ▼
    No reply after 15 days → send follow-up
```

---

## A note on free models

OpenRouter's free tier works well for testing but has a daily request limit (50/day as of writing). For actual use, adding $5 in credits unlocks GPT-4o-mini at roughly $0.0003 per email — negligible cost for the quality improvement.

---

## License

MIT — use it, modify it, build on it.

---

*Built by [Ashish Srivastava](https://github.com/isroasaws-cell)*