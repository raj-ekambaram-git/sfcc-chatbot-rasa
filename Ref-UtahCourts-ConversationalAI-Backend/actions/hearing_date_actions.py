import copy
import logging
import os
import time
from typing import Any, Dict, List, Text

from client import swagger_client
from constants.app_constants import (ACTION_FETCH_HEARING_DATE,
                                     ACTION_FETCH_NEXT_HEARING_DATE,
                                     ATTACHMENT, AUTHORIZATION, CASE_NUMBER,
                                     CASE_NUMBER_KEY, CASE_TITLE,
                                     CASE_TITLE_KEY, CITY, COURT_NAME,
                                     COURT_TYPE, DATA, DISTRICT_COURT,
                                     DISTRICT_COURT_CODE, ELEMENTS, ERROR,
                                     EVENT, HEARING_DATE_KEY,
                                     HEARING_LOCATION_KEY, JUSTICE_COURT,
                                     JUSTICE_COURT_CODE, LOCATION,
                                     LOCATION_CODE, LOGGER_LEVEL, METADATA,
                                     NEXT_HEARING_DATE, PAYLOAD,
                                     SLOT_CASE_NUMBER, SLOT_COURT_TYPE,
                                     SLOT_KNOW_CASE_NUMBER, SLOT_LOCATION_CODE,
                                     SLOT_REENTER_CASE_NUMBER,
                                     SLOT_VIEW_UPCOMING_HEARING_DATES,
                                     USER_EVENT, UTTER_CASE_NUMBER_MISMATCH,
                                     UTTER_DIRECTIONS_FOR_CASE_NUMBER,
                                     UTTER_DIRECTIONS_FOR_HEARING_DATE,
                                     UTTER_NEXT_HEARING_DATE,
                                     UTTER_NO_HEARING_DATE, UTTER_PROBLEM,
                                     UTTER_SAME_CASE_NUMBER,
                                     UTTER_UPCOMING_HEARING_INFORMATION,
                                     VALIDATE_UPCOMING_HEARING_DATE_FORM)
from constants.messages import (CASE_BUTTON_TITLE, CASE_DETAILS_BUTTON_PAYLOAD,
                                CASE_HEARING_DATE_CUSTOM_JSON)
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

api_instance = swagger_client.MyCaseApi()

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get(LOGGER_LEVEL, ERROR))


class ValidateUpcomingHearingDateForm(FormValidationAction):
    def name(self) -> Text:
        return VALIDATE_UPCOMING_HEARING_DATE_FORM

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
                CASE_NUMBER: None,
                SLOT_KNOW_CASE_NUMBER: True}
        else:
            logger.info('VALIDATE_REENTER_CASE_NUMBER - Execution ended')
            return {SLOT_REENTER_CASE_NUMBER: slot_value}

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
            logger.info('VALIDATE_CASE_NUMBER - slot set; Execution ended')
            return {CASE_NUMBER: slot_value, SLOT_KNOW_CASE_NUMBER: True}
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
            return {CASE_NUMBER: None, SLOT_KNOW_CASE_NUMBER: False}
        else:
            dispatcher.utter_message(response=UTTER_CASE_NUMBER_MISMATCH)
            dispatcher.utter_message(response=UTTER_DIRECTIONS_FOR_CASE_NUMBER)
            # CASE_NUMBER: '-1' - Adds SLOT_REENTER_CASE_NUMBER to
            # requested_slot list
            logger.info(
                'VALIDATE_CASE_NUMBER - slot not set (Invalid case number); Execution ended')
            return {CASE_NUMBER: '-1', SLOT_REENTER_CASE_NUMBER: None}

    def validate_view_upcoming_hearing_dates(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """
            validate `view_upcoming_hearing_dates`\n
            slot_value == `True` : User chose to view hearing dates of other cases
                Fetch all cases with hearing date expect the nearest_hearing_date case \n
            slot_value == `False` : User chose not to view hearing dates of other cases
                Set `case_number` slot to '-2' and skip action execution in the rasa action, following this form.\n
                (SLOT_VIEW_UPCOMING_HEARING_DATES = False,
                 CASE_NUMBER = -2)
        """
        logger.info('VALIDATE_VIEW_UPCOMING_HEARING_DATES - Execution started')
        if slot_value:
            metadata = None
            for e in tracker.events[::-1]:
                if e[EVENT] == USER_EVENT:
                    metadata = e[METADATA]
                    break
            authorization = metadata[AUTHORIZATION]
            response = api_instance.get_available_cases(authorization)
            logger.info('REST SERVICES - Case Information response successful')
            cases = response.to_dict()[DATA]

            # find the nearest hearing date case and display the rest of the
            # cases
            nearest_hearing_date = ''
            for case in cases:
                if case[NEXT_HEARING_DATE]:
                    if nearest_hearing_date == '':
                        nearest_hearing_date = case[NEXT_HEARING_DATE]
                        continue
                    formatted_date_1 = time.strptime(
                        nearest_hearing_date, '%m/%d/%Y %I:%M %p')
                    formatted_date_2 = time.strptime(
                        case[NEXT_HEARING_DATE], '%m/%d/%Y %I:%M %p')
                    nearest_hearing_date = case[NEXT_HEARING_DATE] if formatted_date_1 > formatted_date_2 else nearest_hearing_date

            # filtering the cases : skip the case that has nearest hearing date
            filtered_cases = [
                case for case in cases if (
                    case[NEXT_HEARING_DATE] is not None and case[NEXT_HEARING_DATE] != nearest_hearing_date)]

            buttons = []
            for case in filtered_cases:
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
                response=UTTER_UPCOMING_HEARING_INFORMATION,
                buttons=buttons)
            logger.info(
                'VALIDATE_VIEW_UPCOMING_HEARING_DATES - Execution ended')
            return {SLOT_VIEW_UPCOMING_HEARING_DATES: slot_value,
                    CASE_NUMBER: None, SLOT_KNOW_CASE_NUMBER: False}
        else:
            logger.info(
                'VALIDATE_VIEW_UPCOMING_HEARING_DATES - Execution ended')
            return {
                SLOT_VIEW_UPCOMING_HEARING_DATES: slot_value,
                CASE_NUMBER: '-2'}


