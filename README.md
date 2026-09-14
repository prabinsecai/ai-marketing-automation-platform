# AI Marketing Automation & Campaign Intelligence Platform (Phase 1)

> A production-quality B2B marketing intelligence platform that automates campaign strategy formulation, multi-channel copy generation, variation editing, and stakeholder approval governance—strictly grounded in verified business facts and brand guidelines.

---

## 📌 Executive Summary

### Problem
Modern B2B marketing teams spend 70% of their campaign cycles in manual orchestration bottlenecks: drafting briefs, waiting days on multi-channel copy variations, cross-checking product truth to prevent misinformation, and circulating disorganized email threads for stakeholder sign-offs.

### Solution
This platform establishes an end-to-end, governed marketing intelligence workflow:
1. **Source of Truth**: Centralizes product capabilities, USPs, and buyer personas.
2. **AI Marketing Strategist**: Formulates deep, grounded campaign strategies (positioning, messaging, prioritized channels, themes, benchmarks, and risk mitigations).
3. **AI Multi-Channel Content Agent**: Generates tailored copy across Email, Social, and Paid Ads.
4. **Governance & Audit Trail**: Enables line-item copy editing, single-variation regeneration with feedback, selection toggles, and approval workflows.
5. **Real-time Dashboard**: Tracks real database metrics across campaign lifecycles and AI generation latency/token usage.

---

## 🏛️ System Architecture

```
                                ┌──────────────────────────────────────────────┐
                                │             Next.js 15 App Router            │
                                │   (Dashboard, Campaigns, Products, Audiences, │
                                │    Content Library, Approvals, AI Settings)  │
                                └──────────────────────┬───────────────────────┘
                                                       │ REST API (JSON)
                                                       ▼
                                ┌──────────────────────────────────────────────┐
                                │               FastAPI Backend                │
                                │   (Pydantic v2 Schemas, SQLAlchemy 2.0 ORM)  │
                                └──────────────┬────────────────┬──────────────┘
                                               │                │
                        ┌──────────────────────┴──────┐         │
                        ▼                             ▼         ▼
             ┌─────────────────────┐       ┌──────────────────────────────────┐
             │  PostgreSQL / SQLite│       │         AI Service Layer         │
             │ (Alembic Migrations)│       │  ┌────────────────────────────┐  │
             │                     │       │  │ BaseLLMProvider Interface  │  │
             │ - Workspaces        │       │  └──────────────┬─────────────┘  │
             │ - Products          │       │                 │                │
             │ - Audiences         │       │   ┌─────────────┼────────────┐   │
             │ - Campaigns         │       │   ▼             ▼            ▼   │
             │ - Strategies        │       │ [Mock]      [OpenAI]   [Anthropic│
             │ - Content Assets    │       │ Provider    Provider    Provider │
             │ - Approvals         │       └──────────────────────────────────┘
             │ - AI Execution Logs │
             └─────────────────────┘
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
- **CTA Strategy & Timeline**: Two-tier CTA ladder and phase-by-phase rollout.
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
| **Backend** | Python 3.12+, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, Pytest, Uvicorn |
| **Frontend** | Next.js 15 (App Router), TypeScript, Tailwind CSS, Lucide React, Framer Motion |
| **Database** | PostgreSQL 16 (production/Docker), SQLite (automatic local/test fallback) |
| **AI Layer** | Multi-Provider Architecture: `MockLLMProvider`, `OpenAIProvider`, `AnthropicProvider` |
| **Container** | Docker, Docker Compose |

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

# Execution Config
AI_TIMEOUT_SECONDS=45
AI_MAX_RETRIES=2

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
# From repository root
$env:PYTHONPATH="backend"; python -m pytest backend/tests -v
# Or on Linux/macOS:
PYTHONPATH=backend pytest backend/tests -v
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
│   │   │   ├── agents/          # MarketingStrategist & ContentAgent
│   │   │   ├── prompts/         # Grounded prompt templates
│   │   │   ├── providers/       # Mock, OpenAI, and Anthropic providers
│   │   │   ├── base.py          # Base provider interface & TokenUsage
│   │   │   └── factory.py       # LLM provider factory
│   │   ├── api/
│   │   │   └── v1/              # RESTful API routers (Campaigns, Strategy, Content, etc.)
│   │   ├── models/              # SQLAlchemy 2.0 ORM models
│   │   ├── schemas/             # Pydantic v2 schemas
│   │   ├── seed/                # Realistic B2B e-commerce demo seed data
│   │   ├── config.py            # Pydantic BaseSettings
│   │   ├── database.py          # SQLAlchemy session & fallback engine
│   │   └── main.py              # FastAPI application & startup lifespan
│   ├── alembic/                 # Database migration scripts
│   ├── tests/                   # Pytest test suite
│   ├── alembic.ini
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── campaigns/       # Campaigns list & detail pages
│   │   │   ├── products/        # Products & services catalog
│   │   │   ├── audiences/       # Target audience personas
│   │   │   ├── content/         # Global content library
│   │   │   ├── approvals/       # Dedicated reviewer queue
│   │   │   ├── settings/        # System settings & AI execution logs
│   │   │   ├── layout.tsx       # Root layout
│   │   │   └── page.tsx         # Dashboard page
│   │   ├── components/          # Reusable UI, Layout, and Campaign components
│   │   └── lib/                 # API client, TypeScript types, and utilities
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.ts
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
- The database auto-seeds realistic fictional B2B ecommerce data on startup:
  - **Company**: AuraFlow Commerce AI
  - **Products**: AuraFlow Omnichannel Engine, Nexus Dynamic Personalizer
  - **Audiences**: Mid-Market E-commerce Directors, D2C Performance Marketing Leads
  - **Campaigns**: Q3 Omnichannel Velocity Sprint (with complete strategy and content variations), Holiday Prep Sprint, Enterprise Omnichannel Modernization.

---

## 🛡️ Phase 1 Scope & Future Roadmap

### ✅ Implemented in Phase 1
- Workspace, Product, and Target Persona CRUD
- Campaign lifecycle management (`DRAFT` → `STRATEGY_GENERATED` → `CONTENT_GENERATED` → `IN_REVIEW` → `APPROVED`)
- AI Marketing Strategist (Positioning, message, channel tactics, themes, metrics, risks)
- AI Multi-Channel Content Agent (Email, Social, Paid Ads)
- Line-item editing with version history tracking
- Single-variation regeneration with feedback
- Governance approval workflows (`APPROVE`, `REJECT`, `REQUEST_CHANGES`)
- Real database dashboard metrics & AI latency/token audit logs
- Multi-provider abstraction (`mock`, `openai`, `anthropic`)
- Full Docker containerization and comprehensive Pytest test suite

### 🚫 Strict Phase 1 Boundaries (Deliberately Excluded)
To preserve architectural purity and reliability, the following are reserved for future phases:
- Real email dispatching (e.g. SendGrid, Mailgun)
- Social media publishing APIs (e.g. LinkedIn API, Twitter API)
- CRM & external webhook sync (e.g. HubSpot, Salesforce, n8n)
- Automated campaign execution scheduling
- Real-time conversion tracking & ROI optimization engines

---

## 📜 License
MIT License. Built with ❤️ for high-performance marketing and growth engineering teams.
