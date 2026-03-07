"""Auto-generated questionnaire schema from XLSForm."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="adsdo_beneficiaries",
    title="ADSDO Beneficiaries",
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
            "attend_training",
            "Did you attend a training organised by ADSDO?",
            "training_type",
            "What type of training did you attend?",
            "training_duration",
            "How long did the training last?",
            "criteria_clear",
            "Before the training, were the selection criteria and process clearly explained to you?",
            "meet_needs",
            "Did the training meet your needs?",
            "safe_access",
            "Do you feel safe and secure accessing the training?",
            "received_kit",
            "Did you receive a toolkit or materials after the training?",
        ],
        "helpful": [
            "helpful",
            "training_helped",
            "service_satisfaction",
            "kit_quality_sat",
            "market_helpful",
            "record_ok",
            "For note-taking/quality assurance, may we record the interview?",
            "kit_quality",
            "Were you satisfied with the quality of the input/kit?",
            "helped",
            "Has this support helped you in any way?",
        ],
        "complaint_awareness": [
            "know_contact",
            "informed_complaints",
            "informed_concerns",
            "complaint",
            "concern",
            "informed_complaint",
            "Were you informed about how to raise concerns or complaints?",
            "Do you know whom to contact if you have a concern?",
        ],
        "date": [
            "date_time",
            "start",
            "submissiondate",
            "today",
            "interview_date",
            "receive_time",
            "When did you receive the toolkit?",
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
        "training": {
            "attend_training": [
                "Did you attend a training organised by ADSDO?",
                "attend_training",
            ],
            "training_type": [
                "What type of training did you attend?",
                "training_type",
            ],
            "training_duration": [
                "How long did the training last?",
                "training_duration",
            ],
            "criteria_clear": [
                "Before the training, were the selection criteria and process clearly explained to you?",
                "criteria_clear",
            ],
            "meet_needs": [
                "Did the training meet your needs?",
                "meet_needs",
            ],
            "safe_access": [
                "Do you feel safe and secure accessing the training?",
                "safe_access",
            ],
            "service_sat": [
                "How satisfied are you with the services you received?",
                "service_sat",
            ],
        },
        "recall": {
            "topics": [
                "Which topics do you remember being covered?",
                "topics",
            ],
            "topics_other": [
                "Specify other topic",
                "topics_other",
            ],
        },
        "toolkit": {
            "received_kit": [
                "Did you receive a toolkit or materials after the training?",
                "received_kit",
            ],
            "kit_type": [
                "If yes, what type of toolkit did you receive?",
                "kit_type",
            ],
            "kit_type_other": [
                "Specify other toolkit type",
                "kit_type_other",
            ],
            "tools_suitable": [
                "Were the tools suitable for your skills?",
                "tools_suitable",
            ],
            "receive_time": [
                "When did you receive the toolkit?",
                "receive_time",
            ],
            "kit_quality": [
                "Were you satisfied with the quality of the input/kit?",
                "kit_quality",
            ],
        },
        "use": {
            "using_now": [
                "Are you currently using the skills or tools provided?",
                "using_now",
            ],
            "use_how": [
                "If yes/partly, how? (open-ended)",
                "use_how",
            ],
            "no_use_reason": [
                "If no, why not?",
                "no_use_reason",
            ],
            "no_use_other": [
                "Specify other reason",
                "no_use_other",
            ],
        },
        "changes": {
            "helped": [
                "Has this support helped you in any way?",
                "helped",
            ],
            "benefits": [
                "If yes, how? (select all that apply)",
                "benefits",
            ],
            "benefits_other": [
                "Specify other benefit",
                "benefits_other",
            ],
        },
        "acct": {
            "informed_complaint": [
                "Were you informed about how to raise concerns or complaints?",
                "informed_complaint",
            ],
            "know_contact": [
                "Do you know whom to contact if you have a concern?",
                "know_contact",
            ],
        },
        "closing": {
            "closing_comments": [
                "Is there anything else you would like to share?",
                "closing_comments",
            ],
        },
    },
    org_dashboard_tab_labels={
        "general": "General",
        "sample_info": "Sample Information",
        "consent_grp": "Consent & Introduction",
        "resp_details": "Respondent details",
        "training": "Participation in training",
        "recall": "Training content recall",
        "toolkit": "Receipt of toolkit / inputs",
        "use": "Use of skills and inputs",
        "changes": "Perceived changes",
        "acct": "Accountability and safeguarding",
        "closing": "Closing",
    },
)
