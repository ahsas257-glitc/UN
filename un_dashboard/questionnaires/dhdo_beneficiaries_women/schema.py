"""Auto-generated questionnaire schema from XLSForm."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="dhdo_beneficiaries_women",
    title="DHDO Beneficiaries Women",
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
            "Did you attend training organised by DHDO?",
            "training_type",
            "What type of training did you attend?",
            "training_duration",
            "Approximately how long did the training last?",
            "selection_clarity",
            "Before the training, was the selection criteria and process clearly explained to you?",
            "training_meet_needs",
            "Did the training meet your needs?",
            "safe_access",
            "Do you feel safe and secure accessing the training?",
            "received_materials",
            "Did you receive any materials or tools after the training?",
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
            "activity_helped",
            "Has this activity helped you in any way?",
        ],
        "complaint_awareness": [
            "know_contact",
            "informed_complaints",
            "informed_concerns",
            "complaint",
            "concern",
            "Were you informed about how to raise a complaint or concern?",
            "Do you know whom to contact if you have a concern?",
        ],
        "date": [
            "date_time",
            "start",
            "submissiondate",
            "today",
            "interview_date",
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
                "Did you attend training organised by DHDO?",
                "attended_training",
            ],
            "training_type": [
                "What type of training did you attend?",
                "training_type",
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
                "Did the training meet your needs?",
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
                "What topics were covered? (Tick all mentioned)",
                "topics_discussed",
            ],
            "topics_discussed_other": [
                "Others (specify)",
                "topics_discussed_other",
            ],
        },
        "inputs_grp": {
            "received_materials": [
                "Did you receive any materials or tools after the training?",
                "received_materials",
            ],
            "recv_raw": [
                "Raw materials",
                "recv_raw",
            ],
            "recv_raw_details": [
                "Details / Quantity",
                "recv_raw_details",
            ],
            "recv_tools": [
                "Tools (scissors, glue, etc.)",
                "recv_tools",
            ],
            "recv_tools_details": [
                "Details / Quantity",
                "recv_tools_details",
            ],
            "recv_other": [
                "Other inputs",
                "recv_other",
            ],
            "recv_other_details": [
                "Details / Quantity",
                "recv_other_details",
            ],
            "receive_when": [
                "When did you receive these items?",
                "receive_when",
            ],
            "kit_quality_sat": [
                "Were you satisfied with the quality of the input/kit?",
                "kit_quality_sat",
            ],
        },
        "use_grp": {
            "currently_making": [
                "Are you currently making artificial flowers?",
                "currently_making",
            ],
            "skills_use_narrative": [
                "If yes/partly, how are you using the skills? (Record narrative)",
                "skills_use_narrative",
            ],
            "no_production_reasons": [
                "If no, what are the main reasons?",
                "no_production_reasons",
            ],
            "no_production_other": [
                "Other (specify)",
                "no_production_other",
            ],
        },
        "changes_grp": {
            "activity_helped": [
                "Has this activity helped you in any way?",
                "activity_helped",
            ],
            "help_how": [
                "If yes, how?",
                "help_how",
            ],
            "help_other": [
                "Other (specify)",
                "help_other",
            ],
            "challenges_open": [
                "What challenges have you faced in continuing this activity? (Open-ended)",
                "challenges_open",
            ],
        },
        "acc_grp": {
            "informed_complaints": [
                "Were you informed about how to raise a complaint or concern?",
                "informed_complaints",
            ],
            "know_contact": [
                "Do you know whom to contact if you have a concern?",
                "know_contact",
            ],
        },
    },
    org_dashboard_tab_labels={
        "general": "General",
        "sample_info": "Sample Information",
        "consent_grp": "Consent & Introduction",
        "resp_details": "Respondent details",
        "training_part": "Participation in Training",
        "recall_grp": "Training Content Recall",
        "inputs_grp": "Receipt of Inputs / Kits",
        "use_grp": "Use of Skills and Inputs (Self-Reported)",
        "changes_grp": "Perceived Changes and Challenges",
        "acc_grp": "Accountability and Safeguarding",
    },
)
