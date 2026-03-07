"""Auto-generated questionnaire schema from XLSForm."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="hhso_beneficiaries",
    title="HHSO Beneficiaries",
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
            "attended_project",
            "Did you attend activities under this project?",
            "activities_attended",
            "Which activities did you attend? (Select all that apply)",
            "training_duration",
            "Approximately how long did the training last?",
            "barriers_sel",
            "Were there any challenges in attending training?",
        ],
        "helpful": [
            "helpful",
            "training_helped",
            "service_satisfaction",
            "kit_quality_sat",
            "market_helpful",
            "record_ok",
            "For note-taking/quality assurance, may we record the interview?",
            "project_helped",
            "Has the project helped you?",
            "helped_how_sel",
            "If yes, how? (Select all that apply)",
        ],
        "complaint_awareness": [
            "know_contact",
            "informed_complaints",
            "informed_concerns",
            "complaint",
            "concern",
            "informed_complaint",
            "Were you informed about how to raise a concern or complaint?",
            "know_report",
            "Do you know where to report concerns?",
        ],
        "date": [
            "date_time",
            "start",
            "submissiondate",
            "today",
            "interview_date",
            "received_kit",
            "Did you receive a tailoring startup kit?",
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
            "attended_project": [
                "Did you attend activities under this project?",
                "attended_project",
            ],
            "activities_attended": [
                "Which activities did you attend? (Select all that apply)",
                "activities_attended",
            ],
            "training_duration": [
                "Approximately how long did the training last?",
                "training_duration",
            ],
        },
        "recall": {
            "tailoring_topics_sel": [
                "Tailoring topics remembered",
                "tailoring_topics_sel",
            ],
            "literacy_topics_sel": [
                "Literacy topics remembered",
                "literacy_topics_sel",
            ],
            "pss_topics_sel": [
                "Psychosocial support topics remembered",
                "pss_topics_sel",
            ],
        },
        "startup_kit": {
            "received_kit": [
                "Did you receive a tailoring startup kit?",
                "received_kit",
            ],
            "kit_sewing_machine": [
                "Sewing machine",
                "kit_sewing_machine",
            ],
            "kit_scissors": [
                "Scissors",
                "kit_scissors",
            ],
            "kit_needles_thread": [
                "Needles / Thread",
                "kit_needles_thread",
            ],
            "kit_fabric_materials": [
                "Fabric / Materials",
                "kit_fabric_materials",
            ],
            "kit_other_flag": [
                "Other item received?",
                "kit_other_flag",
            ],
            "kit_other_text": [
                "Specify other item",
                "kit_other_text",
            ],
            "kit_timing": [
                "When did you receive the kit?",
                "kit_timing",
            ],
        },
        "use_skills": {
            "use_machine": [
                "Are you currently using the sewing machine?",
                "use_machine",
            ],
            "use_how_sel": [
                "If yes or partly, how? (Select all)",
                "use_how_sel",
            ],
            "followup_visits": [
                "Have HHSO staff conducted follow-up visits?",
                "followup_visits",
            ],
            "followup_support": [
                "If yes, what kind of support was provided? (Open-ended)",
                "followup_support",
            ],
        },
        "perceived_changes": {
            "project_helped": [
                "Has the project helped you?",
                "project_helped",
            ],
            "helped_how_sel": [
                "If yes, how? (Select all that apply)",
                "helped_how_sel",
            ],
        },
        "barriers": {
            "barriers_sel": [
                "Were there any challenges in attending training?",
                "barriers_sel",
            ],
            "barriers_other": [
                "Specify other challenge",
                "barriers_other",
            ],
        },
        "accountability": {
            "informed_complaint": [
                "Were you informed about how to raise a concern or complaint?",
                "informed_complaint",
            ],
            "know_report": [
                "Do you know where to report concerns?",
                "know_report",
            ],
        },
        "closing": {
            "closing_anything": [
                "Is there anything else you would like to share?",
                "closing_anything",
            ],
        },
    },
    org_dashboard_tab_labels={
        "general": "General",
        "sample_info": "Sample Information",
        "consent_grp": "Consent & Introduction",
        "resp_details": "Respondent details",
        "participation": "Participation in training",
        "recall": "Training content recall",
        "startup_kit": "Receipt of startup kit",
        "use_skills": "Use of skills and home-based business",
        "perceived_changes": "Perceived changes",
        "barriers": "Participation barriers",
        "accountability": "Accountability and safeguarding",
        "closing": "Closing",
    },
)
