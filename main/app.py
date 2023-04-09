from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from mailchimp_transactional.api_client import ApiClientError
from fastapi.templating import Jinja2Templates
from main.web_socket_manager import WebSocketManager
from main.database_manager import DataBaseManager
from main.webhook_manager import WebHookManager
from datetime import datetime
import logging


app = FastAPI() #Creating a FastAPI instance
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/") # Initializing Jinja2Templates and setting the directory for template files to the "templates/" directory
websocket_manager = WebSocketManager() #Creating an instance of the WebSocketManager class
logging.basicConfig(filename='errors.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s') #Setting up the basic configuration to log any error, if occurs, into a log file 'errors.log'


#Creating a pydantic model
class MandrillEvent(BaseModel):
    id: str
    event: str
    ts: int
    msg: Optional[dict] = None
    class Config:
        '''Using aliasing to prefix the field names with a "_". This is done because we are using 'id' in our pydantic model but
           the JSON payload returned by mandrill event has "_id" attribute, however the "_id" is not accesible due to the underscore.
           The "allow_population_by_field_name" allows us to use field name
           "id" when creating a 'MandrillEvent' instance from dictionary.'''
        alias_generator = lambda field_name: "_" + field_name
        allow_population_by_field_name = True


#Creating a websocket endpoint at /ws
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket) #Using the connect method of WebSocketManager class to connect to the web socket 
    try:
        while True:
            data = await websocket.receive_text()  # As long as the connection is active any data recieved over the websocket from the front end is read 
            if data != "disconnect":
                 try:
                    webhook_manager = WebHookManager(data) #Creating a WebHookManager instance with data as the argument
                    url = webhook_manager.add_webhook()  #Calling the add_webhook method   
                    await websocket_manager.send_notification("WebHook to '{0}' successfully added!!".format(url)) #If everything goes fine notify the user through web socket that web hook has been added
                 except ApiClientError as error:
                    await websocket_manager.send_notification("Couldn't add WebHook!! Error. Details: {0}".format(error.text)) #In case of exception notify the user about the details
                    logging.error("WebHook add Error. Details: {0}".format(error.text))           
            else:
                #The user also have an option to disconnect the web socket manually. If they choose that, notify the user and close the connection
                #using 'disconnect' method of WebSocketManager. The conenction can be re-initiated by simply reloading the page.
                await websocket_manager.send_notification("WebSocket closed!! Please refresh the page to reconnect...") 
                websocket_manager.disconnect(websocket)

    except WebSocketDisconnect:
                logging.error("Data could not be received through socket. Web Sockect disconnected")
                websocket_manager.disconnect(websocket)

        
#End point to listen to mandrill events. Uses only a 'post' method, the minimum requirement to add a mandrill webhook  
@app.post("/mandrill_event")
async def mandrill_event(payload: MandrillEvent): #Recieving the payload from Mandrill when a mail is sent from it

    try:
        
        if payload.event == "open":  #Check if the event returned by Mandrill payload is an 'open' event
           
            database_manager = DataBaseManager(payload) #Creating an instance of the 'DataBaseManager' class (with payload as the argument) of the database_manager module
            database_manager.insert_event() #Calling the insert_event method to insert the attributes of the payload in a schema of SQLite database
            
            message = f"Mandrill event: {payload.event} for email: {payload.msg['email'] } at: { datetime.fromtimestamp(payload.ts) }  id: {payload.id} "
            await websocket_manager.send_notification(message) #Using the 'send_notification()' method of WebSocketManager class to notify the user of the Mandrill event details in the front end
            
            return {"status": "ok"} #if the event is "open" return "ok" status to Mandrill
        else:
            return {"status": "ignored"} #if the event is other than "open" ignore the event and return the status to Mandrill
        
    except Exception as e:
        logging.error("Mandril events listening Error. Details: {0}".format(str(e)))  
    
#Creating a get endpoint at root to serve the index.html front end to the user    
@app.get("/")
def serve_template(request: Request):
    return templates.TemplateResponse('index.html', context ={'request':request})
    
