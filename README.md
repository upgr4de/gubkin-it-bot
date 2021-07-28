# Telegram bot for take a surveys using Google Apps Script API
The basis of the project's structure was taken from here https://github.com/Latand/aiogram-bot-template (it is explained here https://www.youtube.com/watch?v=fob8oQOjB2Q&list=PLwVBSkoL97Q3phZRyInbM4lShvS1cBl-U&index=5&ab_channel=PhysicsisSimple)

You should study work with Google API, for example, here https://habr.com/ru/post/485898/, here https://developers.google.com/apps-script/overview and here https://cloud.google.com/docs/overview

The following commands will be used in the chatbot: /start - start the chat and greet the chatbot, /help - help, /polls - list of polls, /contact - contact us, /cancel - cancel. And also the /admins command, which can only be used by chatbot administrators.

Through the /admins command, it will be possible to download forms from the Google Forms service and add them to the general list of polls by inserting a link to the form, as well as delete unnecessary polls from this list. The form will be loaded as a JSON file and stored on the server.

Through the /polls command, users will be able to select a poll from the list and go through it, step by step answering the questions, as well as edit the answers. After passing the survey, the responses will be sent as a list (list in Python is an ordered mutable collection of objects of arbitrary types) to Google Forms. The /contact command will have the same meaning, but will immediately transfer the user to the poll to contact the administrators.
