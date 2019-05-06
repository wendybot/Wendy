from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from .utils import localRequest, specificSportRequest
import requests
import json


class Action_specific_sport(Action):
    def name(self):
        return "action_specific_sport"

    def run(self, dispatcher, tracker, domain):
        locale = tracker.get_slot('locale')
        choice = tracker.get_slot('choice')
        sport = tracker.get_slot('sport')

        location = localRequest(locale, choice)

        data_message = specificSportRequest(location, sport)

        dispatcher.utter_message(data_message)
