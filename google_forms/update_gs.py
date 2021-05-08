import json

from googleapiclient import errors
from .login import login
from pprint import pprint
from data.config import SCRIPT_ID, GOOGLE_FORMS_PATH


MANIFEST = '''
{
    "timeZone": "Europe/Moscow",
    "exceptionLogging": "STACKDRIVER",
    "executionApi": {
        "access": "ANYONE"
    }
}
'''.strip()


def update_project(gs_name):
    try:        
        # Read from file code we want to deploy
        with open(f'{GOOGLE_FORMS_PATH}{gs_name}.gs', 'r') as gs_file:
            sample_code = gs_file.read()

        # Upload two files to the project
        request = {
            'files': [{
                'name': 'gFormsRW',
                'type': 'SERVER_JS',
                'source': sample_code
            }, {
                'name': 'appsscript',
                'type': 'JSON',
                'source': MANIFEST
            }]
        }

        # Update files in the project
        login().projects().updateContent(
            body = request,
            scriptId = SCRIPT_ID
        ).execute()

        pprint('Project was successfully updated')

        return True, None
    except (errors.HttpError, ) as error:
        # The API encountered a problem.
        pprint(error.content.decode('utf-8'))

        return False, error.content.decode('utf-8')
