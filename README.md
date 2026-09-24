# LeadFlow

LeadFlow is a multi-source sales lead automation platform built with
n8n, FastAPI, PostgreSQL and React.

## Current Implementation — Stage 2

- Authenticated n8n webhook
- Lead normalization and validation
- Structured validation errors
- FastAPI REST API
- PostgreSQL persistence
- Email-based lead deduplication
- Alembic database migrations
- Google Sheets lead and error logging
- Docker Compose development environment

## Current Workflow

Website/API
→ n8n webhook
→ validation
→ FastAPI
→ PostgreSQL deduplication
→ Google Sheets
→ webhook response

## API Endpoints

- `GET /health`
- `GET /health/db`
- `POST /api/v1/leads`


## Sample request

The lead-intake webhook accepts JSON in the following format:

```json
{
    "full_name": "Layla Hassan",
    "email": "LAYLA@NOVA.TEST",
    "company": "Nova Systems",
    "role": "Sales Director",
    "website": "https://nova.test",
    "source": "Website",
    "notes": "Interested in lead automation"
}
```

Supported source values are:

- `website`
- `form`
- `api`
- `facebook_ads`
- `extension`
- `playwright`
- `manual`

### Example request

```bash
curl -i \
  -X POST \
  http://localhost:5678/webhook/leadflow/intake \
  -H 'Content-Type: application/json' \
  -H "X-LeadFlow-Key: {YOUR_KEY}" \
  --data-raw '{
    "full_name": "Layla Hassan",
    "email": "LAYLA@NOVA.TEST",
    "company": "Nova Systems",
    "role": "Sales Director",
    "website": "https://nova.test",
    "source": "Website",
    "notes": "Interested in lead automation"
  }'
```

## Security

Credentials and webhook keys are stored in n8n's encrypted credential
store and are not included in exported workflows.
