# Mandrill_Events_Listener

The "main" directory in the "Mandrill_Event_Listener", have 5 python files:
     - app.py has all the necessary endpoints and the application logic 
     - database_manager.py is used as a module from which a class is imported in app.py for data base functionalities
     - web_socket_manager.py is used as a module from which a class is imported in app.py for web socket functionalities
     - webhook_manager.py is used as module from which a class is imported in app.py for webhook functionalities
     - test_.py is a test file using pytest to test the mandrill event listening functionality at the defined end point by hitting the endpoint   using dummy payloads

The "static" foleder contains the css and javascript files

The "templates" folder contains the index.html file

The errors are logged into a "errors.log" file

Steps to run the application:
      Navigate to 'Mandrill_Event_Listener' directory

      Run the command "pip install -r requirements.txt"

      Run the command "python -m uvicorn main.app:app --reload" to launch the uvicorn server

      Navigate to "http://127.0.0.1:8000" to use the app


Notes:

The front end has a text field to input a webhook url for Mandrill. Clicking the "Add WebHook" button adds the new webhook. If no webhook url is entered, the default webhook in the code is used.

The success message when a web hook is added, or if there has been any error is displayed on the dash board. 

The front end communicates with the backend over a web socket connection which is opened whenever the app is launched and the user clicks anywhere on the screen. 

When emails are sent using the mandrill app, the events returned are routed to the added web hook url, with "/mandrill_event" end point. Ideally,the notifications are then relayed to the front end through the open web socket connection. However, to view the events from mandrill, in real time on the front end, the app should be hosted on a web server (because local urls are not accepted when an attempt to add a mandrill web hook is made). In this case the web hook url will be "https://server_address/mandrill_event". 

To test the proper functioning of the mandrill event listening activity and storing of the events into a database, a test_.py file is used which uses pytest to ensure events are captured correctly and stored in the database, when a post request is made to the "/mandrill_event" endpoint with dummy payloads.
  - To run the test_.py, the command to be used is "python -m pytest main/test_.py -v" . This should pass all the 3 test cases.

The user has an option to close the web socket connection manually using the "Disconnect Websocket" button. In this case no more notifications will be displayed on the dash board. Simply reloading the page will re-initiate the connection.

