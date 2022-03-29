import logging
import os
from typing import Any, Dict, List, Text

from constants.app_constants import (
    ACTION_PROCESS_EVICTION, ACTION_PROCESS_RENT_REJECTION,
    ACTION_PROVIDE_COMMERCIAL_EVICTION_PROCEDURE,
    ACTION_PROVIDE_EVICTION_PROCEDURE, ACTION_PROVIDE_EVICTION_SUMMARY,
    ACTION_RETRIEVE_BELONGINGS, ACTION_RETRIEVE_DEPOSIT,
    ANSWERING_A_COMPLAINT_OR_PETITION_LINK,
    BAD_HOUSING_PAGE_FROM_UTAH_LEGAL_SERVICES_LINK,
    EVICTION_INFORMATION_FOR_LANDLORDS_LINK,
    EVICTION_INFORMATION_FOR_TENANTS_LINK, FINDING_LEGAL_HELP_LINK,
    PROTECTIVE_ORDERS_LINK, REFUNDING_RENTER_DEPOSIT_LINK,
    SELF_HELP_CENTER_LINK, SELF_HELP_HOUSING_LINK,
    TENANT_PERSONAL_PROPERTY_LINK, UTTER_COMMERCIAL_EVICTION_PROCEDURE,
    UTTER_EVICTION_PROCEDURE, UTTER_EVICTION_SUMMARY,
    UTTER_PROCEDURE_TO_RETRIEVE_DEPOSIT, UTTER_PROCESS_EVICTION,
    UTTER_PROCESS_RENT_REJECTION, UTTER_RETRIEVE_BELONGINGS)
from rasa_sdk import Action, Tracker

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGGER_LEVEL', 'ERROR'))


class ActionProvideEvictionSummary(Action):
    def name(self) -> Text:
        return ACTION_PROVIDE_EVICTION_SUMMARY

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        logger.info('ACTION_PROVIDE_EVICTION_SUMMARY - Execution started')
        dispatcher.utter_message(
            response=UTTER_EVICTION_SUMMARY,
            self_help_housing_link=SELF_HELP_HOUSING_LINK,
            protective_orders_link=PROTECTIVE_ORDERS_LINK,
            eviction_information_for_landlords_link=EVICTION_INFORMATION_FOR_LANDLORDS_LINK,
            eviction_information_for_tenants_link=EVICTION_INFORMATION_FOR_TENANTS_LINK,
            bad_housing_page_from_utah_legal_services_link=BAD_HOUSING_PAGE_FROM_UTAH_LEGAL_SERVICES_LINK,
            answering_a_complaint_or_petition_link=ANSWERING_A_COMPLAINT_OR_PETITION_LINK,
            tenant_personal_property_link=TENANT_PERSONAL_PROPERTY_LINK,
            refunding_renter_deposit_link=REFUNDING_RENTER_DEPOSIT_LINK,
            finding_legal_help_link=FINDING_LEGAL_HELP_LINK,
            self_help_center_link=SELF_HELP_CENTER_LINK)
        logger.info('ACTION_PROVIDE_EVICTION_SUMMARY - Execution ended')
        return []


class ActionProvideEvictionProcedure(Action):
    def name(self) -> Text:
        return ACTION_PROVIDE_EVICTION_PROCEDURE

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        logger.info('ACTION_PROVIDE_EVICTION_PROCEDURE - Execution started')

        dispatcher.utter_message(
            response=UTTER_EVICTION_PROCEDURE,
            protective_orders_link=PROTECTIVE_ORDERS_LINK,
            eviction_information_for_landlords_link=EVICTION_INFORMATION_FOR_LANDLORDS_LINK,
            self_help_center_link=SELF_HELP_CENTER_LINK)
        logger.info('ACTION_PROVIDE_EVICTION_PROCEDURE- Execution ended')
        return []


class ActionProcessEviction(Action):
    def name(self) -> Text:
        return ACTION_PROCESS_EVICTION

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        logger.info('ACTION_PROCESS_EVICTION - Execution started')

        dispatcher.utter_message(
            response=UTTER_PROCESS_EVICTION,
            eviction_information_for_tenants_link=EVICTION_INFORMATION_FOR_TENANTS_LINK,
            bad_housing_page_from_utah_legal_services_link=BAD_HOUSING_PAGE_FROM_UTAH_LEGAL_SERVICES_LINK,
            answering_a_complaint_or_petition_link=ANSWERING_A_COMPLAINT_OR_PETITION_LINK,
            self_help_center_link=SELF_HELP_CENTER_LINK)
        logger.info('ACTION_PROCESS_EVICTION- Execution ended')
        return []


class ActionRetrieveBelongings(Action):
    def name(self) -> Text:
        return ACTION_RETRIEVE_BELONGINGS

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        logger.info('ACTION_RETRIEVE_BELONGINGS - Execution started')

        dispatcher.utter_message(
            response=UTTER_RETRIEVE_BELONGINGS,
            tenant_personal_property_link=TENANT_PERSONAL_PROPERTY_LINK,
            self_help_center_link=SELF_HELP_CENTER_LINK)
        logger.info('ACTION_RETRIEVE_BELONGINGS- Execution ended')
        return []


class ActionProcessRentRejection(Action):
    def name(self) -> Text:
        return ACTION_PROCESS_RENT_REJECTION

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        logger.info('ACTION_PROCESS_RENT_REJECTION - Execution started')

        dispatcher.utter_message(response=UTTER_PROCESS_RENT_REJECTION)
        logger.info('ACTION_PROCESS_RENT_REJECTION- Execution ended')
        return []


class ActionRetrieveDeposit(Action):
    def name(self) -> Text:
        return ACTION_RETRIEVE_DEPOSIT

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        logger.info('ACTION_RETRIEVE_DEPOSIT - Execution started')

        dispatcher.utter_message(
            response=UTTER_PROCEDURE_TO_RETRIEVE_DEPOSIT,
            refunding_renter_deposit_link=REFUNDING_RENTER_DEPOSIT_LINK,
        )
        logger.info('ACTION_RETRIEVE_DEPOSIT- Execution ended')
        return []


class ActionProvideCommercialEvictionProcedure(Action):
    def name(self) -> Text:
        return ACTION_PROVIDE_COMMERCIAL_EVICTION_PROCEDURE

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        logger.info(
            'ACTION_PROVIDE_COMMERCIAL_EVICTION_PROCEDURE - Execution started')

        dispatcher.utter_message(
            response=UTTER_COMMERCIAL_EVICTION_PROCEDURE,
            finding_legal_help_link=FINDING_LEGAL_HELP_LINK,
        )

        logger.info(
            'ACTION_PROVIDE_COMMERCIAL_EVICTION_PROCEDURE- Execution ended')
        return []
