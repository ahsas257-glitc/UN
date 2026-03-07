"""Auto-generated questionnaire schema from XLSForm."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="ecoc_beneficiaries",
    title="ECOC Beneficiaries",
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
            "participated",
            "Did you participate in psychosocial support sessions under this project?",
            "session_type",
            "What type of sessions did you attend?",
            "session_type_other",
            "Other (specify)",
            "session_frequency",
            "How often did sessions take place?",
            "sessions_count",
            "How many sessions did you attend?",
            "training_meet_needs",
            "The sessions met your needs.",
            "felt_safe",
            "Did you feel safe attending the sessions?",
            "private_space",
            "Were sessions conducted in a private and appropriate space?",
            "helped",
            "Has participation helped you in any way?",
            "family_support_change",
            "Has family support changed since your participation?",
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
            "helped",
            "Has participation helped you in any way?",
        ],
        "complaint_awareness": [
            "know_contact",
            "informed_complaints",
            "informed_concerns",
            "complaint",
            "concern",
            "Were you informed about how to raise concerns or complaints?",
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
            "res_num": [
                "Number of repondent:",
                "res_num",
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
            "support_type": [
                "Type of support received",
                "support_type",
            ],
        },
        "sessions_grp": {
            "heard_about": [
                "How did you hear about the psychosocial services being offered by ECOC?",
                "heard_about",
            ],
            "heard_about_other": [
                "Other (specify)",
                "heard_about_other",
            ],
            "participated": [
                "Did you participate in psychosocial support sessions under this project?",
                "participated",
            ],
            "session_type": [
                "What type of sessions did you attend?",
                "session_type",
            ],
            "session_type_other": [
                "Other (specify)",
                "session_type_other",
            ],
            "session_frequency": [
                "How often did sessions take place?",
                "session_frequency",
            ],
            "sessions_count": [
                "How many sessions did you attend?",
                "sessions_count",
            ],
            "training_meet_needs": [
                "The sessions met your needs.",
                "training_meet_needs",
            ],
            "service_satisfaction": [
                "How satisfied are you with the services you received?",
                "service_satisfaction",
            ],
        },
        "recall_grp": {
            "topics_discussed": [
                "Which topics were discussed? (Tick all mentioned)",
                "topics_discussed",
            ],
            "topics_discussed_other": [
                "Other (specify)",
                "topics_discussed_other",
            ],
        },
        "safety_grp": {
            "felt_safe": [
                "Did you feel safe attending the sessions?",
                "felt_safe",
            ],
            "private_space": [
                "Were sessions conducted in a private and appropriate space?",
                "private_space",
            ],
        },
        "changes_grp": {
            "helped": [
                "Has participation helped you in any way?",
                "helped",
            ],
            "help_how": [
                "If yes or somewhat, how?",
                "help_how",
            ],
            "help_other": [
                "Other (specify)",
                "help_other",
            ],
        },
        "family_grp": {
            "family_informed": [
                "Were your family members or mahram informed about the programme?",
                "family_informed",
            ],
            "family_support_change": [
                "Has family support changed since your participation?",
                "family_support_change",
            ],
        },
        "acc_grp": {
            "informed_complaints": [
                "Were you informed about how to raise concerns or complaints?",
                "informed_complaints",
            ],
            "know_contact": [
                "Do you know whom to contact if you have a concern?",
                "know_contact",
            ],
        },
        "peer_grp": {
            "peer_groups_formed": [
                "Were peer support groups formed?",
                "peer_groups_formed",
            ],
            "peer_groups_continuing": [
                "Are peer support groups continuing?",
                "peer_groups_continuing",
            ],
            "peer_support_how": [
                "If yes, how are these supporting women?",
                "peer_support_how",
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
        "sessions_grp": "Participation in Sessions",
        "recall_grp": "Session Content Recall",
        "safety_grp": "Safety and Comfort",
        "changes_grp": "Perceived Changes (Self-Reported)",
        "family_grp": "Family Support",
        "acc_grp": "Accountability and Safeguarding",
        "peer_grp": "Peer Support Groups",
        "closing_grp": "Closing",
    },
)
