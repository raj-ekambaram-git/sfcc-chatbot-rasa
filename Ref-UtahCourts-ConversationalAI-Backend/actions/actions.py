import copy
import json
import logging
import os
from typing import Any, Dict, List, Text

from client import swagger_client
from constants.app_constants import (
    ACTION_ASK_CASE_NUMBER, ACTION_DIRECT_USERS_TO_CHANGE_PASSWORD,
    ACTION_DIRECT_USERS_TO_CHANGE_USERNAME,
    ACTION_DIRECT_USERS_TO_UPDATE_NOTIFICATION, ACTION_FETCH_ALL_CASES,
    ACTION_GREET_USER, ACTION_PROCESS_LOST_CONNECTION_DURING_HEARING,
    ACTION_PROCESS_MISSED_HEARING_NOTICE, ACTION_SAVE_FEEDBACK,
    ACTION_SESSION_START, ACTION_WELCOME_USER, ATTACHMENT, AUTHORIZATION,
    CASE_NUMBER, CASE_NUMBER_KEY, CASE_TITLE, CASE_TITLE_KEY, CITY, COURT_NAME,
    COURT_TYPE, DATA, DISTRICT_COURT, DISTRICT_COURT_CODE, ELEMENTS, ERROR,
    EVENT, JUSTICE_COURT, JUSTICE_COURT_CODE, LOCATION, LOCATION_CODE,
    LOCATION_KEY, LOGGER_LEVEL, METADATA, MY_CASE_PROFILE_URL,
    MYCASE_BASE_PATH, PAYLOAD, SELF_HELP_CENTER_LINK, SLOT_CASE_NUMBER,
    SLOT_COURT_TYPE, SLOT_FEEDBACK, SLOT_KNOW_CASE_NUMBER, SLOT_LOCATION_CODE,
    SLOT_REENTER_CASE_NUMBER, SLOT_USER_NAME, USER_EVENT, USER_ID, USER_NAME,
    UTTER_CASE, UTTER_CASE_NUMBER_MISMATCH, UTTER_CASES,
    UTTER_DIRECTIONS_FOR_CASE_NUMBER, UTTER_DIRECTIONS_TO_CHANGE_PASSWORD,
    UTTER_DIRECTIONS_TO_CHANGE_USERNAME,
    UTTER_DIRECTIONS_TO_UPDATE_NOTIFICATION, UTTER_ENTER_CASE_NUMBER,
    UTTER_GREET_USER, UTTER_NO_CASES, UTTER_POPULAR_QUESTIONS, UTTER_PROBLEM,
    UTTER_PROCESS_LOST_CONNECTION_DURING_HEARING,
    UTTER_PROCESS_MISSED_HEARING_NOTICE, UTTER_SAME_CASE_NUMBER,
    UTTER_SELECT_CASE, UTTER_WELCOME_USER, VALIDATE_CASE_FORM,
    VALIDATE_FEEDBACK_FORM)
from constants.messages import (CASE_BUTTON_TITLE, CASE_CUSTOM_JSON,
                                CASE_DETAILS_BUTTON_PAYLOAD)
from rasa_sdk import Action, Tracker
from rasa_sdk.events import (ActionExecuted, EventType, SessionStarted,
                             SlotSet, UserUtteranceReverted)
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from utils.common_util import perform_analytics, save_feedback

api_instance = swagger_client.MyCaseApi()

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get(LOGGER_LEVEL, ERROR))


class ActionSessionStart(Action):
    def name(self) -> Text:
        return ACTION_SESSION_START

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        logger.info('ACTION_SESSION_START - Execution started')

        if tracker.get_slot('session_started_metadata'):
            metadata = tracker.get_slot('session_started_metadata')
        else:
            for e in tracker.events[::-1]:
                if e[EVENT] == USER_EVENT:
                    metadata = e[METADATA]
                    break
        if 'analytics' in metadata:
            perform_analytics(
                json.loads(
                    json.dumps(
                        metadata['analytics'],
                        sort_keys=True)))

        logger.info('ACTION_SESSION_START - Execution ended')
        return [SessionStarted(), ActionExecuted('action_listen')]


