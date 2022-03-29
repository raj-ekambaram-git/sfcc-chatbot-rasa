# MY CASE
AUTHORIZATION = 'authorization'

# COMMON
ACTION = 'action'
EVENT = 'event'
METADATA = 'metadata'
USER_EVENT = 'user'
USER_ID = 'user_id'
USER_NAME = 'user_name'
URL = 'url'
DATA = 'data'
FORM = 'form'
TEXT = 'text'
ID = 'id'
NAME = 'name'

# DB COLLECTIONS/KEYS

CASE_NUMBER = 'case_number'
LOCATION_CODE = 'location_code'
NEXT_HEARING_DATE = 'next_hearing_date'
COURT_TYPE = 'court_type'
HEARING_DATE = 'hearing_date'
CASE_TITLE = 'case_title'
INT_CASE_NUMBER = 'int_case_number'
CASE_SECURITY = 'case_security'
FILL_OUT_FORM_URL = 'fill_out_form_url'
GUIDED_INTERVIEW_URL = 'guided_interview_url'
JUSTICE_COURT_CODE = 'J'
DISTRICT_COURT_CODE = 'D'
JUSTICE_COURT = 'justice'
DISTRICT_COURT = 'district'

# CASE
CASE_SECURITY_EXPUNGED = 'Expunged'
CASE_SECURITY_SEALED = 'Sealed'
CASE_NUMBER_KEY = 'case number'
CASE_TITLE_KEY = 'case title'
LOCATION_KEY = 'location'
LOCATION = 'location'
COURT_NAME = 'court_name'
CITY = 'city'

# HEARING DATE
CASE_NUMBER_KEY = 'case number'
CASE_TITLE_KEY = 'case title'
HEARING_DATE_KEY = 'hearing date'
HEARING_LOCATION_KEY = 'hearing location'
LOCATION = 'location'
COURT_NAME = 'court_name'
CITY = 'city'

# CHARGES
SEQUENCE = 'sequence'
OFFENSE = 'offense'
SEVERITY = 'severity'
SEVERITY_CODE = 'severity_code'
VIOLATION_DATE = 'violation_date'
VIOLATION_DATE_KEY = 'violation date'
DESCRIPTION = 'descr'

# PARTIES
TYPE = 'type'
PARTY = 'party'
REPRESENTED_BY = 'represented_by'
REPRESENTED_BY_KEY = 'represented by'

# PAYMENT
EPAY_WEB_USER = 'epay_web_user'
EPAY_AMOUNT = 'epay_amount'
EPAY_PARTY = 'epay_party'
FORM_INPUT_NAME_EPAY_WEB_USER = 'epay_WebUser'
FORM_INPUT_NAME_EPAY_AMOUNT = 'epay_Amount'
FORM_INPUT_NAME_EPAY_PARTY = 'epay_Party'
FORM_INPUT_NAME_EPAY_INT_CASE_NUMBER = 'epay_IntCase'
FORM_INPUT_NAME_EPAY_COURT_TYPE = 'epay_CourtType'
PAYMENT_URL = '/ePayments/selectPayment.jsp'

# NOTIFICATION & PASSWORD CHANGE
MY_CASE_PROFILE_URL = '/MyCaseWEB/UserInformationServlet'

# SLOTS
SLOT_USER_NAME = 'user_name'
SLOT_CASE_NUMBER = 'case_number'
SLOT_LOCATION_CODE = 'location_code'
SLOT_COURT_TYPE = 'court_type'
SLOT_FEEDBACK = 'feedback'
SLOT_KNOW_CASE_NUMBER = 'know_case_number'
SLOT_REENTER_CASE_NUMBER = 'reenter_case_number'
SLOT_VIEW_UPCOMING_HEARING_DATES = 'view_upcoming_hearing_dates'

# COMMON UTTERANCES
UTTER_PROBLEM = 'utter_problem'
UTTER_OFFER_HELP = 'utter_offer_help'
UTTER_CHECK_USER_SATISFACTION = 'utter_check_user_satisfaction'
UTTER_ASK_FEEDBACK = 'utter_ask_feedback'
UTTER_THANKS = 'utter_thanks'
UTTER_NO_CASES = 'utter_no_cases'
UTTER_SAME_CASE_NUMBER = 'utter_same_case_number'
UTTER_SELECT_CASE = 'utter_select_case'
UTTER_CASE_NUMBER_MISMATCH = 'utter_case_number_mismatch'
UTTER_CASE = 'utter_case'
UTTER_CASES = 'utter_cases'
UTTER_WELCOME_USER = 'utter_welcome_user'
UTTER_GREET_USER = 'utter_greet_user'
UTTER_POPULAR_QUESTIONS = 'utter_popular_questions'
UTTER_NOT_APPLICABLE = 'utter_not_applicable'
UTTER_DIRECTIONS_TO_UPDATE_NOTIFICATION = 'utter_directions_to_update_notification'
UTTER_DIRECTIONS_TO_CHANGE_USERNAME = 'utter_directions_to_change_username'
UTTER_DIRECTIONS_TO_CHANGE_PASSWORD = 'utter_directions_to_change_password'
UTTER_PROCESS_MISSED_HEARING_NOTICE = 'utter_process_missed_hearing_notice'
UTTER_PROCESS_LOST_CONNECTION_DURING_HEARING = 'utter_process_lost_connection_during_hearing'

