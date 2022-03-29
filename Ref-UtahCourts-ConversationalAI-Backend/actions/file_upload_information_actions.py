import logging
import os
from typing import Any, Dict, List, Text

from client import swagger_client
from constants.app_constants import (ACTION_FETCH_FILE_UPLOAD_INFORMATION,
                                     AUTHORIZATION, CASE_NUMBER, CASE_SECURITY,
                                     CASE_SECURITY_EXPUNGED,
                                     CASE_SECURITY_SEALED, COURT_TYPE, DATA,
                                     DISTRICT_COURT_CODE,
                                     DOCUMENT_FILING_INSTRUCTIONS_LINK, ERROR,
                                     EVENT, FILL_OUT_FORM_URL,
                                     GUIDED_INTERVIEW_URL, JUSTICE_COURT,
                                     JUSTICE_COURT_CODE, LOCATION_CODE,
                                     LOGGER_LEVEL, METADATA, SLOT_CASE_NUMBER,
                                     SLOT_COURT_TYPE, SLOT_KNOW_CASE_NUMBER,
                                     SLOT_LOCATION_CODE,
                                     SLOT_REENTER_CASE_NUMBER, USER_EVENT,
                                     UTTER_FILE_UPLOAD_INFORMATION,
                                     UTTER_NO_FILE_UPLOAD_INFORMATION,
                                     UTTER_NOT_APPLICABLE, UTTER_PROBLEM)
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

api_instance = swagger_client.MyCaseApi()
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get(LOGGER_LEVEL, ERROR))


class ActionFetchFileUploadInformation(Action):

    def name(self) -> Text:
        return ACTION_FETCH_FILE_UPLOAD_INFORMATION

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info('ACTION_FETCH_FILE_UPLOAD_INFORMATION - Execution started')
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
                    response = api_instance.get_document_upload_urls(
                        authorization, case[CASE_NUMBER], case[COURT_TYPE], case[LOCATION_CODE])
                    logger.info(
                        'REST SERVICES - document upload URLs response successful')
                    document_upload_urls = response.to_dict()[DATA]
                    if document_upload_urls[FILL_OUT_FORM_URL] and document_upload_urls[GUIDED_INTERVIEW_URL]:
                        dispatcher.utter_message(
                            response=UTTER_FILE_UPLOAD_INFORMATION,
                            case_number=case[CASE_NUMBER],
                            fill_out_form_link=document_upload_urls[FILL_OUT_FORM_URL],
                            guided_interview_link=document_upload_urls[GUIDED_INTERVIEW_URL])
                    else:
                        dispatcher.utter_message(
                            response=UTTER_NO_FILE_UPLOAD_INFORMATION,
                            document_filing_instructions_link=DOCUMENT_FILING_INSTRUCTIONS_LINK)
        except Exception as ex:
            logger.warn(
                f'Exception occurred in ACTION_FETCH_FILE_UPLOAD_INFORMATION: {ex}')
            dispatcher.utter_message(response=UTTER_PROBLEM)
        finally:
            logger.info(
                'ACTION_FETCH_FILE_UPLOAD_INFORMATION - Execution ended')
            return [
                SlotSet(
                    SLOT_CASE_NUMBER, None), SlotSet(
                    SLOT_COURT_TYPE, None), SlotSet(
                    SLOT_LOCATION_CODE, None), SlotSet(
                    SLOT_KNOW_CASE_NUMBER, None), SlotSet(
                        SLOT_REENTER_CASE_NUMBER, None)]
