# Gubkin-it Bot

<p align="center">
    <img src="https://github.com/upgr4de/gubkin-it-bot/blob/master/logo.png">
</p>

## Telegram bot for take a surveys using Google Apps Script API

The basis of the project's structure was taken from here https://github.com/Latand/aiogram-bot-template (it is explained here https://www.youtube.com/watch?v=fob8oQOjB2Q&list=PLwVBSkoL97Q3phZRyInbM4lShvS1cBl-U&index=5&ab_channel=PhysicsisSimple)

You should study work with Google API, for example here https://habr.com/ru/post/485898/

The following commands are used in the chatbot:
* /start - start the chat and greet the chatbot
* /help
* /polls - list of polls. Through the /polls command, users will be able to select a poll from the list and go through it, step by step answering the questions, as well as edit the answers. After passing the survey, the responses will be sent as a list (list in Python is an ordered mutable collection of objects of arbitrary types) to Google Forms
* /contact - contact us form. The /contact command will have the same meaning (as /polls), but will immediately transfer the user to the poll to contact the administrators
* /cancel
* /admins command, which can only be used by chatbot administrators. Through the /admins command, it will be possible to download forms from the Google Forms service and add them to the general list of polls by inserting a link to the form, as well as delete unnecessary polls from this list. The form will be loaded as a JSON file and stored on the server

