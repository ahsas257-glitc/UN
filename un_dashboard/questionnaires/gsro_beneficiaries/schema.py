"""Auto-generated questionnaire schema from XLSForm."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="gsro_beneficiaries",
    title="GSRO Beneficiaries",
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
        ],
        "helpful": [
            "helpful",
            "training_helped",
            "service_satisfaction",
            "kit_quality_sat",
            "market_helpful",
            "record_ok",
            "For note-taking/quality assurance, may we record the interview?",
            "referral_details",
            "If yes: what kind of support and was it helpful?",
        ],
        "complaint_awareness": [
            "know_contact",
            "informed_complaints",
            "informed_concerns",
            "complaint",
            "concern",
            "informed_feedback",
            "Were you informed how to give feedback or make a complaint?",
        ],
        "date": [
            "date_time",
            "start",
            "submissiondate",
            "today",
            "interview_date",
            "time_received",
            "When did you receive the service(s)?",
            "tazkira_received_date",
            "If received: when did you receive it?",
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
            "pd_area": [
                "Area (PD)",
                "pd_area",
            ],
            "pd_area_other": [
                "Specify other area",
                "pd_area_other",
            ],
            "main_pathway": [
                "Interview type (main pathway)",
                "main_pathway",
            ],
        },
        "service_pathway": {
            "heard_about": [
                "How did you first hear about GSRO’s support for Tazkira/civil documentation?",
                "heard_about",
            ],
            "heard_about_other": [
                "Specify other",
                "heard_about_other",
            ],
            "services_used": [
                "Which services did you use? (Select all)",
                "services_used",
            ],
            "time_received": [
                "When did you receive the service(s)?",
                "time_received",
            ],
        },
        "awareness_recall": {
            "why_tazkira_important": [
                "What information was shared about why a Tazkira is important?",
                "why_tazkira_important",
            ],
            "steps_explained": [
                "What steps/process for obtaining a Tazkira were explained?",
                "steps_explained",
            ],
            "awareness_probe": [
                "Probe list (tick if mentioned)",
                "awareness_probe",
            ],
            "awareness_probe_other": [
                "Specify other",
                "awareness_probe_other",
            ],
        },
        "legal_support": {
            "legal_help": [
                "What kind of legal help did you receive? (Select all)",
                "legal_help",
            ],
            "legal_help_other": [
                "Specify other",
                "legal_help_other",
            ],
            "support_where": [
                "Where did you receive most of the support?",
                "support_where",
            ],
            "lang_understood": [
                "Was the service provided in a language you understood?",
                "lang_understood",
            ],
            "lang_difficult": [
                "If no, what was difficult?",
                "lang_difficult",
            ],
            "barriers_yes": [
                "Did you face any barriers to accessing services?",
                "barriers_yes",
            ],
            "barriers": [
                "Which barriers? (Select all)",
                "barriers",
            ],
            "barriers_other": [
                "Specify other",
                "barriers_other",
            ],
            "gsro_reduce_barriers": [
                "How (if at all) did GSRO help reduce these barriers?",
                "gsro_reduce_barriers",
            ],
            "felt_safe_access": [
                "Did you feel safe while accessing the services?",
                "felt_safe_access",
            ],
            "safe_reasons": [
                "If no, please give reasons.",
                "safe_reasons",
            ],
        },
        "outcome": {
            "tazkira_status": [
                "What is the current status of your Tazkira application?",
                "tazkira_status",
            ],
            "tazkira_received_date": [
                "If received: when did you receive it?",
                "tazkira_received_date",
            ],
            "follow_up_after": [
                "Did GSRO follow up after issuance?",
                "follow_up_after",
            ],
            "change_after": [
                "What changed for you after receiving it?",
                "change_after",
            ],
            "why_not_received": [
                "If not received: main reason(s)",
                "why_not_received",
            ],
            "why_not_received_other": [
                "Specify other",
                "why_not_received_other",
            ],
        },
        "referral": {
            "referred": [
                "Were you referred to another organisation/service for additional support?",
                "referred",
            ],
            "referral_details": [
                "If yes: what kind of support and was it helpful?",
                "referral_details",
            ],
        },
        "accountability": {
            "treated_respectfully": [
                "Did you feel you were treated respectfully and fairly?",
                "treated_respectfully",
            ],
            "treated_why": [
                "Why?",
                "treated_why",
            ],
            "informed_feedback": [
                "Were you informed how to give feedback or make a complaint?",
                "informed_feedback",
            ],
            "feedback_channel": [
                "If yes: which channel(s)?",
                "feedback_channel",
            ],
            "feedback_channel_other": [
                "Specify other",
                "feedback_channel_other",
            ],
            "safe_sharing": [
                "Did you feel safe using the service / providing information?",
                "safe_sharing",
            ],
            "safe_sharing_why": [
                "If no: why?",
                "safe_sharing_why",
            ],
        },
        "consent_ok": {
            "closing": [
                "Closing: Anything else you want to share about GSRO’s support?",
                "closing",
            ],
        },
    },
    org_dashboard_tab_labels={
        "general": "General",
        "sample_info": "Sample Information",
        "consent_grp": "Consent & Introduction",
        "resp_details": "Respondent details",
        "service_pathway": "Access and participation (service pathway)",
        "awareness_recall": "Awareness session recall (if applicable)",
        "legal_support": "Legal counselling and case support (if applicable)",
        "outcome": "Progress toward Tazkira (outcome verification)",
        "referral": "Referral mechanism (if applicable)",
        "accountability": "Accountability, safety and respect",
        "consent_ok": "Quesitons",
    },
)
