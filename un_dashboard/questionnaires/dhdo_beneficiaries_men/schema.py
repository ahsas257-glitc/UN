"""Auto-generated questionnaire schema from XLSForm."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="dhdo_beneficiaries_men",
    title="DHDO Beneficiaries Men",
    indicator_candidates={
        "consent": [
            "consent",
            "consent_to_participate",
            "does_the_person_consent_to_participate",
            "Does the person consent to participate?",
        ],
        "gender": [
            "gender",
            "confirm_gender",
            "Confirm gender",
        ],
        "training": [
            "attended_training",
            "participation",
            "attend",
            "session_attended",
            "Did you attend training sessions organized by DHDO?",
            "training_purpose",
            "What was the purpose of the training, as you understood it?",
            "training_duration",
            "Approximately how long did the training last?",
            "selection_clarity",
            "Before the training, was the selection criteria and process clearly explained to you?",
            "training_meet_needs",
            "The training met your needs.",
            "safe_access",
            "Do you feel safe and secure accessing the training?",
            "received_materials",
            "Did you receive materials or tools after the training?",
            "household_changes",
            "Have you observed any changes in the household since participation?",
        ],
        "helpful": [
            "helpful",
            "training_helped",
            "service_satisfaction",
            "kit_quality_sat",
            "market_helpful",
            "record_ok",
            "For note-taking/quality assurance, may we record the interview?",
            "How satisfied are you with the services you received?",
            "Were you satisfied with the quality of the input/kit?",
        ],
        "complaint_awareness": [
            "know_contact",
            "informed_complaints",
            "informed_concerns",
            "complaint",
            "concern",
            "Were you informed about how concerns or complaints can be raised?",
            "Do you know whom to contact if there is a concern?",
        ],
        "date": [
            "date_time",
            "start",
            "submissiondate",
            "today",
            "interview_date",
            "sufficient_start",
            "Were the materials sufficient to start production?",
        ],
    },
    org_dashboard_tabs={
        "general": {
            "audio": [
                "audio",
                "audio",
            ],
        },
        "sample_info": {
            "name_of_the_enumerator": [
                "Surveyor Name:",
                "Name_of_the_enumerator",
            ],
            "province": [
                "Province",
                "Province",
            ],
            "district": [
                "District",
                "District",
            ],
            "village": [
                "Village name:",
                "Village",
            ],
        },
        "consent_grp": {
            "consent": [
                "Does the person consent to participate?",
                "consent",
            ],
            "record_ok": [
                "For note-taking/quality assurance, may we record the interview?",
                "record_ok",
            ],
        },
        "resp_details": {
            "age_group": [
                "Age group",
                "age_group",
            ],
            "gender": [
                "Confirm gender",
                "gender",
            ],
            "marital": [
                "Confirm marital status",
                "marital",
            ],
            "education": [
                "Level of education",
                "education",
            ],
            "employment": [
                "Employment status",
                "employment",
            ],
            "hh_members": [
                "Number of household members",
                "hh_members",
            ],
            "avg_income": [
                "Average income per month (local currency)",
                "avg_income",
            ],
        },
        "training_part": {
            "attended_training": [
                "Did you attend training sessions organized by DHDO?",
                "attended_training",
            ],
            "training_purpose": [
                "What was the purpose of the training, as you understood it?",
                "training_purpose",
            ],
            "training_duration": [
                "Approximately how long did the training last?",
                "training_duration",
            ],
            "selection_clarity": [
                "Before the training, was the selection criteria and process clearly explained to you?",
                "selection_clarity",
            ],
            "training_meet_needs": [
                "The training met your needs.",
                "training_meet_needs",
            ],
            "safe_access": [
                "Do you feel safe and secure accessing the training?",
                "safe_access",
            ],
            "service_satisfaction": [
                "How satisfied are you with the services you received?",
                "service_satisfaction",
            ],
        },
        "recall_grp": {
            "topics_discussed": [
                "What topics were discussed?",
                "topics_discussed",
            ],
            "topics_discussed_other": [
                "Specify other topic",
                "topics_discussed_other",
            ],
        },
        "inputs_grp": {
            "received_materials": [
                "Did you receive materials or tools after the training?",
                "received_materials",
            ],
            "recv_raw": [
                "Raw materials",
                "recv_raw",
            ],
            "recv_raw_details": [
                "Details / quantity (as known)",
                "recv_raw_details",
            ],
            "recv_tools": [
                "Tools (scissors, glue, etc.)",
                "recv_tools",
            ],
            "recv_tools_details": [
                "Details / quantity (as known)",
                "recv_tools_details",
            ],
            "recv_other": [
                "Other inputs",
                "recv_other",
            ],
            "recv_other_details": [
                "Details / quantity (as known)",
                "recv_other_details",
            ],
            "receive_when": [
                "When were these items received?",
                "receive_when",
            ],
            "sufficient_start": [
                "Were the materials sufficient to start production?",
                "sufficient_start",
            ],
            "kit_quality_sat": [
                "Were you satisfied with the quality of the input/kit?",
                "kit_quality_sat",
            ],
        },
        "use_grp": {
            "woman_producing": [
                "Is the woman beneficiary currently producing artificial flowers?",
                "woman_producing",
            ],
            "materials_use_desc": [
                "How are the materials being used?",
                "materials_use_desc",
            ],
            "sold_products": [
                "Are the products being sold?",
                "sold_products",
            ],
            "sales_support_type": [
                "If yes, how are you supporting sales or marketing?",
                "sales_support_type",
            ],
            "sales_support_other": [
                "Other (specify)",
                "sales_support_other",
            ],
            "no_production_reasons": [
                "If no production is ongoing, what are the main reasons?",
                "no_production_reasons",
            ],
            "no_production_other": [
                "Other (specify)",
                "no_production_other",
            ],
        },
        "changes_grp": {
            "household_changes": [
                "Have you observed any changes in the household since participation?",
                "household_changes",
            ],
            "household_changes_other": [
                "Other (specify)",
                "household_changes_other",
            ],
            "changes_narrative": [
                "Please explain (open narrative)",
                "changes_narrative",
            ],
        },
        "acc_grp": {
            "informed_complaints": [
                "Were you informed about how concerns or complaints can be raised?",
                "informed_complaints",
            ],
            "know_contact": [
                "Do you know whom to contact if there is a concern?",
                "know_contact",
            ],
        },
    },
    org_dashboard_tab_labels={
        "general": "General",
        "sample_info": "Sample Information",
        "consent_grp": "Consent & Introduction",
        "resp_details": "Respondent details",
        "training_part": "Participation in training",
        "recall_grp": "Training content recall",
        "inputs_grp": "Receipt of inputs / kits",
        "use_grp": "Use of skills and inputs",
        "changes_grp": "Perceived changes",
        "acc_grp": "Accountability and safeguarding",
    },
)