First, you need to create a chatbot project folder (in this case - gubkin_it_bot). Then you need to configure the Google project (page 1 - Google Apps Script home page https://script.google.com/home, page 2 - Google Cloud Platform (Console) home page https://console.cloud.google.com/home):
- go to page 2, create a new project
- return to page 2, go to the "API and services" tab, then to the "OAuth consent screen" and set the "User Type" to "External
- In the window that appears, fill in "App name" (in this case, gFormsRW)
- return to page 2 and copy the "Project number" from the "Project info" block
- go to page 1, click "Create Project" and give it a name (in this case, gFormsRW)
- write the script in this project (pic.2.1): the writeForm function writes answers (the answers variable) as a list into Google Forms, the form_url variable is the address of a Google form like https://docs.../edit, the readForm function returns the result (the result variable) into JSON, the getFormMetadata function returns the form metadata into JSON, the itemToObject function converts form.item into an object and returns the result (the data variable) with the requested fields into JSON
- test the script by replacing the input parameters of writeForm and readForm functions with global ones, assigning values to them and displaying the result (result variable in readForm function) on the console
- go to "Project Settings", click on "Change Project Type" and enter the copied "Project number" in the field; now the project in Google Apps Script is associated with the Google Cloud Platform (Console) project
- open page 2, go to "API and services", then to "Credentials" and click on "Create credentials", then to "OAuth client ID" and choose the "Application type" value "Desktop app", fill the "Name" (in this case - Desktop client 1), click on "Create", close the window, in the line with the created OAuth 2. 0 Client ID click on the download button to download the JSON file, this will download the key file for access to the project in Google Cloud Platform (Console), it should be renamed (in this case - desktop_client_1.json) and placed in the folder google_forms/credentials/
- permit the Google Apps Script API within the Google Cloud Platform (Console) project by going to "APIs and services", then to "Library" and typing "Apps Script API", selecting and clicking on "Enable
- go to page 1, click on the project created earlier, then click on "General", at the bottom of the page in the "Scopes of OAuth for the project" field copy the scopes (e.g. https://www.googleapis.com/auth/forms) and save them (they will be used in the scopes variable as a list)
- proceed to page 1, click on the project created earlier, click on "Project Settings", copy "Script ID" into the "Identifiers" field and save it (it will be used in the SCRIPT_ID environment variable)
- go to page 1, click on "Settings" and then on "Google Apps API Script" and then on the enable button

To develop a chatbot, a system (structure) of files and folders is used, which is necessary for the versatility of the project, easy orientation in it and scaling of the bots:

gubkin_it_bot/<br>
├── data/<br>
│   ├── polls/<br>
│   ├──__ init__.py<br>
│   └── config.py<br>
├── env/<br>
├── filters/<br>
├── google_forms/<br>
│   ├── credentials/<br>
│   │   ├── desktop_client_1.json<br>
│   ├── __init__.py<br>
│   ├── login.py<br>
│   └── read_write.py<br>
├── handlers/<br>
│   ├── channels/<br>
│   ├── errors/<br>
│   │   ├── __init__.py<br>
│   │   ├── exceptions.py<br>
│   ├── groups/<br>
│   ├── users/<br>
│   │   ├── __init__.py<br>
│   │   ├── admins.py<br>
│   │   ├── cancel.py<br>
│   │   ├── help.py<br>
│   │   ├── polls.py<br>
│   │   └── start.py<br>
│   └── __init__.py<br>
├── keyboards/<br>
│   ├── inline/<br>
│   │   ├── __init__.py<br>
│   │   ├── admins_ki.py<br>
│   │   ├── callback_data.py<br>
│   │   └── polls_ki.py<br>
│   ├── reply/<br>
│   │   ├── __init__.py<br>
│   │   └── polls_kr.py<br>
│   └── __init__.py<br>
├── middlewares/<br>
│   ├── __init__.py<br>
│   └── throttling.py<br>
├── states/<br>
│   ├── __init__.py<br>
│   ├── admins_s.py<br>
│   └── polls_s.py<br>
├── utils/<br>
│   ├── db_api/<br>
│   ├── misc/<br>
│   │   ├── __init__.py<br>
│   │   ├── logging.py<br>
│   │   └── throttling.py<br>
│   ├── __init__.py<br>
│   └── notify_admins.py<br>
├── .env<br>
├── .gitignore<br>
├── bot.py<br>
├── loader.py<br>
├── Procfile<br>
├── README.md<br>
├── requirements.txt<br>
└── runtime.txt

Consider these files and folders:
- bot.py is the main file where the program code for launching the chat bot is written, which also specifies the method for receiving updates (in this case, long polling)
- loader.py - a file in which the program code is written to load the necessary variables: bot - requests for Telegram Bot API methods, storage - FSM memory type, dp - update manager
- Procfile - a file (for Heroku) that stores information about which main file to run (if the bot is on webhooks, you need to replace bot with web), but on a free plan, the bot will fall asleep every 30 minutes if it is not active (when this will erase the data), so that the bot does not fall asleep, you can use the Kaffeine service http://kaffeine.herokuapp.com/
- README.md - a file (for GitHub) that stores information about the project and how to use it
- requirements.txt - a file that stores information about the project's dependencies
- runtime.txt - a file that stores information about the programming language (and its version) in which the entire project is written. It contains:<br>
- .env - a file that stores information about environment variables (BOT_TOKEN - the chat bot token received during its registration, ADMINS - ID of bot administrators in Telegram separated by commas, SCRIPT_ID - script ID from Google Apps Script)
- .gitignore - a file (for GitHub and Heroku) that stores information about which files to ignore and not upload to the repository
- data/ – folder for project data
- data/polls/ - folder for Google Forms poll files (in JSON)
- data/config.py - a file in which the program code is written to load environment variables from the .env file
- env/ - folder for virtual environment (ignored for GitHub and Heroku), which allows you to use the entire project folder as an isolated environment environment so that all dependencies of libraries, frameworks and their versions do not go beyond this environment, which allows you to use the project on systems with different set of these libraries and frameworks
- filters/ - folder for filters that direct updates (messages from the user) to given functions
- google_forms/ - folder for working with Google Forms
- google_forms/credentials/ - folder for project access keys in Google Apps Script
- google_forms/login.py - a file in which the program code for authorization in the Google Apps Script API is written
- google_forms/read_write.py - a file in which the program code is written for loading Google Forms survey files (in JSON) and uploading a list (list) of answers to Google Forms
- handlers/ - folder for handlers (functions that handle certain events for which they are registered)
- handlers/channels/ – folder for update handlers in channels
- handlers/errors/ – folder for error handlers
-handlers/errors/init.py \*
- handlers/errors/exceptions.py - a file in which the program code for the exception handler is written
- handlers/groups/ – folder for update handlers in a group chat
- handlers/users/ – folder for update handlers in private chat
-handlers/users/init.py \*
- handlers/users/admins.py - a file that contains the program code for the /admins command handlers, the "Load", "Delete" buttons, and polls to delete
- handlers/users/cancel.py - a file in which the program code for the /cancel command handlers and the "Cancel" button is written
- handlers/users/help.py - a file in which the program code is written for the handlers of the /help command and unaccepted messages from the user
- handlers/users/polls.py - a file in which the program code is written for the /contact and /polls command handlers, poll buttons for passing and poll questions
- handlers/users/start.py - a file in which the program code for the /start command handler is written
- handlers/init.py \*
- keyboards/ - folder for custom keyboards
- keyboards/inline/ – folder for inline keyboards (in the message)
- keyboards/inline/admins_ki.py - a file in which the program code for the keyboard is written with the buttons "Load", "Delete" and "Cancel"
- keyboards/inline/callback_data.py - a file in which the program code is written to store callback data after pressing a keyboard button
- keyboards/inline/polls_ki.py - a file in which the program code for the keyboard with poll buttons for passing is written
- keyboards/reply/ - folder for regular keyboards (under the input field)
- keyboards/reply/polls_kr.py - a file that contains the program code for a keyboard with buttons "Great! Start, Skip, and End
- middlewares/ - a folder for middleware that performs interaction between various components (in this case, between the "deliverer" of updates and handlers)
- middlewares/init.py \*
- middlewares/throttling.py - a file in which the program code for throttling is written, that is, a mechanism for skipping a part of machine cycles (cycles) in order to synchronize the work of various components, it does not allow the same handler to be executed many times
- states/ – folder for FSM states
- states/admins_s.py - the file in which the program code for the state of the question is written when loading surveys
- states/polls_s.py - the file in which the program code for the states of the poll questions is written
- utils/ - folder for utilities, that is, utility programs that facilitate the use of other programs
- utils/db_api/ – folder for database utilities
- utils/misc/ – folder for various utilities
- utils/misc/logging.py - a file in which the program code for the logging utility is written, that is, recording the actions of programs during operation
- utils/misc/throttling.py - a file in which the program code for the throttling utility is written
- utils/notify_admins.py - a file in which the program code is written to send notifications to administrators about the start and stop of the bot

\* The code in the init.py file causes Python to treat the directories containing it as modules, and it's also the first file loaded into a module, so it can be used to execute code each time a module is loaded, or specify submodules to export