class ActionWelcomeUser(Action):

    def name(self) -> Text:
        return ACTION_WELCOME_USER

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info('ACTION_WELCOME_USER - Execution started')

        metadata = None
        for e in tracker.events[::-1]:
            if e[EVENT] == USER_EVENT:
                metadata = e[METADATA]
                break
        user_name = metadata[USER_NAME].title()
        dispatcher.utter_message(
            response=UTTER_WELCOME_USER, user_name=user_name)
        dispatcher.utter_message(response=UTTER_POPULAR_QUESTIONS)

        logger.info('ACTION_WELCOME_USER - Execution ended')
        return [SlotSet(SLOT_USER_NAME, user_name)]


class ActionGreetUser(Action):

    def name(self) -> Text:
        return ACTION_GREET_USER

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info('ACTION_GREET_USER - Execution started')

        if tracker.get_slot(USER_NAME):
            dispatcher.utter_message(response=UTTER_GREET_USER)
            logger.info('ACTION_GREET_USER - Execution ended')
            return []
        else:
            metadata = None
            for e in tracker.events[::-1]:
                if e[EVENT] == USER_EVENT:
                    metadata = e[METADATA]
                    break
            user_name = metadata[USER_NAME].title()
            dispatcher.utter_message(
                response=UTTER_GREET_USER, user_name=user_name)
            logger.info('ACTION_GREET_USER - Execution ended')
            return [SlotSet(SLOT_USER_NAME, user_name)]


class ActionFetchAllCases(Action):

    def name(self) -> Text:
        return ACTION_FETCH_ALL_CASES

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info('ACTION_FETCH_ALL_CASES - Execution started')
        try:
            metadata = None
            for e in tracker.events[::-1]:
                if e[EVENT] == USER_EVENT:
                    metadata = e[METADATA]
                    break
            authorization = metadata[AUTHORIZATION]
            response = api_instance.get_available_cases(authorization)
            logger.info('REST SERVICES - Case response successful')
            cases = response.to_dict()[DATA]

            if len(cases) == 0:
                dispatcher.utter_message(response=UTTER_NO_CASES)
            else:
                case_custom_json = copy.deepcopy(
                    CASE_CUSTOM_JSON)
                for case in cases:
                    case_custom_json[ATTACHMENT][PAYLOAD][ELEMENTS].append({
                        CASE_NUMBER_KEY: case[CASE_NUMBER],
                        CASE_TITLE_KEY: case[CASE_TITLE],
                        LOCATION_KEY: f'{case[COURT_NAME]}, {case[LOCATION][CITY]}'
                    })
                if len(cases) == 1:
                    dispatcher.utter_message(
                        response=UTTER_CASE)
                else:
                    dispatcher.utter_message(
                        response=UTTER_CASES)
                dispatcher.utter_message(
                    json_message=case_custom_json)
        except Exception as ex:
            logger.warn(
                f'Exception occurred in ACTION_FETCH_ALL_CASES: {ex}')
            dispatcher.utter_message(response=UTTER_PROBLEM)
        finally:
            logger.info('ACTION_FETCH_ALL_CASES - Execution ended')
            return []


