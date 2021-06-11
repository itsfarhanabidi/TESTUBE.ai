Welcome to the AI Nurse Folder. This folder has all the files necessary to build an AI chatbot which performs a symptomatic analysis for the patient to analyse whether the patient 
has Tuberculosis or not. The chatbot is built with the help of an open source AI framework called RASA that helps in building conversational chatbots easily.


The description of the files is as follows:
  - Config.yml: This is a file that showcases the policies and pipelines used by the chatbot for its operation.
  - Credentials.yml: This file gives information about the various platforms with which the chatbot can be linked. The major requirement to use this fodler is any API which
    can be used with the chatbot. For example, in this project, Twilio functions as the API such that people can communicate with the chatbot on Whatsapp.
  - Domain.yml: This file contains all the inputs from the user as well the actions(responses) of the chatbot to the user's input.
  - Endpoints.yml: A file showcasing different endpoints that the chatbot can use for its operation.
  - NLU.yml: This is the file which contains all the user inputs that the chatbot can be trained on such that it can reply to the input efficiently.
  - Rules.yml: This file highlights the different rules that the chatbot functions on.
  - Stories.yml: This file depicts the conversational flow for any given testcase between the user and chatbot.
