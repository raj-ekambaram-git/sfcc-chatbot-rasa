import copy
import logging
import os
from typing import Any, Dict, List, Text

from client import swagger_client
from constants.app_constants import (ACTION_FETCH_CHARGES, ATTACHMENT,
                                     AUTHORIZATION, CASE_NUMBER, CASE_SECURITY,
                                     CASE_SECURITY_EXPUNGED,
                                     CASE_SECURITY_SEALED, COURT_TYPE, DATA,
                                     DISTRICT_COURT_CODE, ELEMENTS,
                                     EMOJI_CALENDER, EMOJI_FLAG, EMOJI_HASH,
                                     ERROR, EVENT, JUSTICE_COURT,
                                     JUSTICE_COURT_CODE, LOCATION_CODE,
                                     LOGGER_LEVEL, METADATA, OFFENSE, PAYLOAD,
                                     SEQUENCE, SEVERITY, SLOT_CASE_NUMBER,
                                     SLOT_COURT_TYPE, SLOT_KNOW_CASE_NUMBER,
                                     SLOT_LOCATION_CODE,
                                     SLOT_REENTER_CASE_NUMBER, USER_EVENT,
                                     UTTER_CASE_CHARGES,
                                     UTTER_DIRECTIONS_FOR_CASE_CHARGES,
                                     UTTER_NO_CASE_CHARGES,
                                     UTTER_NO_VALID_CASE_CHARGES,
                                     UTTER_NOT_APPLICABLE, UTTER_PROBLEM,
                                     VIOLATION_DATE, VIOLATION_DATE_KEY)
from constants.messages import CASE_CHARGE_CUSTOM_JSON
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

api_instance = swagger_client.MyCaseApi()
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get(LOGGER_LEVEL, ERROR))


class ActionFetchCharges(Action):

    def name(self) -> Text:
        return ACTION_FETCH_CHARGES

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info('ACTION_FETCH_CHARGES - Execution started')
        try:
            metadata = None
            for e in tracker.events[::-1]:
                if e[EVENT] == USER_EVENT:
                    metadata = e[METADATA]
                    break
            authorization = metadata[AUTHORIZATION]
            case_number = tracker.get_slot(SLOT_CASE_NUMBER)

            # Skip the Action execution when case_number == -1. Occurs when
            # user entered an incorrect case number and chose not to re-enter
            if case_number != '-1':
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

                # Case details should not be shown to user if case is sealed or
                # expunged
                if case[CASE_SECURITY] == CASE_SECURITY_EXPUNGED or case[CASE_SECURITY] == CASE_SECURITY_SEALED:
                    logger.info(
                        'Expunged / Sealed case identified. Case details not displayed to User')
                    dispatcher.utter_message(response=UTTER_NOT_APPLICABLE)
                else:
                    response = api_instance.get_charges(
                        authorization, case[CASE_NUMBER], case[COURT_TYPE], case[LOCATION_CODE])
                    logger.info(
                        'REST SERVICES - Case Charges response successful')
                    charges = response.to_dict()[DATA]
                    if len(charges):
                        case_charge_custom_json = copy.deepcopy(
                            CASE_CHARGE_CUSTOM_JSON)
                        for charge in charges:
                            case_charge_custom_json[ATTACHMENT][PAYLOAD][ELEMENTS].append({
                                SEQUENCE: EMOJI_HASH + charge[SEQUENCE],
                                OFFENSE: charge[OFFENSE],
                                SEVERITY: EMOJI_FLAG + charge[SEVERITY],
                                VIOLATION_DATE_KEY: EMOJI_CALENDER + charge[VIOLATION_DATE]
                            })
                        dispatcher.utter_message(
                            response=UTTER_CASE_CHARGES,
                            case_number=case[CASE_NUMBER])
                        dispatcher.utter_message(
                            json_message=case_charge_custom_json)
                        dispatcher.utter_message(
                            response=UTTER_NO_VALID_CASE_CHARGES)
                    else:
                        dispatcher.utter_message(
                            response=UTTER_NO_CASE_CHARGES)
                    dispatcher.utter_message(
                        response=UTTER_DIRECTIONS_FOR_CASE_CHARGES)
        except Exception as ex:
            logger.warn(f'Exception occurred in ACTION_FETCH_CHARGES: {ex}')
            dispatcher.utter_message(response=UTTER_PROBLEM)
        finally:
            logger.info('ACTION_FETCH_CHARGES - Execution ended')
            return [
                SlotSet(
                    SLOT_CASE_NUMBER, None), SlotSet(
                    SLOT_COURT_TYPE, None), SlotSet(
                    SLOT_LOCATION_CODE, None), SlotSet(
                    SLOT_KNOW_CASE_NUMBER, None), SlotSet(
                        SLOT_REENTER_CASE_NUMBER, None)]
