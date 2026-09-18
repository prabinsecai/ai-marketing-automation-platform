# AI Marketing Automation & Campaign Intelligence Platform

> A production-quality B2B marketing intelligence and autonomous execution platform that formulates grounded campaign strategies, generates multi-channel copy variations, governs stakeholder approval pipelines, and executes approved campaigns using **LangGraph** and **local n8n** workflows with automated retries and human escalation.

---

## 📌 Executive Summary

### Problem
Modern B2B marketing teams spend 70% of their campaign cycles in manual orchestration bottlenecks: drafting briefs, waiting days on multi-channel copy variations, cross-checking product truth to prevent misinformation, circulating disorganized email threads for stakeholder sign-offs, and manually copying assets into disparate automation and CRM dispatch tools.

### Solution
This platform establishes an end-to-end, governed marketing intelligence and execution workflow:
1. **Source of Truth**: Centralizes verified product capabilities, USPs, and target buyer personas.
2. **AI Marketing Strategist**: Formulates deep, grounded campaign strategies (positioning, messaging, prioritized channels, themes, benchmarks, and risk mitigations).
3. **AI Multi-Channel Content Agent**: Generates tailored copy across Email, Social, and Paid Ads with line-item editing and single-variation regeneration.
4. **Governance & Approval Gate**: Strict approval workflows requiring explicit sign-off before campaign execution is unlocked.
5. **Campaign Execution Agent (LangGraph)**: Multi-node state machine that validates approval, plans channel execution, dispatches payloads to local n8n, handles transient errors, and escalates to humans after retries.
6. **Local n8n Workflow Automation**: Dispatches webhooks to local n8n instances (`http://localhost:5678`) with seamless offline fallback simulation.
7. **Real-Time Observability**: Complete execution timeline, LangGraph node step logs, token/latency metrics, and global execution dashboard.

---

## 🏛️ System Architecture

```
                                ┌──────────────────────────────────────────────┐
                                │             Next.js 15 App Router            │
                                │   (Dashboard, Campaigns, Executions, Products,│
                                │    Audiences, Content, Approvals, AI Logs)   │
                                └──────────────────────┬───────────────────────┘
                                                       │ REST API (JSON)
                                                       ▼
                                ┌──────────────────────────────────────────────┐
                                │               FastAPI Backend                │
                                │   (Pydantic v2 Schemas, SQLAlchemy 2.0 ORM)  │
                                └──────────┬──────────────────────┬────────────┘
                                           │                      │
             ┌─────────────────────────────┼──────────────────────┼─────────────────────────────┐
             ▼                             ▼                      ▼                             ▼
  ┌─────────────────────┐       ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
  │  PostgreSQL / SQLite│       │   AI Service Layer   │  │ LangGraph Exec Agent │  │ Local n8n Automation │
  │ (Alembic Migrations)│       │                      │  │                      │  │ (http://localhost:   │
  │                     │       │ - Mock Provider      │  │ 1. Validate Approval │  │  5678)               │
  │ - Workspaces        │       │ - OpenAI Provider    │  │ 2. Plan Execution    │  │                      │
  │ - Products          │       │ - Anthropic Provider │  │ 3. Dispatch n8n Webhk│  │ - Campaign Execute   │
  │ - Audiences         │       │ - Marketing Strat.   │  │ 4. Evaluate Result   │  │ - Lead Follow-up     │
  │ - Campaigns         │       │ - Content Agent      │  │ 5. Safe Retries      │  │ - Mock Email / CRM   │
  │ - Executions & Steps│       └──────────────────────┘  │ 6. Human Escalation  │  │ - Asynchronous Callbk│
  │ - Approvals & Logs  │                                 └──────────┬───────────┘  └──────────┬───────────┘
  └─────────────────────┘                                            │                         │
                                                                     └────── POST Webhook ─────┘
```

---

## 🚀 Key Features

### 1. Workspaces & Ground-Truth Context
- Manage brand voice guidelines, tone, prohibited terms, and website URLs.
- Isolate campaigns, products, audiences, and AI audit logs per workspace.