class ActionFetchNextHearingDate(Action):

    def name(self) -> Text:
        return ACTION_FETCH_NEXT_HEARING_DATE

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info('ACTION_FETCH_NEXT_HEARING_DATE - Execution started')
        try:
            metadata = None
            for e in tracker.events[::-1]:
                if e[EVENT] == USER_EVENT:
                    metadata = e[METADATA]
                    break
            authorization = metadata[AUTHORIZATION]

            response = api_instance.get_available_cases(authorization)
            logger.info('REST SERVICES - Case Information response successful')
            cases = response.to_dict()[DATA]

            # filtering the cases : take only the cases which has hearing date
            filtered_cases = []
            for case in cases:
                if case[NEXT_HEARING_DATE]:
                    filtered_cases.append(case)
            if len(filtered_cases) == 0:
                # No valid case having a hearing date
                dispatcher.utter_message(
                    response=UTTER_NO_HEARING_DATE)
                dispatcher.utter_message(
                    response=UTTER_DIRECTIONS_FOR_HEARING_DATE)
                return [SlotSet(SLOT_VIEW_UPCOMING_HEARING_DATES, False)]

            all_hearing_dates = set()
            nearest_hearing_date = ''
            for case in filtered_cases:
                all_hearing_dates.add(case[NEXT_HEARING_DATE])
                if nearest_hearing_date == '':
                    nearest_hearing_date = case[NEXT_HEARING_DATE]
                    continue
                formatted_date_1 = time.strptime(
                    nearest_hearing_date, '%m/%d/%Y %I:%M %p')
                formatted_date_2 = time.strptime(
                    case[NEXT_HEARING_DATE], '%m/%d/%Y %I:%M %p')
                nearest_hearing_date = case[NEXT_HEARING_DATE] if formatted_date_1 > formatted_date_2 else nearest_hearing_date

            logger.info(
                'ACTION_FETCH_NEXT_HEARING_DATE - Nearest hearing date identified')
            upcoming_hearing_date_cases = []
            for case in filtered_cases:
                if case[NEXT_HEARING_DATE] == nearest_hearing_date:
                    upcoming_hearing_date_cases.append(case)
            case_hearing_date_custom_json = copy.deepcopy(
                CASE_HEARING_DATE_CUSTOM_JSON)

            if len(all_hearing_dates) == 1:
                logger.info(
                    'ACTION_FETCH_NEXT_HEARING_DATE - Only one case has hearing date')
                for case in upcoming_hearing_date_cases:
                    case_hearing_date_custom_json[ATTACHMENT][PAYLOAD][ELEMENTS].append({
                        CASE_NUMBER_KEY: case[CASE_NUMBER],
                        CASE_TITLE_KEY: case[CASE_TITLE],
                        HEARING_DATE_KEY: case[NEXT_HEARING_DATE],
                        HEARING_LOCATION_KEY: f'{case[COURT_NAME]}, {case[LOCATION][CITY]}'
                    })
                dispatcher.utter_message(
                    response=UTTER_NEXT_HEARING_DATE,
                    json_message=case_hearing_date_custom_json)
                dispatcher.utter_message(
                    response=UTTER_DIRECTIONS_FOR_HEARING_DATE)
                return [SlotSet(SLOT_VIEW_UPCOMING_HEARING_DATES, False)]

            elif len(all_hearing_dates) > 1:
                for case in upcoming_hearing_date_cases:
                    if case[NEXT_HEARING_DATE] == nearest_hearing_date:
                        case_hearing_date_custom_json[ATTACHMENT][PAYLOAD][ELEMENTS].append({
                            CASE_NUMBER_KEY: case[CASE_NUMBER],
                            CASE_TITLE_KEY: case[CASE_TITLE],
                            HEARING_DATE_KEY: case[NEXT_HEARING_DATE],
                            HEARING_LOCATION_KEY: f'{case[COURT_NAME]}, {case[LOCATION][CITY]}'
                        })
                dispatcher.utter_message(
                    response=UTTER_NEXT_HEARING_DATE,
                    json_message=case_hearing_date_custom_json)
                dispatcher.utter_message(
                    response=UTTER_DIRECTIONS_FOR_HEARING_DATE)
                return [
                    SlotSet(
                        SLOT_CASE_NUMBER, None), SlotSet(
                        SLOT_COURT_TYPE, None), SlotSet(
                        SLOT_LOCATION_CODE, None), SlotSet(
                        SLOT_KNOW_CASE_NUMBER, None), SlotSet(
                            SLOT_REENTER_CASE_NUMBER, None)]
        except Exception as ex:
            logger.warn(
                f'Exception occurred in ACTION_FETCH_NEXT_HEARING_DATE: {ex}')
            dispatcher.utter_message(response=UTTER_PROBLEM)
            return [SlotSet(SLOT_VIEW_UPCOMING_HEARING_DATES, False)]


