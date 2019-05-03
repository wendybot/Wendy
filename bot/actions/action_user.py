from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import requests
import random
import json

class User_Action(Action):
    def name(self):
        return "action_user"

    def run(self, dispatcher, tracker, domain):

    tracker_state = tracker.current_state()
    sender_id = tracker_state['sender_id']
    user_local = tracker.get_slot('user_local')
    user_sport = tracker.get_slot('user_sport')
    user_day = tracker.get_slot('user_day')
    user_time = tracker.get_slot('user_time')

    dataJson = {	
        "telegramId": sender_id,
	    "sport": user_sport,
	    "notificationDays": user_day,
	    "notificationTime": user_time,
	    "local": user_local
        }

    response = requests.post('localhost:3003/registerUser', data = dataJson)


