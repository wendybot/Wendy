from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import requests
import json

def weatherRequest(type, locale):
    payload = {'place': locale}
    
    response = requests.get('http://68.183.43.29:30000/climate', params=payload)
    answer = response.content.decode()
    answer_json = json.loads(answer)
    

    if(type == 'umidade'):
        return 'Neste local, minha umidade é de ' + str(answer_json['humidity']) + '%'
    
    elif(type == 'vento'):
        return 'Neste local, meus ventos sopram para o ' + answer_json["windyDegrees"]+ ' com velocidade de ' +str(answer_json["windySpeed"]) + 'm/s.'
        
    else:
        return answer


class Action_local(Action):
    def name(self):
        return "action_local"

    def run(self, dispatcher, tracker, domain):
        locale = tracker.get_slot('locale')
        type = 'my_peepee_is_hard'
        
        payload = {'address': locale}
        
        response = requests.get('http://68.183.43.29:31170/listLocales', params=payload)
        answer = response.content.decode()
        answer_json = json.loads(answer)
        
        if(len(answer_json) != 1):
            data_message = 'Eu possuo vários locais com esse nome, poderia informar qual destas localizações você deseja?\n\n'
            
            counter = 0
            
            for local in answer_json:
                data_message += str(counter) + '. ' + local['name'] + '\n'
                counter += 1
            
        else:
            if(answer_json[0]['name'] == 'error'):
                data_message = 'Desculpe-me, mas não me recordo de ter criado esse lugar. Talvez me informou erroneamente?'
                
            else:
                data_message = weatherRequest(type, locale)
                
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