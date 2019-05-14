from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from typing import List
import requests
import random
import json
import os

class User_Action(Action):
    def name(self):
        return "action_user"

    def run(self, dispatcher, tracker, domain):
        tracker_state = tracker.current_state()
        sender_id = tracker_state['sender_id']
        user_local = tracker.get_slot('user_locale')
        local_user = ''.join(user_local)
        user_sport = tracker.get_slot('user_sport')
        sport_user = ''.join(user_sport)
        user_day = tracker.get_slot('user_day')
        day_user = ''.join(user_day)
        user_hour = tracker.get_slot('user_hour')
        user_minute = tracker.get_slot('user_minute')

        # dataJson = {	
        #     "telegramId": sender_id,
        #     "sport": [user_sport],
        #     "days": [user_day],
        #     "times": [ { user_hour, user_minute }],
        #     "local": [user_local]
        #     }
        # dispatcher.utter_message(sender_id)
        dispatcher.utter_message(local_user)
        dispatcher.utter_message(sport_user)
        dispatcher.utter_message(day_user)
        # dispatcher.utter_message(user_hour)
        # dispatcher.utter_message(user_minute)


        # response = requests.post('http://'+ip_address+':3003/createNotification', data = dataJson)