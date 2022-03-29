import copy
import logging
import os
import time
from typing import Any, Dict, List, Text

from client import swagger_client
from constants.app_constants import (ACTION, ACTION_FETCH_PAYMENT, ATTACHMENT,
                                     AUTHORIZATION, CASE_NUMBER, CASE_SECURITY,
                                     CASE_SECURITY_EXPUNGED,
                                     CASE_SECURITY_SEALED, COURT_TYPE, DATA,
                                     DISTRICT_COURT_CODE, ELEMENTS,
                                     EPAY_AMOUNT, EPAY_PARTY, EPAY_WEB_USER,
                                     ERROR, EVENT, FORM,
                                     FORM_INPUT_NAME_EPAY_AMOUNT,
                                     FORM_INPUT_NAME_EPAY_COURT_TYPE,
                                     FORM_INPUT_NAME_EPAY_INT_CASE_NUMBER,
                                     FORM_INPUT_NAME_EPAY_PARTY,
                                     FORM_INPUT_NAME_EPAY_WEB_USER, ID,
                                     INT_CASE_NUMBER, JUSTICE_COURT,
                                     JUSTICE_COURT_CODE, LOCATION_CODE,
                                     LOGGER_LEVEL, METADATA, MYCASE_BASE_PATH,
                                     PAYLOAD, PAYMENT_URL, SLOT_CASE_NUMBER,
                                     SLOT_COURT_TYPE, SLOT_KNOW_CASE_NUMBER,
                                     SLOT_LOCATION_CODE,
                                     SLOT_REENTER_CASE_NUMBER, TEXT,
                                     USER_EVENT, UTTER_FIND_CASE_PAYMENT,
                                     UTTER_NO_CASE_PAYMENT,
                                     UTTER_NOT_APPLICABLE, UTTER_PROBLEM)
from constants.messages import CASE_PAYMENT_CUSTOM_JSON
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

api_instance = swagger_client.MyCaseApi()
MYCASE_BASE_PATH = os.getenv(MYCASE_BASE_PATH)

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get(LOGGER_LEVEL, ERROR))


class ActionFetchPayment(Action):

    def name(self) -> Text:
        return ACTION_FETCH_PAYMENT

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info('ACTION_FETCH_PAYMENT - Execution started')

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
                    response = api_instance.get_payment_information(
                        authorization, case[CASE_NUMBER], case[COURT_TYPE], case[LOCATION_CODE])
                    logger.info(
                        'REST SERVICES - Case Payment response successful')
                    payment_information = response.to_dict()[DATA]
                    if payment_information and payment_information[EPAY_AMOUNT] is not None and float(
                            payment_information[EPAY_AMOUNT]) != 0:
                        case_payment_custom_json = copy.deepcopy(
                            CASE_PAYMENT_CUSTOM_JSON)
                        case_payment_custom_json[ATTACHMENT][PAYLOAD][FORM][ACTION] = MYCASE_BASE_PATH + PAYMENT_URL
                        case_payment_custom_json[ATTACHMENT][PAYLOAD][FORM][ID] = case_payment_custom_json[ATTACHMENT][PAYLOAD][FORM][ID].format(
                            timestamp=int(time.time()))
                        case_payment_custom_json[ATTACHMENT][PAYLOAD][TEXT] = case_payment_custom_json[ATTACHMENT][PAYLOAD][TEXT].format(
                            epay_amount=payment_information[EPAY_AMOUNT], case_number=case_number)

                        elements = case_payment_custom_json[ATTACHMENT][PAYLOAD][FORM][ELEMENTS]
                        elements.append({'name': FORM_INPUT_NAME_EPAY_INT_CASE_NUMBER,
                                        'value': payment_information[INT_CASE_NUMBER]})
                        elements.append(
                            {'name': FORM_INPUT_NAME_EPAY_COURT_TYPE, 'value': payment_information[COURT_TYPE]})
                        elements.append(
                            {'name': FORM_INPUT_NAME_EPAY_WEB_USER, 'value': payment_information[EPAY_WEB_USER]})
                        elements.append(
                            {'name': FORM_INPUT_NAME_EPAY_AMOUNT, 'value': payment_information[EPAY_AMOUNT]})
                        elements.append(
                            {'name': FORM_INPUT_NAME_EPAY_PARTY, 'value': payment_information[EPAY_PARTY]})
                        dispatcher.utter_message(
                            json_message=case_payment_custom_json)
                        dispatcher.utter_message(
                            response=UTTER_FIND_CASE_PAYMENT)
                    else:
                        dispatcher.utter_message(
                            response=UTTER_NO_CASE_PAYMENT)
                        dispatcher.utter_message(
                            response=UTTER_FIND_CASE_PAYMENT)
        except Exception as ex:
            logger.warn(f'Exception occurred in ACTION_FETCH_PAYMENT: {ex}')
            dispatcher.utter_message(response=UTTER_PROBLEM)
        finally:
            logger.info('ACTION_FETCH_PAYMENT - Execution ended')
            return [
                SlotSet(
                    SLOT_CASE_NUMBER, None), SlotSet(
                    SLOT_COURT_TYPE, None), SlotSet(
                    SLOT_LOCATION_CODE, None), SlotSet(
                    SLOT_KNOW_CASE_NUMBER, None), SlotSet(
                        SLOT_REENTER_CASE_NUMBER, None)]
