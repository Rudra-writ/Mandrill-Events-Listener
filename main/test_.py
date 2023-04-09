from fastapi.testclient import TestClient
import pytest
from main.app import app

client = TestClient(app) 

#Creating the test cases with dummy payloads
@pytest.mark.parametrize("_id, event, ts, msg", 
[("10", "open", 20230408, {"email":"xyz@abc.com"}),  
("20", "click", 20230408, {"email":"xyz@abc.com"}),
("30", "send", 20230408, {"email":"efg@abc.com"}),     
],)
def test_mandrill_response(_id, event, ts, msg):
    
    response = client.post("/mandrill_event", json={"_id": _id, "event": event, "ts": ts, "msg": msg })   #post request to the "/mandrill_event" endpoint
    if (event == "open"):   
        #In case the event is "open", the response from the backend shold be " {"status": "ok"} "
        assert response.status_code == 200  
        assert response.json() == 	{"status": "ok"}  
    else:
        #In case of any other event, the response from the backend shold be " {"status": "ignored"} "
        assert response.status_code == 200 
        assert response.json() == 	{"status": "ignored"} 


