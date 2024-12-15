import bs4
import time
import logging
import datetime
import requests

logger = logging.getLogger(__name__)

class Wrapper:
    def __init__(self):
        self.session = requests.Session()
        
        self.client_token = None
        self.client_token_timestamp = None
        
        self.get_client_token()
        
    def get_client_token(self):
        while self.client_token == None:
            response = self.session.get("https://clienttoken.spotify.com/v1/clienttoken", headers={"Accept": "application/json"}, payload={
                    "client_data": {
                    "client_version": "1.2.54.42.gd1ce9e40",
                    "client_id": "d8a5ed958d274c2e8ee717e6a4b0971d",
                    "js_sdk_data": {
                        "device_brand": "unknown",
                        "device_model": "unknown",
                        "os": "unknown",
                        "os_version": "unknown",
                        "device_id": "unknown",
                        "device_type": "unknown"
                    }
                }
            })
            if response.status_code() == 200:
                logger.info("Client token request went through")
                parsed_response = response.json()
                if parsed_response["response_type"] == "RESPONSE_GRANTED_TOKEN_RESPONSE":
                    self.client_token = parsed_response["granted_token"]["token"]
                    self.client_token_timestamp = datetime.datetime.now()
                else:
                    logger.error("Client token request was denied by the server, attempting to get a new token")
                    time.sleep(2)
                    continue
                
    def check_client_token(self):
        if self.client_token == None:
            self.get_client_token()
        else:
            if (datetime.datetime.now() - self.client_token_timestamp).seconds > 1209600:
                self.get_client_token()
            else:
                return True