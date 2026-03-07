"""Core constants for UN Women dashboard."""

import re

import pandas as pd

EXPECTED_TOTAL_ORGS = 16
TARGET_INTERVIEWS_PER_ORG = 20
CORRECTION_LOG_SHEET = "correction_log"
DEFAULT_SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1jA7HXcZ18CoBYnNGINeuR7XjtXoHwX5riraYGKuzpzM/edit?gid=36515757"
)
DEFAULT_XLS_FORMS_DIR = r"C:\Users\LENOVO\Documents\XLS_Forms"

ARABIC_SCRIPT_RE = re.compile(r"[\u0600-\u06FF]")

YES_VALUES = {
    "yes",
    "y",
    "true",
    "1",
    "بلی",
    "بلي",
    "هو",
    "آره",
    "ha",
}
PARTLY_VALUES = {
    "partly",
    "partially",
    "somewhat",
    "تاحدی",
    "قسمی",
    "نسبتا",
}
POSITIVE_VALUES = YES_VALUES | PARTLY_VALUES

PROTECTED_COLUMNS = {
    "_uuid",
    "_id",
    "start",
    "end",
    "today",
    "deviceid",
    "subscriberid",
    "simid",
    "phonenumber",
    "username",
    "meta/instanceid",
    "org_code",
    "sheet_name",
    "province",
    "ingo_partner",
    "interview_date",
}

ORG_ALIASES = {"ARWEO": "ARWE"}

ORG_SHEET_TABS = [
    "OHAD-Beneficiaries",
    "DHDO-Beneficiaries-Men",
    "ORSTW-Beneficiaries",
    "DHDO-Beneficiaries-Women",
    "ANBO-Beneficiaries",
    "ECOC-Beneficiaries",
    "ECOC-Beneficiaries-Male Guardians",
    "RPO-Beneficiaries",
    "GWO-Beneficiaries",
    "GSRO-Beneficiaries",
    "ASPSO-Beneficiaries",
    "ADSDO-Beneficiaries",
    "HHSO-Beneficiaries",
    "HOSAA-Beneficiaries",
    "PTCRO-Beneficiaries",
    "ARWE-Beneficiaries",
]

DEFAULT_INDICATOR_CANDIDATES = {
    "consent": [
        "consent",
        "consent_to_participate",
        "does_the_person_consent_to_participate",
    ],
    "gender": [
        "gender",
        "confirm_gender",
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
    ],
    "complaint_awareness": [
        "know_contact",
        "informed_complaints",
        "informed_concerns",
        "complaint",
        "concern",
    ],
    "date": [
        "date_time",
        "start",
        "submissiondate",
        "today",
        "interview_date",
    ],
}

ORG_MASTER_RECORDS = [
    {"org_code": "ANBO", "province": "Kunar", "ingo_partner": "DRC"},
    {"org_code": "OHAD", "province": "Kunar", "ingo_partner": "DRC"},
    {"org_code": "ARWE", "province": "Nangarhar", "ingo_partner": "DRC"},
    {"org_code": "DHDO", "province": "Nangarhar", "ingo_partner": "NRC"},
    {"org_code": "ECOC", "province": "Nangarhar", "ingo_partner": "NRC"},
    {"org_code": "ORSTW", "province": "Nangarhar", "ingo_partner": "NRC"},
    {"org_code": "RPO", "province": "Laghman", "ingo_partner": "NRC"},
    {"org_code": "ADSDO", "province": "Herat", "ingo_partner": "WVI"},
    {"org_code": "ASPSO", "province": "Herat", "ingo_partner": "WVI"},
    {"org_code": "HOSAA", "province": "Herat", "ingo_partner": "WVI"},
    {"org_code": "GSRO", "province": "Herat", "ingo_partner": "WVI"},
    {"org_code": "PTCRO", "province": "Herat", "ingo_partner": "DRC"},
    {"org_code": "GWO", "province": "Farah", "ingo_partner": "DRC"},
    {"org_code": "HHSO", "province": "Farah", "ingo_partner": "DRC"},
]


def org_master_frame() -> pd.DataFrame:
    """Return the baseline organization registry as a dataframe."""
    return pd.DataFrame(ORG_MASTER_RECORDS)
