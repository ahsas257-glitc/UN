# UN Women Dashboard (Advanced Liquid Glass Edition)

This Streamlit app now has a modular architecture, a modern Liquid Glass UI system, and adaptive multi-project dashboards.

## Features
- Public dashboard with KPI cards and org-level progress analytics
- Public report export (Excel)
- Advanced insights (trend analysis + concentration heatmap + top performers)
- Organization module:
  - Dashboard
  - Report
  - Dataset updater (Excel to Google Sheet append)
  - Pivot Tables
  - Chart Builder
- Adaptive questionnaire dashboards:
  - Parses XLSForm files from `XLS_FORMS_DIR` (or local default path)
  - Builds section-wise smart tabs per project automatically
- Fully themed Liquid Glass design
  - Theme is locked to admin settings (hidden user toolbar/theme toggle)
- Strict visual mode behavior:
  - Dark mode: full black background + white text/values
  - Light mode: full white background + black text/values
- Questionnaire architecture:
  - Each questionnaire has its own dedicated folder under `un_dashboard/questionnaires/`
  - Switch questionnaire from sidebar (`Survey Form`)
  - GWO dashboard now includes full XLSForm-aligned tabs:
    - Sample Information
    - Respondent details
    - Participation in training
    - Receipt of production kits
    - Use of skills and inputs
    - Market and perceived changes
    - Household and safeguarding

## Project structure
```text
D:\UN
├── app.py
├── .streamlit\config.toml
├── requirements.txt
└── un_dashboard
    ├── app.py
    ├── core
    │   └── constants.py
    ├── design
    │   └── theme.py
    ├── questionnaires
    │   ├── base.py
    │   ├── registry.py
    │   ├── gwo_beneficiaries
    │   │   └── schema.py
    │   └── unw_beneficiary
    │       └── schema.py
    ├── services
    │   ├── exporter.py
    │   ├── sheets.py
    │   ├── transforms.py
    │   └── translation.py
    └── views
        ├── gwo_dashboard.py
        ├── organization.py
        └── public.py
```

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud
- Entry point: `app.py`
- Theme is controlled by admin config/secrets and user theme toggle is hidden.
- Optional forms directory for adaptive dashboards:
  - `XLS_FORMS_DIR = "C:/Users/LENOVO/Documents/XLS_Forms"`
- Optional locked theme override:
  - `LOCKED_THEME_MODE = "dark"` or `"light"`

## Required secrets (for translation updater workflow)
Add these in Streamlit Cloud `Secrets`:

```toml
SHEET_URL = "https://docs.google.com/spreadsheets/d/.../edit"
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL = "gpt-4o-mini"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
universe_domain = "googleapis.com"
```

## correction_log format
Sheet name must be `correction_log` with columns:
- `_uuid`
- `Label`
- `old_value`
- `new_value`