class ValidateFeedbackForm(FormValidationAction):
    def name(self) -> Text:
        return VALIDATE_FEEDBACK_FORM

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        required_slots = slots_mapped_in_domain + ['feedback']
        return required_slots

    async def extract_feedback(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text_of_last_user_message = tracker.latest_message.get('text')
        if text_of_last_user_message == '/deny':
            return {'feedback': None}
        else:
            logger.info(
                'EXTRACT_FEEDBACK - extracted feedback from last user text')
            return {'feedback': text_of_last_user_message}


class ActionSaveFeedback(Action):

    def name(self) -> Text:
        return ACTION_SAVE_FEEDBACK

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        metadata = None
        for e in tracker.events[::-1]:
            if e[EVENT] == USER_EVENT:
                metadata = e[METADATA]
                break
        user_id = metadata[USER_ID]
        user_name = metadata[USER_NAME]
        feedback = tracker.get_slot(SLOT_FEEDBACK)
        save_feedback({
            'user_id': user_id,
            'user_name': user_name,
            'feedback': feedback
        })
        return [SlotSet(SLOT_FEEDBACK, None)]


class ValidateCaseForm(FormValidationAction):
    def name(self) -> Text:
        return VALIDATE_CASE_FORM

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        additional_slots = []

        # Add SLOT_REENTER_CASE_NUMBER when case_number is invalid
        if tracker.get_slot(CASE_NUMBER) == '-1':
            additional_slots.append(SLOT_REENTER_CASE_NUMBER)

        return additional_slots + slots_mapped_in_domain

    # Extractor methods

    async def extract_reenter_case_number(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        """
            `reenter_case_number` is a Custom slot mapping.\n
            Extractor function for the `reenter_case_number` slot
        """
        logger.info(
            'EXTRACT_REENTER_CASE_NUMBER - Extracting re-enter case number')
        latest_intent = tracker.get_intent_of_latest_message()
        if latest_intent == 'affirm':
            return {SLOT_REENTER_CASE_NUMBER: True}
        elif latest_intent == 'deny':
            return {SLOT_REENTER_CASE_NUMBER: False}
        else:
            # SLOT_REENTER_CASE_NUMBER should be set None if any other intent
            # other than 'affirm' or 'deny' is received
            return {SLOT_REENTER_CASE_NUMBER: None}

    # Validation methods

    def validate_know_case_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """
            Validate `know_case_number` slot. \n
            If `slot_value` == `False`, Fetch all available cases \n
            Set `know_case_number` to slot_value
        """
        logger.info('VALIDATE_KNOW_CASE_NUMBER - Execution started')
        if not slot_value:
            metadata = None
            for e in tracker.events[::-1]:
                if e[EVENT] == USER_EVENT:
                    metadata = e[METADATA]
                    break
            authorization = metadata[AUTHORIZATION]
            response = api_instance.get_available_cases(authorization)
            logger.info('REST SERVICES - Case Information response successful')
            cases = response.to_dict()[DATA]
            if len(cases) == 1:
                case = cases[0]
                logger.info(
                    'VALIDATE_KNOW_CASE_NUMBER - slot set; Execution ended')
                return {
                    SLOT_KNOW_CASE_NUMBER: slot_value,
                    SLOT_CASE_NUMBER: case[CASE_NUMBER],
                    SLOT_COURT_TYPE: JUSTICE_COURT if case[COURT_TYPE] == JUSTICE_COURT_CODE else DISTRICT_COURT,
                    SLOT_LOCATION_CODE: case[LOCATION_CODE]}
            elif len(cases) > 1:
                buttons = []
                for case in cases:
                    buttons.append(
                        {
                            'content_type': 'text',
                            'title': CASE_BUTTON_TITLE.format(
                                case_number=case[CASE_NUMBER],
                                case_title=case[CASE_TITLE]),
                            'payload': CASE_DETAILS_BUTTON_PAYLOAD.format(
                                court_type=JUSTICE_COURT if case[COURT_TYPE] == JUSTICE_COURT_CODE else DISTRICT_COURT,
                                case_number=case[CASE_NUMBER],
                                location_code=case[LOCATION_CODE]),
                        })
                dispatcher.utter_message(
                    response=UTTER_SELECT_CASE, buttons=buttons)
                logger.info(
                    'VALIDATE_KNOW_CASE_NUMBER - slot set; Execution ended')
                return {SLOT_KNOW_CASE_NUMBER: slot_value}
            else:
                # This part is executed when no cases are present in the
                # account
                logger.info(
                    'VALIDATE_KNOW_CASE_NUMBER - slot set; Execution ended')
                dispatcher.utter_message(
                    response=UTTER_NO_CASES)
                return {
                    SLOT_KNOW_CASE_NUMBER: slot_value,
                    SLOT_CASE_NUMBER: '-1',
                    SLOT_REENTER_CASE_NUMBER: False}

    def validate_case_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """
            Validate `case_number` slot. \n
            Fetch for case details for input `case_number` \n
            Cases returned count:
                zero     : `case_number` is invalid - set `case_number` slot to "-1". Ask user whether to re-enter case number
                one      : `case_number` is valid - set slot and exit form. Action gets executed
                multiple : Display all cases under same case number - Set SLOT_KNOW_CASE_NUMBER = False and `requested_slot` = `case_number`
        """
        logger.info('VALIDATE_CASE_NUMBER - Execution started')

        metadata = None
        for e in tracker.events[::-1]:
            if e[EVENT] == USER_EVENT:
                metadata = e[METADATA]
                break
        authorization = metadata[AUTHORIZATION]
        case_number = slot_value
        court_type = tracker.get_slot(
            SLOT_COURT_TYPE) if tracker.get_slot(
            SLOT_COURT_TYPE) else None
        if court_type:
            court_type = JUSTICE_COURT_CODE if court_type == JUSTICE_COURT else DISTRICT_COURT_CODE
        location_code = tracker.get_slot(SLOT_LOCATION_CODE)
        cases = []
        response = None
        if case_number and court_type and location_code:
            response = api_instance.get_case_by_case_number(
                authorization, case_number, court_type=court_type, location_code=location_code)
        elif case_number and court_type:
            response = api_instance.get_case_by_case_number(
                authorization, case_number, court_type=court_type)
        elif case_number and location_code:
            response = api_instance.get_case_by_case_number(
                authorization, case_number, location_code=location_code)
        elif case_number:
            response = api_instance.get_case_by_case_number(
                authorization, case_number)
        else:
            response = api_instance.get_available_cases(authorization)

        logger.info('REST SERVICES - Case Information response successful')
        cases = response.to_dict()[DATA]

        if len(cases) == 1:
            case = cases[0]
            logger.info('VALIDATE_CASE_NUMBER - slot set; Execution ended')
            return {
                SLOT_CASE_NUMBER: slot_value,
                SLOT_COURT_TYPE: JUSTICE_COURT if case[COURT_TYPE] == JUSTICE_COURT_CODE else DISTRICT_COURT,
                SLOT_LOCATION_CODE: case[LOCATION_CODE],
                SLOT_KNOW_CASE_NUMBER: True}
        elif len(cases) > 1:
            buttons = []
            for case in cases:
                buttons.append(
                    {
                        'content_type': 'text',
                        'title': CASE_BUTTON_TITLE.format(
                            case_number=case[CASE_NUMBER],
                            case_title=case[CASE_TITLE]),
                        'payload': CASE_DETAILS_BUTTON_PAYLOAD.format(
                            court_type=JUSTICE_COURT if case[COURT_TYPE] == JUSTICE_COURT_CODE else DISTRICT_COURT,
                            case_number=case[CASE_NUMBER],
                            location_code=case[LOCATION_CODE]),
                    })
            dispatcher.utter_message(
                response=UTTER_SAME_CASE_NUMBER, buttons=buttons)
            # SLOT_KNOW_CASE_NUMBER: False - utter_enter_case_number should not be uttered as quick reply buttons are displayed
            # CASE_NUMBER: None - This sets requested_slot = CASE_NUMBER; Scope
            # stays inside form

            logger.info(
                'VALIDATE_CASE_NUMBER - slot not set (Multiple cases); Execution ended')
            return {SLOT_CASE_NUMBER: None, SLOT_KNOW_CASE_NUMBER: False}
        else:
            dispatcher.utter_message(response=UTTER_CASE_NUMBER_MISMATCH)
            dispatcher.utter_message(response=UTTER_DIRECTIONS_FOR_CASE_NUMBER)
            # CASE_NUMBER: '-1' - Adds SLOT_REENTER_CASE_NUMBER to
            # requested_slot list

            logger.info(
                'VALIDATE_CASE_NUMBER - slot not set (Invalid case number); Execution ended')
            return {
                SLOT_CASE_NUMBER: '-1',
                SLOT_REENTER_CASE_NUMBER: None,
                SLOT_KNOW_CASE_NUMBER: True}

    def validate_reenter_case_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """
            validate `reenter_case_number`\n
            slot_value == `True` : User chose to re-enter case number
                Reset `case_number` to None - adds `case_number` to resquested_slot \n
            slot_value == `False` : User chose not to re-enter case number
                All slot are set at this point. Deactivate the form \n
                (SLOT_REENTER_CASE_NUMBER = False,
                 SLOT_KNOW_CASE_NUMBER = True,
                 CASE_NUMBER = -1)
        """
        logger.info('VALIDATE_REENTER_CASE_NUMBER - Execution started')
        if slot_value:
            logger.info('VALIDATE_REENTER_CASE_NUMBER - Execution ended')
            return {
                SLOT_REENTER_CASE_NUMBER: slot_value,
                SLOT_CASE_NUMBER: None,
                SLOT_KNOW_CASE_NUMBER: True}
        else:
            logger.info('VALIDATE_REENTER_CASE_NUMBER - Execution ended')
            return {SLOT_REENTER_CASE_NUMBER: slot_value}


class ActionAskCaseNumber(Action):
    def name(self) -> Text:
        return ACTION_ASK_CASE_NUMBER

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        # Skip the utterance when SLOT_KNOW_CASE_NUMBER is set to False
        if tracker.get_slot(SLOT_KNOW_CASE_NUMBER):
            logger.info('ACTION_ASK_CASE_NUMBER - Execution started')
            dispatcher.utter_message(response=UTTER_ENTER_CASE_NUMBER)
            logger.info('ACTION_ASK_CASE_NUMBER - Execution ended')
        return []


class ActionDirectUsersToUpdateNotification(Action):
    def name(self) -> Text:
        return ACTION_DIRECT_USERS_TO_UPDATE_NOTIFICATION

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        logger.info(
            'ACTION_DIRECT_USERS_TO_UPDATE_NOTIFICATION - Execution started')
        base_path_url = os.environ.get(MYCASE_BASE_PATH)
        formatted_url_link = base_path_url + MY_CASE_PROFILE_URL
        dispatcher.utter_message(
            response=UTTER_DIRECTIONS_TO_UPDATE_NOTIFICATION,
            url_link=formatted_url_link)
        logger.info(
            'ACTION_DIRECT_USERS_TO_UPDATE_NOTIFICATION - Execution ended')
        return []


class ActionDirectUsersToChangePassword(Action):
    def name(self) -> Text:
        return ACTION_DIRECT_USERS_TO_CHANGE_PASSWORD

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        logger.info(
            'ACTION_DIRECT_USERS_TO_CHANGE_PASSWORD - Execution started')
        base_path_url = os.environ.get(MYCASE_BASE_PATH)
        formatted_url_link = base_path_url + MY_CASE_PROFILE_URL
        dispatcher.utter_message(
            response=UTTER_DIRECTIONS_TO_CHANGE_PASSWORD,
            url_link=formatted_url_link)
        logger.info('ACTION_DIRECT_USERS_TO_CHANGE_PASSWORD - Execution ended')
        return []


class ActionDirectUsersToChangeUsername(Action):
    def name(self) -> Text:
        return ACTION_DIRECT_USERS_TO_CHANGE_USERNAME

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        logger.info(
            'ACTION_DIRECT_USERS_TO_CHANGE_USERNAME - Execution started')
        base_path_url = os.environ.get(MYCASE_BASE_PATH)
        formatted_url_link = base_path_url + MY_CASE_PROFILE_URL
        dispatcher.utter_message(
            response=UTTER_DIRECTIONS_TO_CHANGE_USERNAME,
            url_link=formatted_url_link)
        logger.info('ACTION_DIRECT_USERS_TO_CHANGE_USERNAME - Execution ended')
        return []


class ActionProcessMissedHearingNotice(Action):
    def name(self) -> Text:
        return ACTION_PROCESS_MISSED_HEARING_NOTICE

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        logger.info('ACTION_PROCESS_MISSED_HEARING_NOTICE - Execution started')
        dispatcher.utter_message(
            response=UTTER_PROCESS_MISSED_HEARING_NOTICE,
            self_help_center_link=SELF_HELP_CENTER_LINK)
        logger.info('ACTION_PROCESS_MISSED_HEARING_NOTICE - Execution ended')
        return []


class ActionProcessLostConnectionDuringHearing(Action):
    def name(self) -> Text:
        return ACTION_PROCESS_LOST_CONNECTION_DURING_HEARING

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        logger.info(
            'ACTION_PROCESS_LOST_CONNECTION_DURING_HEARING - Execution started')
        dispatcher.utter_message(
            response=UTTER_PROCESS_LOST_CONNECTION_DURING_HEARING,
            self_help_center_link=SELF_HELP_CENTER_LINK)
        logger.info(
            'ACTION_PROCESS_LOST_CONNECTION_DURING_HEARING - Execution ended')
        return []
