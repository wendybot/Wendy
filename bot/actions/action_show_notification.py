from rasa_core_sdk import Action
from .environment import configSport
import requests
import json
from .utils import convertDay


class Action_show_notification(Action):
    def name(self):
        return "action_show_notification"

    def run(self, dispatcher, tracker, domain):
        URL = configSport()
        tracker_state = tracker.current_state()
        sender_id = tracker_state['sender_id']
        payload = {"id": sender_id}
    
        response = requests.get(URL+'/userNotification', params = payload)
        answer = response.content.decode()
        answerJson = json.loads(answer)
        json_counter = 0
        try: 
            if(len(answerJson) > 0):
                for notification in answerJson:
                    json_counter+=1
                    data_message = 'Notificação ' + str(json_counter) + ':\n'
                    data_message+= 'Esporte:' + notification["sport"].title() + '\n'
                    if(len(notification["locals"]) > 0):
                        for locales in notification["locals"]:
                            data_message+= 'Local: ' + locales.title() + '\n'
                    if (len(str(notification["hour"])) < 2):
                        data_message+= 'Horário: 0' + str(notification["hour"]) 
                    else:
                        data_message+= 'Horário: ' + str(notification["hour"]) 
                    if (len(str(notification["minutes"])) < 2):
                        data_message+= ':0' + str(notification["minutes"]) + '\n'
                    else:
                        data_message+= ':' + str(notification["minutes"]) + '\n'
                    if(len(notification["days"]) > 0):
                        for days in notification["days"]:
                            day = convertDay(days)
                            data_message+= 'Dia(s) da semana: ' + day + '\n'
                    data_message+= 'Notificado(a) ' + str(notification["hoursBefore"]) + ' horas e ' + str(notification["minutesBefore"]) + ' minutos antes.\n'
                    dispatcher.utter_message(data_message)
        except ValueError:
            dispatcher.utter_message("Não foi possível exibir suas notificações")