### 2. Product & Target Buyer Catalogs
- Define structured product features, pricing, target benefits, and USPs.
- Define audience personas with demographic data, core pain points, professional goals, and preferred channels.
- **Anti-Hallucination Grounding**: Prompt templates explicitly instruct AI agents to only use verified facts.

### 3. Campaign Workflow Pipeline
Strict 5-stage progression:
```text
DRAFT
  └──> STRATEGY_GENERATED
         └──> CONTENT_GENERATED
                └──> IN_REVIEW
                       └──> APPROVED
```

### 4. AI Marketing Strategist
Generates structured strategic intelligence including:
- **Campaign Summary & Positioning**: Market positioning statement and differentiation.
- **Key Message**: Memorable narrative anchor.
- **Audience Reasoning**: Behavioral and psychological breakdown of conversion drivers.
- **Channel Strategy**: Prioritization (Primary/Secondary), rationale, and execution tactics.
- **Core Campaign Themes**: Distinct narrative hooks addressing buyer pain points.
- **Content Recommendations**: Specific asset types and channel best practices.
- **CTA Strategy & Timeline**: Two-tier CTA ladder and staged rollout.
- **Success Metrics & Risks**: Concrete KPI benchmarks and risk mitigation pairs.

### 5. AI Multi-Channel Content Agent
Generates channel-specific variations:
- **Email Copy**: Subject line, preview preheader, structured body, and crisp CTA.
- **Social Posts**: Platform optimization (LinkedIn, Twitter/X, Instagram), opening hook, caption, CTA, and hashtags.
- **Paid Advertisements**: High-CTR headline, primary value copy, and action CTA.
- **Variation Controls**:
  - Full inline editing with change summary and version history tracking.
  - Single-variation regeneration incorporating custom prompt instructions.
  - Selection toggle (`is_selected`) to mark winning variations for deployment.
  - Formal approval actions (`APPROVE`, `REJECT`, `REQUEST_CHANGES`) with reviewer feedback.

### 6. Observability & Real-Time Dashboard
- Live database-derived counts (Total campaigns, Drafts, In Review, Approved, Products, Audiences).
- Lifecycle status funnel.
- Recent AI execution feed displaying model name, latency (ms), token usage, and prompt previews.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.12+, FastAPI, LangGraph, LangChain, SQLAlchemy 2.0, Alembic, Pydantic v2, Pytest, Uvicorn |
| **Frontend** | Next.js 15 (App Router), TypeScript, Tailwind CSS, Lucide React, Framer Motion |
| **Database** | PostgreSQL 16 (production/Docker), SQLite (automatic local/test fallback) |
| **AI Layer** | Multi-Provider Architecture: `MockLLMProvider`, `OpenAIProvider`, `AnthropicProvider`, `CampaignExecutionAgent` (LangGraph) |
| **Automation** | Local n8n (`http://localhost:5678`), Webhooks, Simulated Fallback Engine |
| **Container** | Docker, Docker Compose |

---

## ⚡ LangGraph Campaign Execution & Local n8n Automation

### 1. LangGraph State Machine Architecture

```
  [validate_approval] ──(Blocked / Unapproved)──> [END / Blocked]
          │
      (Approved)
          ▼
   [plan_execution]
          │
          ▼
  [dispatch_workflows] ──(POST /webhook/campaign-execute)──> [Local n8n]
          │
          ▼
   [evaluate_result] ────(Success)───> [END / Complete]
          │
      (Failure)
          ├────(retries < max)────> [handle_retry] ──> [dispatch_workflows]
          └────(retries >= max)───> [escalate] ────> [END / Human Review]
```

### 2. Imported n8n Workflows (`n8n/workflows/`)

- `campaign_execution.json`: Primary multi-channel distribution webhook receiver with callback loop.
- `lead_followup.json`: Lead scoring and routing automation for campaign engagements.
- `mock_email_dispatch.json`: Enterprise simulated SMTP / SES email transmission engine.
- `mock_crm_sync.json`: Automated audience sync to HubSpot / Salesforce CRM records.

### 3. Local n8n Execution & Offline Resilience

