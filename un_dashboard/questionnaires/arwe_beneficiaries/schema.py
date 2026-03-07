"""Auto-generated questionnaire schema from XLSForm."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="arwe_beneficiaries",
    title="ARWE Beneficiaries",
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
            "Did you attend the training organised by ARWEO?",
            "training_type",
            "What type of training did you attend?",
            "training_duration",
            "Approximately how long did the training last?",
            "selection_clarity",
            "Before the training, was the selection criteria and process clearly explained to you?",
            "training_meet_needs",
            "Did the training meet your needs?",
            "safe_access",
            "Do you feel safe and secure accessing the training?",
            "topics_discussed",
            "What topics were covered in the training? (Tick all mentioned)",
            "received_items",
            "Did you receive any items or materials after the training?",
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
            "group_helped",
            "Has being part of this group helped you?",
            "group_helped_how",
            "If yes, how?",
        ],
        "complaint_awareness": [
            "know_contact",
            "informed_complaints",
            "informed_concerns",
            "complaint",
            "concern",
            "Were you informed about how to raise a concern or complaint?",
            "Do you know whom to contact if you have a concern?",
        ],
        "date": [
            "date_time",
            "start",
            "submissiondate",
            "today",
            "interview_date",
            "vet_affordable",
            "If yes, were they affordable and timely?",
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
        },
        "training_part": {
            "attended_training": [
                "Did you attend the training organised by ARWEO?",
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
                "Before the training, was the selection criteria and process clearly explained to you?",
                "selection_clarity",
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
        "recall_grp": {
            "topics_discussed": [
                "What topics were covered in the training? (Tick all mentioned)",
                "topics_discussed",
            ],
            "topics_discussed_other": [
                "Others (specify)",
                "topics_discussed_other",
            ],
        },
        "inputs_grp": {
            "received_items": [
                "Did you receive any items or materials after the training?",
                "received_items",
            ],
            "recv_hens": [
                "Hens",
                "recv_hens",
            ],
            "hens_qty": [
                "Quantity (if known)",
                "hens_qty",
            ],
            "recv_rooster": [
                "Rooster",
                "recv_rooster",
            ],
            "rooster_qty": [
                "Quantity (if known)",
                "rooster_qty",
            ],
            "recv_feed": [
                "Poultry feed",
                "recv_feed",
            ],
            "feed_details": [
                "Details / amount (as known)",
                "feed_details",
            ],
            "recv_coop_materials": [
                "Coop/shelter materials",
                "recv_coop_materials",
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
            "keeping_poultry": [
                "Are you currently keeping poultry using what you learned?",
                "keeping_poultry",
            ],
            "keeping_poultry_how": [
                "If yes or partly, how are you using it? (Record narrative)",
                "keeping_poultry_how",
            ],
            "no_keep_reason": [
                "If no, what are the main reasons?",
                "no_keep_reason",
            ],
            "no_keep_other": [
                "Other (specify)",
                "no_keep_other",
            ],
        },
        "peer_grp": {
            "joined_group": [
                "Have you joined or interacted with other women beneficiaries as a group?",
                "joined_group",
            ],
            "group_frequency": [
                "If yes: How often do you meet or communicate?",
                "group_frequency",
            ],
            "group_discuss": [
                "If yes: What do you discuss?",
                "group_discuss",
            ],
            "group_discuss_other": [
                "Other (specify)",
                "group_discuss_other",
            ],
            "group_helped": [
                "Has being part of this group helped you?",
                "group_helped",
            ],
            "group_helped_how": [
                "If yes, how?",
                "group_helped_how",
            ],
        },
        "market_grp": {
            "sold_products": [
                "Have you sold eggs or poultry products?",
                "sold_products",
            ],
            "sell_where": [
                "If yes: Where did you sell?",
                "sell_where",
            ],
            "sell_where_other": [
                "Other (specify)",
                "sell_where_other",
            ],
            "market_info_given": [
                "Were you given information about markets or buyers?",
                "market_info_given",
            ],
            "market_info_useful": [
                "Was this information useful?",
                "market_info_useful",
            ],
        },
        "vet_grp": {
            "know_vet": [
                "Do you know where to access poultry vaccination or veterinary services?",
                "know_vet",
            ],
            "used_vet": [
                "Have you used these services?",
                "used_vet",
            ],
            "vet_affordable": [
                "If yes, were they affordable and timely?",
                "vet_affordable",
            ],
        },
        "nut_grp": {
            "nutrition_changed": [
                "Has your household food or nutrition changed since the project?",
                "nutrition_changed",
            ],
            "nutrition_changes": [
                "If yes: What changed?",
                "nutrition_changes",
            ],
            "nutrition_changes_other": [
                "Other (specify)",
                "nutrition_changes_other",
            ],
        },
        "acc_grp": {
            "informed_complaints": [
                "Were you informed about how to raise a concern or complaint?",
                "informed_complaints",
            ],
            "know_contact": [
                "Do you know whom to contact if you have a concern?",
                "know_contact",
            ],
        },
        "closing_grp": {
            "anything_else": [
                "Is there anything else you would like to share about this project?",
                "anything_else",
            ],
        },
    },
    org_dashboard_tab_labels={
        "general": "General",
        "sample_info": "Sample Information",
        "consent_grp": "Consent & Introduction",
        "resp_details": "Respondent details",
        "training_part": "Participation in Training",
        "recall_grp": "Training Content Recall",
        "inputs_grp": "Receipt of Inputs",
        "use_grp": "Use of Skills and Inputs",
        "peer_grp": "Peer Support Groups / Cooperatives",
        "market_grp": "Market Linkages",
        "vet_grp": "Veterinary & Poultry Health Services",
        "nut_grp": "Nutrition and Household Use",
        "acc_grp": "Accountability and Safeguarding",
        "closing_grp": "Closing",
    },
)
