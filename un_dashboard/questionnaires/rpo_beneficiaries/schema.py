"""Auto-generated questionnaire schema from XLSForm."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="rpo_beneficiaries",
    title="RPO Beneficiaries",
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
            "attended_all_sessions",
            "Did you attend all planned training sessions?",
            "not_attend_reason",
            "If not, why? (Tick all mentioned)",
            "not_attend_other",
            "Other (specify)",
            "training_meet_needs",
            "Did the training meet your needs?",
            "safe_access",
            "Do you feel safe and secure accessing the training?",
            "num_trainings",
            "How many trainings did you participate in?",
            "dp_topics",
            "Which topics were covered in your training? (Tick all mentioned)",
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
        ],
        "complaint_awareness": [
            "know_contact",
            "informed_complaints",
            "informed_concerns",
            "complaint",
            "concern",
            "Were you informed about how to raise a concern or complaint?",
            "Do you know whom to contact if you have a concern related to this project?",
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
        "participation_grp": {
            "participated_any": [
                "Did you participate in any activities organised by RPO?",
                "participated_any",
            ],
            "selection_clarity": [
                "Was the selection criteria and process clearly explained to you?",
                "selection_clarity",
            ],
            "activities_participated": [
                "Which activities did you participate in? (Tick all mentioned)",
                "activities_participated",
            ],
            "activities_other": [
                "Other (specify)",
                "activities_other",
            ],
            "attended_all_sessions": [
                "Did you attend all planned training sessions?",
                "attended_all_sessions",
            ],
            "not_attend_reason": [
                "If not, why? (Tick all mentioned)",
                "not_attend_reason",
            ],
            "not_attend_other": [
                "Other (specify)",
                "not_attend_other",
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
        "dp_recall_grp": {
            "num_trainings": [
                "How many trainings did you participate in?",
                "num_trainings",
            ],
            "dp_topics": [
                "Which topics were covered in your training? (Tick all mentioned)",
                "dp_topics",
            ],
            "dp_most_useful": [
                "Which topics were most useful for you? Why?",
                "dp_most_useful",
            ],
        },
        "riskmap_grp": {
            "took_part_riskmap": [
                "Did you take part in risk mapping in your community?",
                "took_part_riskmap",
            ],
            "hazards_identified": [
                "If yes: What types of risks or hazards were identified?",
                "hazards_identified",
            ],
            "hazards_other": [
                "Other (specify)",
                "hazards_other",
            ],
            "women_involved_vulnerable": [
                "Were women involved in identifying vulnerable households and places?",
                "women_involved_vulnerable",
            ],
            "hazard_map_referenced": [
                "Do women in the community still talk about or refer to the hazard map?",
                "hazard_map_referenced",
            ],
        },
        "kit_grp": {
            "received_kit": [
                "Did you receive an emergency kit from this project?",
                "received_kit",
            ],
            "kit_items": [
                "Which items do you remember receiving? (Do not prompt unless needed)",
                "kit_items",
            ],
            "kit_items_other": [
                "Other (specify)",
                "kit_items_other",
            ],
            "kit_receive_when": [
                "When did you receive the kit?",
                "kit_receive_when",
            ],
            "kit_kept_ready": [
                "Are you currently keeping the kit prepared at home?",
                "kit_kept_ready",
            ],
            "kit_used": [
                "Have you used the kit?",
                "kit_used",
            ],
            "kit_quality_sat": [
                "Were you satisfied with the quality of the input/kit?",
                "kit_quality_sat",
            ],
        },
        "wlsg_grp": {
            "member_wlsg": [
                "Are you a member of a Women-Led Support Group?",
                "member_wlsg",
            ],
            "wlsg_role": [
                "If yes: What does the group do? How does it help you?",
                "wlsg_role",
            ],
            "women_maintain_maps": [
                "Are women involved in maintaining hazard maps or preparedness plans?",
                "women_maintain_maps",
            ],
            "women_share_warnings": [
                "Are women involved in sharing early warning messages?",
                "women_share_warnings",
            ],
        },
        "confidence_grp": {
            "more_prepared": [
                "Do you feel more prepared now to respond to disasters?",
                "more_prepared",
            ],
            "what_changed": [
                "What has changed for you since participating in this project?",
                "what_changed",
            ],
            "what_changed_other": [
                "Other (specify)",
                "what_changed_other",
            ],
            "shared_learning": [
                "Have you shared what you learned with others?",
                "shared_learning",
            ],
        },
        "acc_grp": {
            "informed_complaints": [
                "Were you informed about how to raise a concern or complaint?",
                "informed_complaints",
            ],
            "know_contact": [
                "Do you know whom to contact if you have a concern related to this project?",
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
        "participation_grp": "Participation in Project Activities",
        "dp_recall_grp": "Training Content Recall – Disaster Preparedness",
        "riskmap_grp": "Participatory Risk Mapping and Hazard Maps",
        "kit_grp": "Emergency Kits",
        "wlsg_grp": "Women-Led Support Groups",
        "confidence_grp": "Perceived Changes and Confidence",
        "acc_grp": "Accountability and Safeguarding",
        "closing_grp": "Closing",
    },
)
