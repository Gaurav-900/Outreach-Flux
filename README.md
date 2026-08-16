# Outreach-Flux

**Outreach-Flux** is a personal AI-powered job-outreach system designed for relevance, quality, and controlled automation. Instead of mass-emailing job postings, it uses a highly targeted **Company-centric** approach: it discovers companies that are actively hiring for your profile, researches them, finds the best contacts, and drafts speculative, highly personalized outreach emails.

## 🚀 How It Works

The system operates on an automated, rotating scheduler that handles everything from discovery to drafting:

1. **Discovery**: Queries multiple job boards (FreeHire, Adzuna, TheMuse, AI Dev Jobs) to find roles matching your profile. It ignores the specific job and saves the **Company** as a target.
2. **Company Research**: Automatically scrapes the company's website and careers page to summarize what they do, their industry, and their tech stack.
3. **Contact Discovery**: 
   * **Public Extraction**: Scans the company's public HTML for recruiter or founder emails.
   * **Tomba Fallback**: If no public contacts exist, it uses the Tomba API to find verified employee email addresses based on the company's domain.
4. **AI Generation**: Uses **Gemini** (or DeepSeek) to ingest your `candidate.json` profile, the company research, and location preferences to write a highly tailored speculative pitch.
5. **Review & Send**: Drafts are populated in your React dashboard. You can manually approve and send them via the Gmail API, or enable Auto-Send for full automation.
6. **Reply Tracking**: Automatically tracks Gmail threads to detect if the response was a genuine human reply or an automated rejection/bounce.

## 💻 Tech Stack

* **Frontend**: React + Vite (TypeScript, Tailwind CSS)
* **Backend**: Python 3.12+ + FastAPI + Uvicorn
* **Database**: Supabase PostgreSQL (via `supabase-py`)
* **AI / LLMs**: Gemini (Primary) / DeepSeek (Fallback)
* **Data Providers**: Adzuna, TheMuse, FreeHire
* **Contact Enrichment**: Tomba
* **Email Provider**: Gmail API (OAuth)

## 🛠️ Setup & Installation

### Prerequisites
* Python 3.12+
* Node.js & npm
* A Supabase project with the schema applied
* API Keys (Gemini, Tomba, Adzuna, etc.)

### 1. Environment Configuration
Create a `.env` file in the `backend/` directory with your database connection strings, API keys, and Gmail credentials. **(Do not commit sensitive keys!)**

Configure your candidate profile in `backend/config/candidate.json`.

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Running the System
You can start both the backend API and the frontend dashboard simultaneously using the included startup script from the root directory:

```bash
./start.sh
```

- **Backend API**: runs on `http://localhost:5000`
- **Frontend Dashboard**: runs on `http://localhost:5173`

The Automation Orchestrator will automatically begin its discovery and generation ticks in the background.

## 🎯 Project Scope & Philosophy
The primary goal of Outreach-Flux is **quality over quantity**. It is not designed to bypass CAPTCHAs, spam thousands of recruiters, or operate as a multi-user SaaS. It is a single-user system designed to mimic the care and research of a manual job hunt, fully automated by AI.