1. **Live Mode**: If local n8n is running on `http://localhost:5678`, the LangGraph agent dispatches live HTTP webhooks directly to active workflows.
2. **Offline Simulated Mode**: When n8n is offline or unreachable in local development / CI environments, the client automatically falls back to an offline simulated engine with deterministic IDs and complete audit logging—ensuring 100% zero-friction development and passing tests.

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory (see `.env.example`):

```bash
# Project Info
PROJECT_NAME="AI Marketing Automation & Campaign Intelligence Platform"
ENVIRONMENT="development"
DEBUG=True

# Database
DATABASE_URL="postgresql+psycopg2://postgres:postgrespassword@localhost:5432/marketing_platform"
DATABASE_FALLBACK_SQLITE=True
SQLITE_DB_PATH="sqlite:///./marketing_platform.db"

# AI Provider ("mock" | "openai" | "anthropic")
LLM_MODE="mock"

# OpenAI (Required only if LLM_MODE=openai)
OPENAI_API_KEY=""
OPENAI_MODEL="gpt-4o-mini"

# Anthropic (Required only if LLM_MODE=anthropic)
ANTHROPIC_API_KEY=""
ANTHROPIC_MODEL="claude-3-5-haiku-20241022"

# AI Execution Config
AI_TIMEOUT_SECONDS=45
AI_MAX_RETRIES=2

# Local n8n Integration
# When running n8n natively on Windows/macOS and the backend in Docker,
# set this to host.docker.internal instead of localhost (done automatically in docker-compose.yml)
N8N_BASE_URL="http://localhost:5678"
N8N_WEBHOOK_CAMPAIGN_EXECUTE="/webhook/campaign-execute"
N8N_WEBHOOK_LEAD_FOLLOWUP="/webhook/lead-followup"
N8N_WEBHOOK_SECRET="marketing-automation-n8n-secret"
MAX_EXECUTION_RETRIES=3

# Frontend
NEXT_PUBLIC_API_URL="http://localhost:8000/api/v1"
```

---

## 🏃 Quick Start & Local Setup

### 1. Backend Setup

```bash
cd backend
python -m pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```
Backend will be available at `http://localhost:8000` (Swagger UI at `http://localhost:8000/docs`).
*Note: If PostgreSQL is not active locally, the backend automatically utilizes SQLite fallback with zero setup needed.*

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
Frontend will be available at `http://localhost:3000`.

---

## 🐳 Docker Deployment

To launch the complete stack (PostgreSQL + FastAPI + Next.js):

```bash
# Build and run all services
docker compose up --build -d

# View logs
docker compose logs -f

# Teardown
docker compose down
```

---

## 🧪 Testing & Quality Validation

### 1. Run Backend Pytest Suite

```bash
# From backend/ directory
pytest -v
```

### 2. Frontend Type Checking & Build Validation

```bash
cd frontend

# TypeScript compilation check
npx tsc --noEmit

# ESLint validation
npm run lint

# Production build test
npm run build
```

---

## 📂 Project Structure

