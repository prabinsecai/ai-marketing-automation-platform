# Local n8n Workflow Automation Architecture

This directory contains n8n workflow templates, webhook trigger specifications, and sample payloads for the **AI Marketing Automation & Campaign Intelligence Platform** (Phase 2).

## Overview

The Platform executes approved campaigns through a dual-mode integration:
1. **Live Local n8n Instance** (`http://localhost:5678`): Dispatches HTTP webhooks directly into imported n8n workflows.
2. **Offline Simulated Engine**: When n8n is offline or unreachable in local/CI environments, the LangGraph Execution Agent automatically simulates successful webhook delivery and callback loops with full traceability.

---

## Workflows Included

| Workflow | File | Description |
| :--- | :--- | :--- |
| **Campaign Execution** | `workflows/campaign_execution.json` | Main orchestration workflow receiving approved campaign payloads and coordinating multi-channel distribution. |
| **Lead Follow-up** | `workflows/lead_followup.json` | Scores lead engagement and triggers high-priority outreach vs. nurture sequences. |
| **Mock Email Dispatch** | `workflows/mock_email_dispatch.json` | Simulates enterprise SMTP/SES email delivery for email assets. |
| **Mock CRM Sync** | `workflows/mock_crm_sync.json` | Simulates audience and contact sync into HubSpot/Salesforce CRMs. |

---

## How to Import Workflows into Local n8n

1. Start your local n8n instance:
   ```bash
   npx n8n start
   ```
   or via Docker:
   ```bash
   docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
   ```
2. Open `http://localhost:5678` in your browser.
3. In the left navigation menu, click **Workflows** → **Import from File...**
4. Select any of the `.json` files from `n8n/workflows/`.
5. Activate the workflow toggle in the top-right corner.

---

## Webhook Endpoints & Communication Flow

```
+------------------------------------+
|  FastAPI + LangGraph Agent         |
|  (Execution Agent Node)            |
+-----------------+------------------+
                  |
         POST /webhook/campaign-execute
                  |
                  v
+-----------------+------------------+
|  Local n8n Workflow Engine         |
|  (http://localhost:5678)           |
+-----------------+------------------+
                  |
         POST /api/v1/webhooks/n8n/result
                  |
                  v
+-----------------+------------------+
|  FastAPI Webhook Handler           |
|  (Updates CampaignExecution Status)|
+------------------------------------+
```
