from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from .utils import localRequest
import requests
import random
import json

class Action_sports(Action):
    def name(self):
        return "action_sports"

    def run(self, dispatcher, tracker, domain):
        locale = tracker.get_slot('locale')
        choice = tracker.get_slot('choice')
        location = localRequest(locale, choice)
        payload = {'place': location}
        response = requests.get('http://68.183.43.29:30000/sports', params=payload)
        content = response.content.decode()
        answer = json.loads(content)
        data_loc = locale.capitalize()+':'
        try:
            dispatcher.utter_message(data_loc)
            if(len(answer["favorable"]) > 0):
                data_sport = 'Para as condições atuais, recomendo: '
                for favorable in answer["favorable"]:
                    data_sport += '\n' + favorable["name"].capitalize()
                dispatcher.utter_message(data_sport)
            elif(len(answer["reservation"]) > 0):
                data_reservation = 'Caso queira, algumas condições favorecem: '
                for reservation in answer["reservation"]:
                    data_reservation += '\n' + reservation["name"].capitalize()
                dispatcher.utter_message(data_reservation)
            elif(len(answer["alert"]) > 0):
                data_alert = 'Poucas condições favorecem: '
                for alert in answer["alert"]:
                    data_alert += '\n' + alert["name"].capitalize()
                dispatcher.utter_message(data_alert)
        except ValueError:
            dispatcher.utter_message(ValueError)