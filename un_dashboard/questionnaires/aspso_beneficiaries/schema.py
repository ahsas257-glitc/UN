"""Auto-generated questionnaire schema from XLSForm."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="aspso_beneficiaries",
    title="ASPSO Beneficiaries",
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
            "Did you attend any training organised by ASPSO?",
            "training_type",
            "What type of training did you attend?",
            "training_type_other",
            "Other training type (specify)",
            "training_duration",
            "Approximately how long did the training last?",
            "selection_clarity",
            "Before the training, were the selection criteria and process clearly explained to you?",
            "topics_covered",
            "What topics were covered in your training? (Select all that apply)",
            "received_items",
            "Did you receive any items or materials after the training?",
            "recv_tools",
            "Tools or equipment related to training (received?)",
            "training_met_needs",
            "The training met my needs.",
            "safe_access_training",
            "Do you feel safe and secure accessing the training?",
            "training_helped",
            "Has the training helped you in any way?",
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
            "kit_quality_satisfaction",
            "Were you satisfied with the quality of the input/kit?",
            "Has the training helped you in any way?",
            "helped_how",
            "If yes, how? (Select all that apply)",
            "helped_how_other",
            "Other (specify)",
        ],
        "complaint_awareness": [
            "know_contact",
            "informed_complaints",
            "informed_concerns",
            "complaint",
            "concern",
            "informed_complaint",
            "Were you informed about how to raise a concern or complaint related to this project?",
            "Do you know whom to contact if you have a concern?",
        ],
        "date": [
            "date_time",
            "start",
            "submissiondate",
            "today",
            "interview_date",
            "recv_raw",
            "Raw materials / starter supplies (received?)",
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
            "skill_area": [
                "Intervention / skill area",
                "skill_area",
            ],
            "skill_area_other": [
                "Other skill area (specify)",
                "skill_area_other",
            ],
        },
        "training": {
            "attended_training": [
                "Did you attend any training organised by ASPSO?",
                "attended_training",
            ],
            "training_type": [
                "What type of training did you attend?",
                "training_type",
            ],
            "training_type_other": [
                "Other training type (specify)",
                "training_type_other",
            ],
            "training_duration": [
                "Approximately how long did the training last?",
                "training_duration",
            ],
            "selection_clarity": [
                "Before the training, were the selection criteria and process clearly explained to you?",
                "selection_clarity",
            ],
        },
        "content_recall": {
            "topics_covered": [
                "What topics were covered in your training? (Select all that apply)",
                "topics_covered",
            ],
            "topics_other": [
                "Other topic (specify)",
                "topics_other",
            ],
        },
        "inputs": {
            "received_items": [
                "Did you receive any items or materials after the training?",
                "received_items",
            ],
            "recv_tools": [
                "Tools or equipment related to training (received?)",
                "recv_tools",
            ],
            "recv_tools_qty": [
                "Quantity / details (tools/equipment)",
                "recv_tools_qty",
            ],
            "recv_raw": [
                "Raw materials / starter supplies (received?)",
                "recv_raw",
            ],
            "recv_raw_qty": [
                "Quantity / details (raw materials)",
                "recv_raw_qty",
            ],
            "recv_other_inputs": [
                "Other inputs (received?)",
                "recv_other_inputs",
            ],
            "recv_other_inputs_desc": [
                "Describe other inputs (quantity/details)",
                "recv_other_inputs_desc",
            ],
            "received_when": [
                "When did you receive these items?",
                "received_when",
            ],
            "training_met_needs": [
                "The training met my needs.",
                "training_met_needs",
            ],
            "safe_access_training": [
                "Do you feel safe and secure accessing the training?",
                "safe_access_training",
            ],
            "service_satisfaction": [
                "How satisfied are you with the services you received?",
                "service_satisfaction",
            ],
        },
        "utilisation": {
            "currently_using": [
                "Are you currently using what you learned or received?",
                "currently_using",
            ],
            "using_how": [
                "If yes/partly, how are you using it? (narrative)",
                "using_how",
            ],
            "not_using_reason": [
                "If no, what are the main reasons?",
                "not_using_reason",
            ],
            "not_using_reason_other": [
                "Other reason (specify)",
                "not_using_reason_other",
            ],
            "kit_quality_satisfaction": [
                "Were you satisfied with the quality of the input/kit?",
                "kit_quality_satisfaction",
            ],
        },
        "changes": {
            "training_helped": [
                "Has the training helped you in any way?",
                "training_helped",
            ],
            "helped_how": [
                "If yes, how? (Select all that apply)",
                "helped_how",
            ],
            "helped_how_other": [
                "Other (specify)",
                "helped_how_other",
            ],
            "challenges": [
                "What challenges have you faced in applying what you learned?",
                "challenges",
            ],
        },
        "accountability": {
            "informed_complaint": [
                "Were you informed about how to raise a concern or complaint related to this project?",
                "informed_complaint",
            ],
            "know_contact": [
                "Do you know whom to contact if you have a concern?",
                "know_contact",
            ],
        },
        "closing": {
            "anything_else": [
                "Is there anything else you would like to share about your experience with this project?",
                "anything_else",
            ],
        },
    },
    org_dashboard_tab_labels={
        "general": "General",
        "sample_info": "Sample Information",
        "consent_grp": "Consent & Introduction",
        "resp_details": "Respondent details",
        "training": "Participation in training",
        "content_recall": "Training content recall",
        "inputs": "Receipt of inputs / kits",
        "utilisation": "Use of skills and inputs (self-reported)",
        "changes": "Perceived changes and challenges",
        "accountability": "Accountability and safeguarding",
        "closing": "Closing",
    },
)
