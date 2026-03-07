# -*- coding: utf-8 -*-
"""Project configuration.
Edit this file if column names change in future survey exports.
"""

DATA_SHEET_NAME = 0  # first sheet

# Core identifier / location columns in your XLSForm export
COL_UUID = "_uuid"
COL_ID = "_id"  # fallback

COL_NGO = "NGO"  # will be created if missing
DEFAULT_NGO_NAME = "GWO"

COL_PROVINCE = "Province"
COL_DISTRICT = "District"
COL_LOCATION = "Village name:"
COL_ENUMERATOR = "Surveyor Name:"
COL_INTERVIEW_DATE = "date_time"  # your export has date_time

# Disaggregation columns
COL_GENDER = "Confirm gender"
COL_AGE_GROUP = "Age group"
COL_EDUCATION = "Level of education"
COL_EMPLOYMENT = "Employment status"

# Key outcome / monitoring columns (based on the questionnaire)
COL_CONSENT = "Does the person consent to participate?"
COL_RECORD_OK = "For note-taking/quality assurance, may we record the interview?"

COL_TRAINING_ATTEND = "Did you attend a training under this project?"
COL_TRAINING_SESSIONS = "How many sessions did you attend?"
COL_TRAINING_DURATION = "Approximately how long did the training last?"

COL_RECEIVED_KIT = "Did you receive a production kit?"
COL_KIT_RECEIPT_TIMING = "When did you receive the kit?"

COL_PRODUCING = "Are you currently producing paste or pickles?"
COL_SELL_WHERE = "Where do you sell? (Select all that apply)"

COL_MARKET_INFO = "Were you given information about markets or shopkeepers?"
COL_INTRO_BUYERS = "Did GWO introduce you to any buyers?"
COL_HELPFUL = "Was this helpful?"  # used as a practical satisfaction proxy

COL_ACTIVITY_HELPED = "Has this activity helped you in any way? (Select all that apply)"  # improvement proxy
COL_FAMILY_SUPPORT = "Did your family support your participation?"

COL_INFORMED_CONCERNS = "Were you informed how to raise concerns?"
COL_KNOW_COMPLAINT_CONTACT = "Do you know whom to contact if you have a complaint?"

# Define "positive" groupings (edit if you prefer stricter / looser definitions)
YES_VALUES = {"yes", "y", "true", "1"}
NO_VALUES = {"no", "n", "false", "0"}

POSITIVE_HELPFUL_VALUES = {"yes", "partly"}   # "Yes" + "Partly" counted positive
POSITIVE_PRODUCING_VALUES = {"yes", "partly"} # Yes + Partly

# Risk thresholds (traffic lights)
THRESH_STRONG = 0.80
THRESH_MODERATE = 0.60