```
ai-marketing-automation-platform/
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── agents/          # MarketingStrategist, ContentAgent, CampaignExecutionAgent (LangGraph)
│   │   │   ├── prompts/         # Grounded prompt templates
│   │   │   ├── providers/       # Mock, OpenAI, and Anthropic providers
│   │   │   ├── base.py          # Base provider interface & TokenUsage
│   │   │   ├── factory.py       # LLM provider factory
│   │   │   └── n8n_client.py    # Local n8n client with simulated fallback
│   │   ├── api/
│   │   │   └── v1/              # RESTful API routers (Campaigns, Strategy, Content, Executions, Webhooks)
│   │   ├── models/              # SQLAlchemy 2.0 ORM models (CampaignExecution, ExecutionStep, etc.)
│   │   ├── schemas/             # Pydantic v2 schemas
│   │   ├── seed/                # Realistic B2B SaaS demo seed data
│   │   ├── config.py            # Pydantic BaseSettings
│   │   ├── database.py          # SQLAlchemy session & fallback engine
│   │   └── main.py              # FastAPI application & startup lifespan
│   ├── alembic/                 # Database migrations
│   ├── tests/                   # Pytest test suite (16 comprehensive unit & integration tests)
│   ├── alembic.ini
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── campaigns/       # Campaigns list & detail pages (with Execution controls & timeline)
│   │   │   ├── executions/      # Global Campaign Executions Dashboard & Agent Trace Viewer
│   │   │   ├── products/        # Products & services catalog
│   │   │   ├── audiences/       # Target audience personas
│   │   │   ├── content/         # Global content library
│   │   │   ├── approvals/       # Dedicated reviewer queue
│   │   │   ├── settings/        # System settings & AI execution logs
│   │   │   ├── layout.tsx       # Root layout with Executions navigation
│   │   │   └── page.tsx         # Real-time marketing & execution dashboard
│   │   ├── components/          # Reusable UI, Layout, and Campaign components
│   │   └── lib/                 # API client, TypeScript types, and utilities
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.ts
├── n8n/
│   ├── workflows/               # Workflow templates (campaign_execution, lead_followup, etc.)
│   ├── examples/                # Sample webhook payloads
│   └── README.md                # n8n setup and architecture guide
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🎯 Demo Mode & Sample Data

The platform comes pre-configured with **`LLM_MODE=mock`** by default:
- Works 100% offline with zero paid API keys.
- Generates rich, context-specific marketing strategies and copy variations tailored to the chosen product and persona.
- The database auto-seeds realistic fictional B2B SaaS data on startup:
  - **Company**: AuraFlow Commerce AI
  - **Products**: AuraFlow Omnichannel Engine, Nexus Dynamic Personalizer
  - **Audiences**: Mid-Market E-commerce Directors, D2C Performance Marketing Leads
  - **Campaigns**: Q3 Omnichannel Velocity Sprint (Approved with selected copy, ready for execution), Holiday Prep Sprint, Enterprise Omnichannel Modernization.

---

## 🛡️ Completed Deliverables

- Workspace, Product, and Target Persona Catalog
- 5-stage Campaign Lifecycle Management (`DRAFT` → `STRATEGY_GENERATED` → `CONTENT_GENERATED` → `IN_REVIEW` → `APPROVED`)
- AI Marketing Strategist (Positioning, message, channel tactics, themes, metrics, risks)
- AI Multi-Channel Content Agent (Email, Social, Paid Ads)
- Line-item copy editing with version history tracking
- Single-variation regeneration with feedback
- Governance approval workflows (`APPROVE`, `REJECT`, `REQUEST_CHANGES`)
- AI Token Usage & Observability Dashboard
- **LangGraph Campaign Execution Agent**: Multi-node state machine with strict approval validation.
- **Local n8n Workflow Integration**: Real HTTP webhook dispatching (`http://localhost:5678`) with resilient offline simulation fallback.
- **Asynchronous Webhook Callback Receiver**: `POST /api/v1/webhooks/n8n/result` with secret validation and database update loop.
- **Execution Tracking & Auditability**: `CampaignExecution` and `ExecutionStep` models tracking node-level inputs, outputs, errors, and traces.
- **Idempotency & Concurrency Guards**: Idempotency key deduplication and conflict prevention for active runs.
- **Automatic Retry & Human Escalation**: Automatic retry scheduling up to max configured attempts, followed by automated transition to `ESCALATED` state.
- **Executions Dashboard & Campaign Controls**: Real-time execution monitor, step timeline, JSON inspector, and manual retry controls in Next.js UI.
- Comprehensive test suite with 100% pass rate across AI agents, CRUD APIs, LangGraph state machine, idempotency, callbacks, and escalations.
- Real database dashboard metrics & AI latency/token audit logs
- Multi-provider abstraction (`mock`, `openai`, `anthropic`)
- Full Docker containerization and comprehensive Pytest test suite

### 🔮 Future Extensions (Reserved)
To preserve architectural purity and reliability, the following are reserved for future development:
- Real email dispatching (e.g. SendGrid, Mailgun)
- Social media publishing APIs (e.g. LinkedIn API, Twitter API)
- CRM & external webhook sync (e.g. HubSpot, Salesforce, n8n)
- Automated campaign execution scheduling
- Real-time conversion tracking & ROI optimization engines

---

## 📜 License
MIT License. Built with ❤️ for high-performance marketing and growth engineering teams.
