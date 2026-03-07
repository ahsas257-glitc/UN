"""Auto-generated questionnaire schema from XLSForm."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="ptcro_beneficiaries",
    title="PTCRO Beneficiaries",
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
            "attend_sessions",
            "Did you attend hygiene awareness sessions?",
            "informed",
            "How were you informed about the session?",
            "separate_sessions",
            "Were sessions conducted separately for men and women?",
            "changed_understanding",
            "Did the session change your understanding of hygiene?",
            "training_received",
            "What training did you receive?",
            "sessions_facilitated",
            "How many sessions have you facilitated?",
            "diff_response",
            "Do men and women respond differently during sessions? Please explain.",
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
            "informed_feedback",
            "Were you informed about how to provide feedback or complaints?",
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
            "respondent_category": [
                "Respondent category",
                "respondent_category",
            ],
            "participant_type": [
                "Are you:",
                "participant_type",
            ],
        },
        "sec2": {
            "attend_sessions": [
                "Did you attend hygiene awareness sessions?",
                "attend_sessions",
            ],
            "informed": [
                "How were you informed about the session?",
                "informed",
            ],
            "informed_other": [
                "Specify other",
                "informed_other",
            ],
            "separate_sessions": [
                "Were sessions conducted separately for men and women?",
                "separate_sessions",
            ],
            "participate_fully": [
                "Were you able to participate fully?",
                "participate_fully",
            ],
        },
        "sec3": {
            "messages_remember": [
                "What hygiene messages do you remember? Probe:\n•        When should hands be washed?\n•        How should water be stored safely?\n•        What was discussed about menstrual hygiene?\n•        What was discussed about children’s hygiene?\n•        What was discussed about waste disposal?",
                "messages_remember",
            ],
            "changed_understanding": [
                "Did the session change your understanding of hygiene?",
                "changed_understanding",
            ],
            "changed_how": [
                "If yes, how?",
                "changed_how",
            ],
        },
        "sec4": {
            "received_kit": [
                "Did your household receive a hygiene kit?",
                "received_kit",
            ],
            "benef_selected": [
                "How were beneficiaries selected?",
                "benef_selected",
            ],
            "kit_items_rec": [
                "What items were included in the kit? (Tick all)",
                "kit_items_rec",
            ],
            "kit_items_other": [
                "Specify other item",
                "kit_items_other",
            ],
            "items_used": [
                "Are the items still being used?",
                "items_used",
            ],
        },
        "sec5": {
            "practices_changed": [
                "What hygiene practices have changed in your household?",
                "practices_changed",
            ],
            "change_desc": [
                "If yes/partly, please describe.",
                "change_desc",
            ],
            "prevent_full": [
                "What prevents full adoption of hygiene practices?",
                "prevent_full",
            ],
        },
        "sec6": {
            "informed_feedback": [
                "Were you informed about how to provide feedback or complaints?",
                "informed_feedback",
            ],
            "mechs_mentioned": [
                "What mechanisms were mentioned? (Select all)",
                "mechs_mentioned",
            ],
            "mechs_other": [
                "Specify other mechanism",
                "mechs_other",
            ],
            "trust_mechs": [
                "Do you trust these mechanisms?",
                "trust_mechs",
            ],
        },
        "sec7": {
            "how_selected": [
                "How were you selected?",
                "how_selected",
            ],
            "training_received": [
                "What training did you receive?",
                "training_received",
            ],
            "sessions_facilitated": [
                "How many sessions have you facilitated?",
                "sessions_facilitated",
            ],
            "diff_response": [
                "Do men and women respond differently during sessions? Please explain.",
                "diff_response",
            ],
            "challenges_mobilize": [
                "What challenges do you face in mobilizing your community?",
                "challenges_mobilize",
            ],
            "supervision": [
                "Do you receive supervision or mentoring?",
                "supervision",
            ],
        },
        "consent_ok": {
            "closing": [
                "Any additional comments?",
                "closing",
            ],
        },
    },
    org_dashboard_tab_labels={
        "general": "General",
        "sample_info": "Sample Information",
        "consent_grp": "Consent & Introduction",
        "resp_details": "Respondent details",
        "sec2": "Section 2: Participation in Community Sessions",
        "sec3": "Section 3: Knowledge and Message Recall",
        "sec4": "Section 4: Hygiene Kit Verification (If Applicable)",
        "sec5": "Section 5: Behaviour Change",
        "sec6": "Section 6: Accountability and Safeguarding",
        "sec7": "Section 7: Hygiene Champion Section (Only for Champions)",
        "consent_ok": "Quesitons",
    },
)
