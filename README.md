# 🤖 **Team Activity Monitor**

### *AI-Powered Engineering Activity Assistant (JIRA + GitHub + LLM + Streamlit + Docker)*

A complete AI chatbot that integrates **JIRA**, **GitHub**, and **OpenAI** to answer natural-language questions about team activity.

Example queries:

> **“What is Abhishek working on these days?”**
> **“Show me Mike’s commits this week.”**
> **“Any open PRs from Abhialien?”**

Built in **2 days** with **production-style architecture** and **full Docker containerization** for easy deployment.

---

# 🚀 **Features**

## 🔹 Live JIRA Integration

* Assigned issues
* Status, summary, priority
* Changelog (recent updates)
* Comments
* JIRA Cloud REST API v3
* Token-based authentication

## 🔹 Live GitHub Integration

* Recent commits
* Active pull requests
* Recently pushed repos
* Period filtering (today/week/month)
* Pagination
* GitHub REST API v3

## 🔹 AI-Powered Summaries (OpenAI)

* Natural language insights from backend JSON
* Bullet summaries
* Professional, short status summaries
* Zero hallucination design: AI only summarizes retrieved data

## 🔹 Query & Intent Understanding

* Extracts member names from natural language
* Multi-stage intent detection:

  * explicit keywords
  * regex patterns
  * full-activity phrases
  * AI fallback classifier
* Supported intents:

  * `JIRA_ISSUES`
  * `GITHUB_COMMITS`
  * `GITHUB_PRS`
  * `GITHUB_REPOS`
  * `FULL_ACTIVITY`

## 🔹 Production-Style Backend (FastAPI)

* `/activity` NLP endpoint
* `/api/v1/jira/...`
* `/api/v1/github/...`
* Unified response format
* Pagination
* Error handling
* Auto-generated Swagger docs

## 🔹 Beautiful Frontend (Streamlit)

* Chat-style UI (WhatsApp-like bubbles)
* Timestamps for each message
* Auto-scrolling
* AI insight rendering
* Fully Dockerized

## 🔹 Clean Architecture (Maintainable)

```
src/
  api/
  core/
  services/
  integrations/
  main.py

streamlit_app/
  components/
  main.py

tests/
```

---

# ⚙️ **Configuration**

Create a `.env` file in the project root:

```
# JIRA
JIRA_BASE_URL=...
JIRA_EMAIL=...
JIRA_API_TOKEN=...
JIRA_ABHISHEK_ACCOUNT_ID=...
JIRA_ABHIALIEN_ACCOUNT_ID=...

# GitHub
GITHUB_TOKEN=...
GITHUB_REPO_NAME=autonomize-activity-monitor
GITHUB_API_HOST_URL=https://api.github.com

# OpenAI
OPENAI_API_KEY=...

# Environment
ENV=production
```

---

# 🐳 **Docker Setup**

We now support **Docker + Docker Compose** for full production deployment.

## 1️⃣ Build & Run (One Command)

```bash
docker compose up --build
```

This starts:

### 🔹 Backend (FastAPI)

→ [http://localhost:8000](http://localhost:8000)

* Swagger UI → `/docs`
* ReDoc → `/redoc`
* Health → `/health`

### 🔹 Frontend (Streamlit)

→ [http://localhost:8501](http://localhost:8501)

---

# 🐳 **Dockerfile Structure**

### Backend → `Dockerfile.backend`

* Uses Python slim
* Installs dependencies
* Copies `src/`
* Runs `uvicorn src.api.main:app`

### Frontend → `Dockerfile.frontend`

* Uses Python slim
* Installs Streamlit
* Copies `streamlit_app/`
* Runs `streamlit run streamlit_app/main.py`

### Docker Compose → `docker-compose.yml`

* Both services
* Shared `.env`
* Network linking
* Backend reachable as `http://backend:8000`

---

# ▶️ **Run Locally (No Docker)**

## Backend

```bash
uvicorn src.api.main:app --reload --port 8000
```

## Frontend

```bash
streamlit run streamlit_app/main.py
```

---

# 🧪 **Tests**

Run tests with:

```bash
pytest -q
```

---

# 🔥 **Example Queries**

Try asking in the UI:

* “What is Abhishek working on these days?”
* “Show Abhialien’s JIRA issues”
* “Recent commits by Abhishek this week”
* “Any PRs opened yesterday?”
* “Which repos did Abhishek touch recently?”

---

# 📦 **API Endpoints**

### NLP Endpoint

```
POST /activity
```

→ Full AI-assisted activity summary

### JIRA

```
GET /api/v1/jira/users/{username}/issues
GET /api/v1/jira/issues/{issue_key}
```

### GitHub

```
GET /api/v1/github/{username}
GET /api/v1/github/{username}/commits
GET /api/v1/github/{username}/prs
GET /api/v1/github/{username}/repos
```

---

# 🧠 **Why This Project Stands Out**

* Combines **three external APIs** (JIRA, GitHub, OpenAI)
* Implements **intent detection**, **period detection**, **query parsing**
* Uses clean, maintainable **service-driven architecture**
* Full **Dockerized deployment**
* Real working **AI agent**
* Ready to extend into production

---

# 🙌 **Author**

Developed by **Abhishek S.**
*This project was completed as a 2-day AI Agent assignment.*