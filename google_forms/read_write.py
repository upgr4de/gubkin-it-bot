import socket
import json

from googleapiclient import errors
from .login import login
from pprint import pprint
from data.config import SCRIPT_ID, POLLS_PATH


# Get JSON, which is returned by script
def read_form(form_url):
    socket.setdefaulttimeout(120)

    try:
        pprint('Reading form...')

        body = {
            'function': 'readForm',
            'devMode': True,
            'parameters': form_url
        }
        
        # Get JSON from script
        resp = login().scripts().run(scriptId = SCRIPT_ID, body = body).execute()
        poll_name = resp['response']['result']['metadata']['title']

        if poll_name == 'Контактная информация' or poll_name == 'Связаться с нами':
            poll_name = 'contact'

        # Write out JSON to file
        with open(f'{POLLS_PATH}{poll_name}.json', 'w', encoding = 'utf-8') as poll_file:
            json.dump(resp['response']['result'], poll_file, ensure_ascii = False, indent = 4)

        pprint('Form was successfully read')

        return True, None
    except (errors.HttpError, ) as error:
        # The API encountered a problem.
        pprint(error.content.decode('utf-8'))

        return False, error.content.decode('utf-8')


def write_form(form_url, answers):
    socket.setdefaulttimeout(120)

    try:
        pprint('Writing form...')

        body = {
            'function': 'writeForm',
            'devMode': True,
            'parameters': [form_url, answers]
        }

        login().scripts().run(scriptId = SCRIPT_ID, body = body).execute()

        pprint('Form was successfully wrote')

        return True, None
    except (errors.HttpError, ) as error:
        # The API encountered a problem.
        pprint(error.content.decode('utf-8'))

        return False, error.content.decode('utf-8')
