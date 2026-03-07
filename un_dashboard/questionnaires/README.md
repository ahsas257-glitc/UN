# Questionnaires

Each questionnaire has its own folder in this directory.

## Current questionnaire folders
- `gwo_beneficiaries/`
- `adsdo_beneficiaries/`
- `anbo_beneficiaries/`
- `arwe_beneficiaries/`
- `aspso_beneficiaries/`
- `dhdo_beneficiaries_men/`
- `dhdo_beneficiaries_women/`
- `ecoc_beneficiaries/`
- `ecoc_beneficiaries_male_guardians/`
- `gsro_beneficiaries/`
- `hhso_beneficiaries/`
- `hosaa_beneficiaries/`
- `ohad_beneficiaries/`
- `orstw_beneficiaries/`
- `ptcro_beneficiaries/`
- `rpo_beneficiaries/`
- `unw_beneficiary/`

## Structure
Each questionnaire package follows the same structure as `gwo_beneficiaries/`:
1. `__init__.py` exports `SCHEMA`.
2. `schema.py` defines a `QuestionnaireSchema` with:
- `indicator_candidates`
- `org_dashboard_tabs`
- `org_dashboard_tab_labels`

## Registration
`registry.py` discovers questionnaire packages dynamically; no manual import list is needed.
