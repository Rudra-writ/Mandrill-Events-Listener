import mailchimp_transactional as MailchimpTransactional
from main.web_socket_manager import WebSocketManager
import logging

class WebHookManager:
    logging.basicConfig(filename='errors.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    

    def __init__(self, data):
        self.data = data

    ''' In the front end, the user has the option to input a url of choice to which the mandrill webhook will be attached. When they click on
    the 'Add WebHook' button, the url entered will be set as the webhook url and a an API call will be initiated to add the web hook.
    This feature allows the user to change the Mandrill's event listening end point with convenience, without having to use the mandrill app.
    This is also a way to test the web socket connection is open and the web hook url is valid '''
    def add_webhook(self):
        websocket_manager = WebSocketManager()
        url = self.data if self.data != '' else "http://meagan.org" #If the user does not enter a url for webhook( which is ideally the address of the websever serving this backend followed by '/mandrill_event' endpoint), use a default url (Mandrill API documentation)            
        # The below snippet uses the Client class of MailchimpTransactional module and an API key (use any valid API key) to add the web hook (found in Mandrill API documentation)
        mailchimp = MailchimpTransactional.Client("md-8Jp1N96IZCxKPJdJfNrwig") 
        response = mailchimp.webhooks.add({"url": url})
        return url
       
                        
        
