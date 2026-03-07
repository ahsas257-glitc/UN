"""Auto-generated questionnaire schema from XLSForm."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="orstw_beneficiaries",
    title="ORSTW Beneficiaries",
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
            "Did you attend any training organised by ORSTW?",
            "training_type",
            "What type of training did you attend?",
            "training_duration",
            "Approximately how long did the training last?",
            "selection_clarity",
            "Before the training, were the selection criteria and process clearly explained to you?",
            "training_meet_needs",
            "Did the training meet your needs?",
            "safe_access",
            "Did you feel safe and secure accessing the training?",
            "tailoring_topics",
            "If Tailoring training: What topics were covered? (Tick all mentioned)",
            "embroidery_topics",
            "If Embroidery/Handicrafts training: What topics were covered? (Tick all mentioned)",
            "received_items",
            "Did you receive any items or materials after the training?",
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
            "Were you satisfied with the quality of the input/kit?",
            "Has the training helped you in any way?",
        ],
        "complaint_awareness": [
            "know_contact",
            "informed_complaints",
            "informed_concerns",
            "complaint",
            "concern",
            "Were you informed about how to raise a concern or complaint related to this project?",
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
            "intervention": [
                "Intervention (select all that apply)",
                "intervention",
            ],
        },
        "training_grp": {
            "attended_training": [
                "Did you attend any training organised by ORSTW?",
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
                "Before the training, were the selection criteria and process clearly explained to you?",
                "selection_clarity",
            ],
            "training_meet_needs": [
                "Did the training meet your needs?",
                "training_meet_needs",
            ],
            "safe_access": [
                "Did you feel safe and secure accessing the training?",
                "safe_access",
            ],
            "service_satisfaction": [
                "How satisfied are you with the services you received?",
                "service_satisfaction",
            ],
        },
        "recall_grp": {
            "tailoring_topics": [
                "If Tailoring training: What topics were covered? (Tick all mentioned)",
                "tailoring_topics",
            ],
            "embroidery_topics": [
                "If Embroidery/Handicrafts training: What topics were covered? (Tick all mentioned)",
                "embroidery_topics",
            ],
        },
        "kit_grp": {
            "received_items": [
                "Did you receive any items or materials after the training?",
                "received_items",
            ],
            "sewing_machine_yn": [
                "Sewing machine",
                "sewing_machine_yn",
            ],
            "sewing_machine_qty": [
                "Quantity reported",
                "sewing_machine_qty",
            ],
            "tailoring_tools_yn": [
                "Tailoring tools (scissors, needles, etc.)",
                "tailoring_tools_yn",
            ],
            "tailoring_tools_qty": [
                "Quantity reported",
                "tailoring_tools_qty",
            ],
            "embroidery_tools_yn": [
                "Embroidery tools",
                "embroidery_tools_yn",
            ],
            "embroidery_tools_qty": [
                "Quantity reported",
                "embroidery_tools_qty",
            ],
            "raw_materials_yn": [
                "Raw materials (cloth, threads, etc.)",
                "raw_materials_yn",
            ],
            "raw_materials_qty": [
                "Quantity reported",
                "raw_materials_qty",
            ],
            "other_inputs_yn": [
                "Other inputs",
                "other_inputs_yn",
            ],
            "other_inputs_qty": [
                "Quantity reported",
                "other_inputs_qty",
            ],
            "other_inputs_specify": [
                "Other inputs (specify)",
                "other_inputs_specify",
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
            "using_now": [
                "Are you currently using what you learned or received?",
                "using_now",
            ],
            "using_how": [
                "If yes or partly, how are you using it? (Record narrative)",
                "using_how",
            ],
            "no_use_reason": [
                "If no, what are the main reasons?",
                "no_use_reason",
            ],
            "no_use_other": [
                "Other (specify)",
                "no_use_other",
            ],
        },
        "changes_grp": {
            "training_helped": [
                "Has the training helped you in any way?",
                "training_helped",
            ],
            "help_types": [
                "If yes, how?",
                "help_types",
            ],
            "help_other": [
                "Other (specify)",
                "help_other",
            ],
            "challenges_open": [
                "What challenges have you faced in applying what you learned? (Open-ended)",
                "challenges_open",
            ],
        },
        "acc_grp": {
            "informed_complaints": [
                "Were you informed about how to raise a concern or complaint related to this project?",
                "informed_complaints",
            ],
            "know_contact": [
                "Do you know whom to contact if you have a concern?",
                "know_contact",
            ],
        },
        "closing_grp": {
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
        "training_grp": "Participation in Training",
        "recall_grp": "Training Content Recall",
        "kit_grp": "Receipt of Inputs / Kits",
        "use_grp": "Use of Skills and Inputs (Self-Reported)",
        "changes_grp": "Perceived Changes and Challenges",
        "acc_grp": "Accountability and Safeguarding",
        "closing_grp": "Closing",
    },
)
