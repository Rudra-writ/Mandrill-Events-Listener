from fastapi import WebSocket, WebSocketDisconnect
import logging

class WebSocketManager:
    def __init__(self):
        self.connections = []
    
    #Method to open a websocket connection
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
    
    #Method to disconnect the websocket connection
    def disconnect(self, websocket: WebSocket):
        try:
            self.connections.remove(websocket)
        except:
            logging.error("No websocket to disconnect")
    
    #Method to send the notification containing Mandrill events information via web scoket to the front end
    async def send_notification(self, message: str):
        for connection in self.connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                logging.basicConfig(filename='errors.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
                logging.error("Data could not be sent through Socket. Web Sockect disconnected") #In case of error logging the details to the log file
                self.disconnect(connection) #Then calling the disconnect method to disconnect the connection
