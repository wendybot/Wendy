from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from .utils import sportsRequest, specificSportRequest, weatherRequest
import requests
import json

class Action_local(Action):
    def name(self):
        return "action_local"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent'].get('name')
        locale = tracker.get_slot('locale')
        sport = tracker.get_slot('sport')
        type_ = tracker.get_slot('type')
        
        payload = {'address': locale}
        
        response = requests.get('http://68.183.43.29:31170/listLocales', params=payload)
        answer = response.content.decode()
        answer_json = json.loads(answer)
        
        if(len(answer_json) != 1):
            data_message = 'Eu possuo vários locais com esse nome, poderia informar qual o número da localidade que deseja?\n\n'
            
            counter = 1
            
            for local in answer_json:
                data_message += str(counter) + '. ' + local['name'] + '\n'
                counter += 1
                if counter == 6:
                    break
            
        else:
            if(answer_json[0]['name'] == 'error'):
                data_message = 'Desculpe-me, mas não me recordo de ter criado esse lugar. Talvez me informou erroneamente?'
                
            else:
                if(intent == 'sports'):
                    data_message = sportsRequest(locale)
                elif(intent == 'specific_sport'):
                    data_message = specificSportRequest(locale, sport)
                else:
                    data_message = weatherRequest(type_, locale)
                
        try:
            if(data_message[:1] != '{'):
                dispatcher.utter_message(data_message)
                
            else:
                data_message_json = json.loads(data_message)
                
                dispatcher.utter_message(locale.capitalize() + ':')
                dispatcher.utter_message('Neste local, minha temperatura é ' + data_message_json["temperature"]+'°C,')
                dispatcher.utter_message('com umidade de ' + str(data_message_json["humidity"])+'%, ')
                dispatcher.utter_message('e pressão ' + data_message_json["pressure"]+' atm. ')
                dispatcher.utter_message('Meus ventos sopram para ' + data_message_json["windyDegrees"]+',')
                dispatcher.utter_message(' com velocidade de ' + str(data_message_json["windySpeed"])+' m/s,')
                dispatcher.utter_message(' e apresento ' + data_message_json["sky"]+'.')
                dispatcher.utter_message('O sol me ilumina de ' + data_message_json["sunrise"])
                dispatcher.utter_message('às ' + data_message_json["sunset"] + '.')
            
        except ValueError:
            dispatcher.utter_message(ValueError)
    
        return [SlotSet('type', None)]