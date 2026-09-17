# LeadFlow

LeadFlow is a multi-source sales lead automation platform built with
n8n, FastAPI, PostgreSQL and React.

## Stage 1

The first workflow currently:

- Accepts leads through an authenticated webhook
- Normalizes incoming fields
- Validates names, emails, companies, URLs and sources
- Returns structured 201 or 400 responses
- Stores accepted leads in Google Sheets
- Logs rejected leads and validation errors separately

## Current workflow

Webhook → Normalize → Validate → Route
- Valid → Google Sheets Leads → 201
- Invalid → Google Sheets Errors → 400

## Sample request

The lead-intake webhook accepts JSON in the following format:

```json
{
  "full_name": "Sarah Khan",
  "email": "sarah@acme.test",
  "company": "Acme",
  "role": "Operations Manager",
  "website": "https://acme.test",
  "source": "website",
  "notes": "Interested in CRM automation"
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
curl -X POST \
  http://localhost:5678/webhook/leadflow/intake \
  -H 'Content-Type: application/json' \
  -H 'X-LeadFlow-Key: <your-webhook-key>' \
  --data-raw '{
    "full_name": "Sarah Khan",
    "email": "sarah@acme.test",
    "company": "Acme",
    "role": "Operations Manager",
    "website": "https://acme.test",
    "source": "website",
    "notes": "Interested in CRM automation"
  }'
```

## Security

Credentials and webhook keys are stored in n8n's encrypted credential
store and are not included in exported workflows.
