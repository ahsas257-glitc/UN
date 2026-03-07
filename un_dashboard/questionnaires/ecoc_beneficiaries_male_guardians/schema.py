"""Auto-generated questionnaire schema from XLSForm."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="ecoc_beneficiaries_male_guardians",
    title="ECOC Beneficiaries Male Guardians",
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
            "attended_sessions",
            "Did you attend any sessions organised by ECOC ?",
            "sessions_count",
            "How many sessions did you attend?",
            "session_location",
            "Where were the sessions conducted?",
            "session_location_other",
            "Other (specify)",
            "topics_discussed",
            "What topics were discussed during the sessions? (Tick all mentioned)",
            "sessions_useful",
            "Were the sessions useful to you?",
            "support_continued",
            "Do you support continued participation of women in such sessions?",
            "participation_challenges",
            "What challenges, if any, make participation difficult?",
            "participation_challenges_other",
            "anything_else",
            "Is there anything else you would like to share about the male guardian engagement sessions?",
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
            "Were you informed about how to raise concerns or complaints related to this project?",
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
            "relationship_to_beneficiary": [
                "Relationship to beneficiary",
                "relationship_to_beneficiary",
            ],
            "relationship_other": [
                "Other (specify)",
                "relationship_other",
            ],
        },
        "engage_grp": {
            "attended_sessions": [
                "Did you attend any sessions organised by ECOC ?",
                "attended_sessions",
            ],
            "sessions_count": [
                "How many sessions did you attend?",
                "sessions_count",
            ],
            "session_location": [
                "Where were the sessions conducted?",
                "session_location",
            ],
            "session_location_other": [
                "Other (specify)",
                "session_location_other",
            ],
        },
        "recall_grp": {
            "topics_discussed": [
                "What topics were discussed during the sessions? (Tick all mentioned)",
                "topics_discussed",
            ],
            "topics_discussed_other": [
                "Other (specify)",
                "topics_discussed_other",
            ],
        },
        "relevance_grp": {
            "sessions_useful": [
                "Were the sessions useful to you?",
                "sessions_useful",
            ],
            "useful_how": [
                "If yes or somewhat, how?",
                "useful_how",
            ],
            "useful_how_other": [
                "Other (specify)",
                "useful_how_other",
            ],
        },
        "changes_grp": {
            "noticed_changes": [
                "Have you noticed any changes in the wellbeing of the woman/girl who participated?",
                "noticed_changes",
            ],
            "change_types": [
                "If yes, what changes?",
                "change_types",
            ],
            "change_types_other": [
                "Other (specify)",
                "change_types_other",
            ],
        },
        "support_grp": {
            "support_continued": [
                "Do you support continued participation of women in such sessions?",
                "support_continued",
            ],
            "participation_challenges": [
                "What challenges, if any, make participation difficult?",
                "participation_challenges",
            ],
            "participation_challenges_other": [
                "Other (specify)",
                "participation_challenges_other",
            ],
        },
        "acc_grp": {
            "informed_complaints": [
                "Were you informed about how to raise concerns or complaints related to this project?",
                "informed_complaints",
            ],
            "know_contact": [
                "Do you know whom to contact if you have a concern?",
                "know_contact",
            ],
        },
        "closing_grp": {
            "anything_else": [
                "Is there anything else you would like to share about the male guardian engagement sessions?",
                "anything_else",
            ],
        },
    },
    org_dashboard_tab_labels={
        "general": "General",
        "sample_info": "Sample Information",
        "consent_grp": "Consent & Introduction",
        "resp_details": "Respondent details",
        "engage_grp": "Participation in Engagement Sessions",
        "recall_grp": "Session Content Recall",
        "relevance_grp": "Perceived Relevance",
        "changes_grp": "Observed Changes",
        "support_grp": "Support for Participation",
        "acc_grp": "Accountability and Feedback",
        "closing_grp": "Closing",
    },
)
