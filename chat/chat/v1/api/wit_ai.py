from http import HTTPStatus
import requests

from .reply import *
from .secrets import *

WIT_RESPONSE_ERROR_REPLY = "Sorry, I use wit to process your intent but wit has error right now."
INTENT_NOT_PROGRAMMED_REPLY = "Sorry, I understand your intent but I am not programmed to respond to this intent."
WIT_CAN_NOT_MATCH_REPLY = "Sorry, I can not understand your intent from my training."


def get_reply(message):
    """Return the reply of a given message after processing."""
    url = f'https://api.wit.ai/message?v={WIT_DATETIME}&q={message}'
    headers = {'Authorization': WIT_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code != HTTPStatus.OK:
        return WIT_RESPONSE_ERROR_REPLY
    jsonResponse = response.json()
    try:
        if jsonResponse['intents'][0]['name'] == "getDentists":
            return DentistsReply().get_reply()
        elif jsonResponse['intents'][0]['name'] == "getDentistInformation":
            name = jsonResponse['entities']['dentist:dentist'][0]['body']
            return DentistInformationReply(name).get_reply()
        elif jsonResponse['intents'][0]['name'] == "getDentistAvailableTimeslots":
            name = jsonResponse['entities']['dentist:dentist'][0]['body']
            return DentistAvailableTimeslotReply(name).get_reply()
        elif jsonResponse['intents'][0]['name'] == "updateTimeslot":
            name = jsonResponse['entities']['dentist:dentist'][0]['body'] or ''
            action = jsonResponse['entities']['action:action'][0]['body'] or ''
            # Get hour 13 -> 13, 09 -> 9
            startTime = jsonResponse['entities']['wit$datetime:datetime'][0]['value'][11:13].lstrip('0') or ''
            return UpdateTimeslotReply(name, action, startTime).get_reply()
        return INTENT_NOT_PROGRAMMED_REPLY
    except:
        return WIT_CAN_NOT_MATCH_REPLY