class ActionFetchHearingDate(Action):

    def name(self) -> Text:
        return ACTION_FETCH_HEARING_DATE

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info('ACTION_FETCH_HEARING_DATE - Execution started')
        try:
            metadata = None
            for e in tracker.events[::-1]:
                if e[EVENT] == USER_EVENT:
                    metadata = e[METADATA]
                    break
            authorization = metadata[AUTHORIZATION]
            case_number = tracker.get_slot(SLOT_CASE_NUMBER)

            # Skip the Action execution when case_number == -1 || -2.
            # -1 : Occurs when user entered an incorrect case number and chose not to re-enter
            # -2 : Occurs when user chose not to view the upcoming hearing dates
            if case_number != '-1' and case_number != '-2':
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

                logger.info(
                    'REST SERVICES - Case Information response successful')
                cases = response.to_dict()[DATA]

                case = cases[0]
                if case[NEXT_HEARING_DATE]:
                    case_hearing_date_custom_json = copy.deepcopy(
                        CASE_HEARING_DATE_CUSTOM_JSON)
                    case_hearing_date_custom_json[ATTACHMENT][PAYLOAD][ELEMENTS].append({
                        CASE_NUMBER_KEY: case[CASE_NUMBER],
                        CASE_TITLE_KEY: case[CASE_TITLE],
                        HEARING_DATE_KEY: case[NEXT_HEARING_DATE],
                        HEARING_LOCATION_KEY: f'{case[COURT_NAME]}, {case[LOCATION][CITY]}'
                    })
                    dispatcher.utter_message(
                        response=UTTER_NEXT_HEARING_DATE,
                        json_message=case_hearing_date_custom_json)
                    dispatcher.utter_message(
                        response=UTTER_DIRECTIONS_FOR_HEARING_DATE)
                else:
                    dispatcher.utter_message(
                        response=UTTER_NO_HEARING_DATE)
                    dispatcher.utter_message(
                        response=UTTER_DIRECTIONS_FOR_HEARING_DATE)
        except Exception as ex:
            logger.warn(
                f'Exception occurred in ACTION_FETCH_HEARING_DATE: {ex}')
            dispatcher.utter_message(response=UTTER_PROBLEM)
        finally:
            logger.info('ACTION_FETCH_HEARING_DATE - Execution ended')
            return [
                SlotSet(
                    SLOT_CASE_NUMBER, None), SlotSet(
                    SLOT_COURT_TYPE, None), SlotSet(
                    SLOT_LOCATION_CODE, None), SlotSet(
                    SLOT_KNOW_CASE_NUMBER, None), SlotSet(
                        SLOT_REENTER_CASE_NUMBER, None), SlotSet(
                            SLOT_VIEW_UPCOMING_HEARING_DATES, None)]