# CASE FORM UTTERANCES

UTTER_DIRECTIONS_FOR_CASE_NUMBER = 'utter_directions_for_case_number'
UTTER_ENTER_CASE_NUMBER = 'utter_enter_case_number'

# HEARING DATE UTTERANCES
UTTER_FIND_HEARING_DATE = 'utter_find_hearing_date'
UTTER_NEXT_HEARING_DATE = 'utter_next_hearing_date'
UTTER_DIRECTIONS_FOR_HEARING_DATE = 'utter_directions_for_hearing_date'
UTTER_NO_HEARING_DATE = 'utter_no_hearing_date'
UTTER_DIRECTIONS_FOR_HEARING_DATE = 'utter_directions_for_hearing_date'
UTTER_UPCOMING_HEARING_INFORMATION = 'utter_upcoming_hearing_information'

# CASE INFORMATION UTTERANCES
UTTER_FIND_CASE_INFORMATION = 'utter_find_case_information'
UTTER_CASE_INFORMATION = 'utter_case_information'
UTTER_NO_VALID_CASE_INFORMATION = 'utter_no_valid_case_information'
UTTER_DIRECTIONS_FOR_CASE_INFORMATION = 'utter_directions_for_case_information'
UTTER_AUTHENTICATION_ISSUE = 'utter_authentication_issue'

# CASE CHARGE UTTERANCES
UTTER_FIND_CASE_CHARGES = 'utter_find_case_charges'
UTTER_CASE_CHARGES = 'utter_case_charges'
UTTER_NO_VALID_CASE_CHARGES = 'utter_no_valid_case_charges'
UTTER_NO_CASE_CHARGES = 'utter_no_case_charges'
UTTER_DIRECTIONS_FOR_CASE_CHARGES = 'utter_directions_for_case_charges'

# CASE PARTIES UTTERANCES
UTTER_NO_CASE_PARTIES = 'utter_no_case_parties'
UTTER_CASE_PARTIES = 'utter_case_parties'
UTTER_NO_VALID_CASE_PARTIES = 'utter_no_valid_case_parties'
UTTER_FIND_CASE_PARTIES = 'utter_find_case_parties'
UTTER_FIND_CASE_PARTIES_INFORMATION = 'utter_find_case_parties_information'

# CASE PAYMENT UTTERANCES
UTTER_NO_CASE_PAYMENT = 'utter_no_case_payment'
UTTER_NO_VALID_CASE_PAYMENT = 'utter_no_valid_case_payment'
UTTER_FIND_CASE_PAYMENT = 'utter_find_case_payment'
UTTER_FIND_CASE_PAYMENT_INFORMATION = 'utter_find_case_payment_information'

# CASE FILE UPLOAD UTTERANCES
UTTER_FILE_UPLOAD_INFORMATION = 'utter_file_upload_information'
UTTER_FIND_FILE_UPLOAD_INFORMATION = 'utter_find_file_upload_information'
UTTER_NO_FILE_UPLOAD_INFORMATION = 'utter_no_file_upload_information'
DOCUMENT_FILING_INSTRUCTIONS_LINK = 'https://www.utcourts.gov/howto/filing/'

# EVICTION RELATED LINKS
SELF_HELP_HOUSING_LINK = 'https://www.utcourts.gov/selfhelp/housing.php'
PROTECTIVE_ORDERS_LINK = 'https://www.utcourts.gov/abuse/protective_orders.html'
EVICTION_INFORMATION_FOR_LANDLORDS_LINK = 'https://www.utcourts.gov/howto/landlord/eviction-landlord.html'
EVICTION_INFORMATION_FOR_TENANTS_LINK = 'https://www.utcourts.gov/howto/landlord/eviction-tenant.html'
BAD_HOUSING_PAGE_FROM_UTAH_LEGAL_SERVICES_LINK = 'https://www.utahlegalservices.org/node/7/bad-housing'
ANSWERING_A_COMPLAINT_OR_PETITION_LINK = 'https://www.utcourts.gov/howto/answer/'
TENANT_PERSONAL_PROPERTY_LINK = 'https://www.utcourts.gov/howto/landlord/tenants_personal_property.html#recovering'
REFUNDING_RENTER_DEPOSIT_LINK = 'https://www.utcourts.gov/howto/landlord/refunding_deposits.html'
FINDING_LEGAL_HELP_LINK = 'https://www.utcourts.gov/howto/legalassist/'
SELF_HELP_CENTER_LINK = 'https://www.utcourts.gov/selfhelp/contact/'

