import sqlite3
import logging
from datetime import datetime

class DataBaseManager:

    logging.basicConfig(filename='errors.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    def __init__(self,payload):
        self.payload = payload

    #Method to connect to the SQLite database, "mandrill_events.db"
    def connect_db(self):
        try:
            conn = sqlite3.connect('mandrill_events.db')
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS mandrill_events (id TEXT PRIMARY KEY NOT NULL, email TEXT NOT NULL,  event TEXT NOT NULL, timestamp TIMESTAMP NOT NULL);''') #Create a table "mandrill_events" if doesn't exist already
            conn.commit()
            return conn #Returning the connection 
        
        except Exception as e:
            logging.error("Database Connection Error. Details: {0}".format(str(e)))  #In case of error logging the details to the errors.log file

    #Method to insert the Mandrill events to the SQLite "mandrill_events" schema
    def insert_event(self):
        try: 
            conn = self.connect_db() #Using the database connection returned by the connect_db() method
            cursor = conn.cursor() #Creating a cursor instance
            cursor.execute("INSERT INTO mandrill_events (id, email, event, timestamp) VALUES (?, ?, ?, ?)", (self.payload.id, self.payload.msg['email'], self.payload.event, datetime.fromtimestamp(self.payload.ts))) #Inserting the events in to the schema, using the curosr
            conn.commit()
            conn.close() #Closing the data base connection after commiting the changes

        except Exception as e:
            logging.error("Database Insertion Error. Details: {0}".format(str(e))) #In case of error logging it to the error.log file
            