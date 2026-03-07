"""GWO beneficiaries questionnaire schema and dashboard tab mapping."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="gwo_beneficiaries",
    title="GWO Beneficiaries",
    indicator_candidates={
        "consent": [
            "Does the person consent to participate?",
            "consent",
        ],
        "gender": [
            "Confirm gender",
            "gender",
        ],
        "training": [
            "Did you attend a training under this project?",
            "attended_training",
            "attend a training",
        ],
        "helpful": [
            "Was this helpful?",
            "market_helpful",
            "helpful",
        ],
        "complaint_awareness": [
            "Do you know whom to contact if you have a complaint?",
            "Were you informed how to raise concerns?",
            "know_contact",
            "informed_concerns",
        ],
        "date": [
            "date_time",
            "start",
            "submissiondate",
            "today",
        ],
    },
    org_dashboard_tabs={
        "sample_information": {
            "surveyor": ["Surveyor Name:", "Name_of_the_enumerator", "Surveyor Name"],
            "province": ["Province", "province"],
            "district": ["District", "district"],
        },
        "respondent_details": {
            "age_group": ["Age group", "age_group"],
            "gender": ["Confirm gender", "gender"],
            "marital": ["Confirm marital status", "marital"],
            "education": ["Level of education", "education"],
            "employment": ["Employment status", "employment"],
            "household_members": ["Number of household members", "hh_members"],
            "avg_income": ["Average income per month (local currency)", "avg_income"],
        },
        "participation_training": {
            "attended_training": [
                "Did you attend a training under this project?",
                "attended_training",
            ],
            "sessions_attended": [
                "How many sessions did you attend?",
                "sessions_attended",
            ],
            "training_duration": [
                "Approximately how long did the training last?",
                "training_duration",
            ],
        },
        "receipt_production_kits": {
            "received_kit": ["Did you receive a production kit?", "received_kit"],
            "kit_items": ["Kit items received", "kit_items"],
            "aluminum_cooking_pot": ["Aluminum cooking pot", "kit_aluminum_pot_yn"],
            "aluminum_cooking_pot_qty": [
                "kit_aluminum_pot_qty",
                "aluminum cooking pot quantity",
                "Quantity reported",
            ],
            "gas_stove": ["Gas stove", "kit_gas_stove_yn"],
            "gas_stove_qty": ["kit_gas_stove_qty", "gas stove quantity", "Quantity reported.1"],
            "gas_cylinder": ["Gas cylinder", "kit_gas_cylinder_yn"],
            "gas_cylinder_qty": ["kit_gas_cylinder_qty", "gas cylinder quantity", "Quantity reported.2"],
            "glass_jars": ["Glass jars", "kit_glass_jars_yn"],
            "glass_jars_qty": ["kit_glass_jars_qty", "glass jars quantity", "Quantity reported.3"],
            "knives": ["Knives", "kit_knives_yn"],
            "knives_qty": ["kit_knives_qty", "knives quantity", "Quantity reported.4"],
            "plastic_bucket": ["Plastic bucket", "kit_plastic_bucket_yn"],
            "plastic_bucket_qty": ["kit_plastic_bucket_qty", "plastic bucket quantity", "Quantity reported.5"],
            "hand_mixer": ["Hand mixer", "kit_hand_mixer_yn"],
            "hand_mixer_qty": ["kit_hand_mixer_qty", "hand mixer quantity", "Quantity reported.6"],
            "table": ["Table", "kit_table_yn"],
            "table_qty": ["kit_table_qty", "table quantity", "Quantity reported.7"],
        },
        "use_skills_inputs": {
            "producing_now": ["Are you currently producing paste or pickles?", "producing_now"],
            "produce_frequency": ["How often do you produce?", "produce_frequency"],
            "where_sell": ["Where do you sell? (Select all that apply)", "where_sell"],
            "where_sell_other": ["Specify other", "where_sell_other"],
            "hygiene_followed": ["Are hygiene practices being followed?", "hygiene_followed"],
            "hygiene_not_followed_reason": [
                "If no, why? (Select all that apply)",
                "hygiene_not_followed_reason",
            ],
            "hygiene_not_followed_other": ["Specify other", "hygiene_not_followed_other"],
        },
        "market_perceived_changes": {
            "info_markets": [
                "Were you given information about markets or shopkeepers?",
                "info_markets",
            ],
            "introduced_buyers": ["Did GWO introduce you to any buyers?", "introduced_buyers"],
            "market_helpful": ["Was this helpful?", "market_helpful"],
            "changes_helped": [
                "Has this activity helped you in any way? (Select all that apply)",
                "changes_helped",
            ],
        },
        "household_safeguarding": {
            "family_support": ["Did your family support your participation?", "family_support"],
            "concerns_family": [
                "Have there been any concerns from family or community? (Open-ended)",
                "concerns_family",
            ],
            "informed_concerns": ["Were you informed how to raise concerns?", "informed_concerns"],
            "know_contact": ["Do you know whom to contact if you have a complaint?", "know_contact"],
        },
    },
)
