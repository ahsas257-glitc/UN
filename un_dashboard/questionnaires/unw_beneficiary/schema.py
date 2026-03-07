"""UN Women beneficiary monitoring questionnaire schema."""

from __future__ import annotations

from un_dashboard.questionnaires.base import QuestionnaireSchema

SCHEMA = QuestionnaireSchema(
    key="unw_beneficiary",
    title="UNW Beneficiary Monitoring",
    indicator_candidates={
        "consent": [
            "Does the person consent to participate?",
            "consent to participate",
        ],
        "gender": [
            "Confirm gender",
            "gender",
        ],
        "training": [
            "Did you attend a training under this project?",
            "attend a training",
        ],
        "helpful": [
            "Was this helpful?",
            "helpful",
        ],
        "complaint_awareness": [
            "Do you know whom to contact if you have a complaint?",
            "Were you informed how to raise concerns?",
        ],
        "date": [
            "date_time",
            "start",
            "submissiondate",
            "today",
        ],
    },
)
