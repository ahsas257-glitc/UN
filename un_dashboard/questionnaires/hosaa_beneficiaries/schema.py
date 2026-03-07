"""Auto-generated questionnaire schema from XLSForm."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="hosaa_beneficiaries",
    title="HOSAA Beneficiaries",
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
            "attended",
            "Did you attend any awareness sessions organised by HOSAA?",
            "session_count",
            "Approximately how many sessions did you attend?",
            "session_location",
            "Where were the sessions conducted?",
            "session_location_other",
            "Specify other location",
            "informed_how",
            "How were you informed about the session?",
            "felt_safe",
            "Did you feel safe while attending the sessions?",
            "topics_discussed",
            "What topics were discussed during the sessions you attended?",
            "change_water",
            "Since attending, have you made any changes in how you store or handle drinking water at home?",
            "change_mhm",
            "Since attending, have you changed anything related to menstrual hygiene practices?",
            "benefited",
            "Do you feel the awareness sessions have benefited you?",
            "important_others",
            "Do you believe these sessions are important for other women and girls? Why or why not?",
            "informed_complaint",
            "During the session, were you informed about how to raise a concern or complaint?",
            "closing",
            "Is there anything else you would like to share about your experience with these awareness sessions?",
        ],
        "helpful": [
            "helpful",
            "training_helped",
            "service_satisfaction",
            "kit_quality_sat",
            "market_helpful",
            "record_ok",
            "For note-taking/quality assurance, may we record the interview?",
        ],
        "complaint_awareness": [
            "know_contact",
            "informed_complaints",
            "informed_concerns",
            "complaint",
            "concern",
            "informed_complaint",
            "During the session, were you informed about how to raise a concern or complaint?",
            "Do you know whom to contact if you have a complaint or suggestion?",
            "safe_raise",
            "Do you feel safe raising concerns if needed?",
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
        "participation": {
            "attended": [
                "Did you attend any awareness sessions organised by HOSAA?",
                "attended",
            ],
            "session_count": [
                "Approximately how many sessions did you attend?",
                "session_count",
            ],
            "session_location": [
                "Where were the sessions conducted?",
                "session_location",
            ],
            "session_location_other": [
                "Specify other location",
                "session_location_other",
            ],
            "informed_how": [
                "How were you informed about the session?",
                "informed_how",
            ],
            "convenient": [
                "Were the timing and location convenient for you?",
                "convenient",
            ],
            "convenient_no_reason": [
                "If no, please explain why.",
                "convenient_no_reason",
            ],
            "felt_safe": [
                "Did you feel safe while attending the sessions?",
                "felt_safe",
            ],
            "felt_safe_no_reason": [
                "If no, please explain why.",
                "felt_safe_no_reason",
            ],
        },
        "recall": {
            "topics_discussed": [
                "What topics were discussed during the sessions you attended?",
                "topics_discussed",
            ],
            "topics_other": [
                "Specify other topic",
                "topics_other",
            ],
            "learned_water": [
                "Can you describe what you learned about keeping drinking water safe at home?",
                "learned_water",
            ],
            "learned_mhm": [
                "Can you explain what was discussed regarding menstrual hygiene management?",
                "learned_mhm",
            ],
            "easy_understand": [
                "Were the topics explained in a way that was easy for you to understand?",
                "easy_understand",
            ],
            "difficult_why": [
                "If no, what made it difficult?",
                "difficult_why",
            ],
        },
        "application": {
            "change_water": [
                "Since attending, have you made any changes in how you store or handle drinking water at home?",
                "change_water",
            ],
            "change_water_desc": [
                "If yes, please describe the changes.",
                "change_water_desc",
            ],
            "change_mhm": [
                "Since attending, have you changed anything related to menstrual hygiene practices?",
                "change_mhm",
            ],
            "change_mhm_desc": [
                "If yes, please explain what has changed.",
                "change_mhm_desc",
            ],
            "shared_info": [
                "Have you shared the information with other women or girls in your household or community?",
                "shared_info",
            ],
            "shared_with": [
                "If yes, with whom and what information did you share?",
                "shared_with",
            ],
        },
        "barriers": {
            "barrier_water": [
                "What challenges prevent you from applying the safe water practices?",
                "barrier_water",
            ],
            "barrier_mhm": [
                "What challenges prevent you from practicing menstrual hygiene as discussed?",
                "barrier_mhm",
            ],
            "barrier_types": [
                "Are there financial, cultural, or household barriers that make it difficult to follow these practices?",
                "barrier_types",
            ],
        },
        "benefits_sec": {
            "benefited": [
                "Do you feel the awareness sessions have benefited you?",
                "benefited",
            ],
            "benefit_ways": [
                "If yes, in what ways have they benefited you?",
                "benefit_ways",
            ],
            "benefit_other": [
                "Specify other benefit",
                "benefit_other",
            ],
            "important_others": [
                "Do you believe these sessions are important for other women and girls? Why or why not?",
                "important_others",
            ],
        },
        "accountability": {
            "informed_complaint": [
                "During the session, were you informed about how to raise a concern or complaint?",
                "informed_complaint",
            ],
            "know_contact": [
                "Do you know whom to contact if you have a complaint or suggestion?",
                "know_contact",
            ],
            "safe_raise": [
                "Do you feel safe raising concerns if needed?",
                "safe_raise",
            ],
            "safe_raise_no_reason": [
                "If no, please explain why.",
                "safe_raise_no_reason",
            ],
        },
        "consent_ok": {
            "closing": [
                "Is there anything else you would like to share about your experience with these awareness sessions?",
                "closing",
            ],
        },
    },
    org_dashboard_tab_labels={
        "general": "General",
        "sample_info": "Sample Information",
        "consent_grp": "Consent & Introduction",
        "resp_details": "Respondent details",
        "participation": "Participation in awareness sessions",
        "recall": "Recall of session content",
        "application": "Understanding and application of knowledge",
        "barriers": "Barriers and challenges",
        "benefits_sec": "Perceived changes and benefits",
        "accountability": "Accountability and safeguarding",
        "consent_ok": "Quesitons",
    },
)