# EVICTION UTTERANCES
UTTER_EVICTION_SUMMARY = 'utter_eviction_summary'
UTTER_EVICTION_PROCEDURE = 'utter_eviction_procedure'
UTTER_PROCESS_EVICTION = 'utter_process_eviction'
UTTER_RETRIEVE_BELONGINGS = 'utter_retrieve_belongings'
UTTER_PROCESS_RENT_REJECTION = 'utter_process_rent_rejection'
UTTER_PROCEDURE_TO_RETRIEVE_DEPOSIT = 'utter_procedure_to_retrieve_deposit'
UTTER_COMMERCIAL_EVICTION_PROCEDURE = 'utter_commercial_eviction_procedure'

# EVICTION ACTIONS
ACTION_PROVIDE_EVICTION_SUMMARY = 'action_provide_eviction_summary'
ACTION_PROVIDE_EVICTION_PROCEDURE = 'action_provide_eviction_procedure'
ACTION_PROCESS_EVICTION = 'action_process_eviction'
ACTION_RETRIEVE_BELONGINGS = 'action_retrieve_belongings'
ACTION_PROCESS_RENT_REJECTION = 'action_process_rent_rejection'
ACTION_RETRIEVE_DEPOSIT = 'action_retrieve_deposit'
ACTION_PROVIDE_COMMERCIAL_EVICTION_PROCEDURE = 'action_provide_commercial_eviction_procedure'

# BOT ACTIONS
ACTION_SESSION_START = 'action_session_start'
ACTION_WELCOME_USER = 'action_welcome_user'
ACTION_GREET_USER = 'action_greet_user'
ACTION_FETCH_ALL_CASES = 'action_fetch_all_cases'
ACTION_FETCH_HEARING_DATE = 'action_fetch_hearing_date'
ACTION_FETCH_NEXT_HEARING_DATE = 'action_fetch_next_hearing_date'
ACTION_FETCH_CHARGES = 'action_fetch_charges'
ACTION_FETCH_CASE_INFORMATION = 'action_fetch_case_information'
ACTION_FETCH_FILE_UPLOAD_INFORMATION = 'action_fetch_file_upload_information'
ACTION_FETCH_PARTIES = 'action_fetch_parties'
ACTION_FETCH_PAYMENT = 'action_fetch_payment'
ACTION_SAVE_FEEDBACK = 'action_save_feedback'
ACTION_PROCESS_MISSED_HEARING_NOTICE = 'action_process_missed_hearing_notice'
ACTION_PROCESS_LOST_CONNECTION_DURING_HEARING = 'action_process_lost_connection_during_hearing'
ACTION_DIRECT_USERS_TO_UPDATE_NOTIFICATION = 'action_direct_users_to_update_notification'
ACTION_DIRECT_USERS_TO_CHANGE_USERNAME = 'action_direct_users_to_change_username'
ACTION_DIRECT_USERS_TO_CHANGE_PASSWORD = 'action_direct_users_to_change_password'
ACTION_ASK_CASE_NUMBER = 'action_ask_case_number'
VALIDATE_CASE_FORM = 'validate_case_form'
VALIDATE_FEEDBACK_FORM = 'validate_feedback_form'
VALIDATE_UPCOMING_HEARING_DATE_FORM = 'validate_upcoming_hearing_date_form'

# ENVIRONMENT VARIABLE NAMES
MYCASE_BASE_PATH = 'MYCASE_BASE_PATH'
MONGODB_URL = 'MONGODB_URL'
MONGODB_NAME = 'MONGODB_NAME'
MONGODB_COLLECTION_NAME = 'MONGODB_COLLECTION_NAME'
MONGODB_USERNAME = 'MONGODB_USERNAME'
MONGODB_PASSWORD = 'MONGODB_PASSWORD'
MONGODB_AUTH_SOURCE = 'MONGODB_AUTH_SOURCE'
MONGODB_ANALYTICS_COLLECTION_NAME = 'MONGODB_ANALYTICS_COLLECTION_NAME'
MONGODB_FEEDBACK_COLLECTION_NAME = 'MONGODB_FEEDBACK_COLLECTION_NAME'
LOGGER_LEVEL = 'LOGGER_LEVEL'
ERROR = 'ERROR'

# CAROUSEL KEYS
ATTACHMENT = 'attachment'
ELEMENTS = 'elements'
PAYLOAD = 'payload'

# MONGO UTIL
ADMIN_AUTH_SOURCE = 'admin'

# EMOJIS
EMOJI_FLAG = '🚩 '
EMOJI_CALENDER = '📅 '
EMOJI_HASH = '#️⃣ '
