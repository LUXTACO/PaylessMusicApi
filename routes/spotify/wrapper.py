import bs4
import time
import logging
import datetime
import requests

logger = logging.getLogger(__name__)

class Wrapper:
    def __init__(self):
        self.session = requests.Session()
        
        self.client_id = None
        self.access_token = None
        self.access_token_timestamp = None
        self.client_token = None
        self.client_token_timestamp = None
        
        self.get_access_token()
        self.get_client_token()
        
    def get_client_token(self):
        while self.client_token == None:
            response = self.session.get("https://clienttoken.spotify.com/v1/clienttoken", headers={"Accept": "application/json"}, payload={
                    "client_data": {
                    "client_version": "1.2.54.42.gd1ce9e40", #? Update this if needed
                    "client_id": self.client_id,
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
                    logger.error(f"Client token request was denied by the server, status code: {response.status_code}")
                    time.sleep(2)
                    continue
                
    def get_access_token(self):
        while self.access_token == None:
            response = self.session.get("https://open.spotify.com", headers={"Accept": "text/html"})
            if response.status_code == 200:
                logger.info("Auth token request went through")
                soup = bs4.BeautifulSoup(response.text, "html.parser")
                script_tag = soup.find("script", {"id": "session", "data-testid": "session"})
                if script_tag:
                    session_data = script_tag.string
                    session_json = json.loads(session_data)
                    self.access_token = session_json.get("accessToken")
                    self.access_token_timestamp = datetime.datetime.now()
                    self.client_id = session_json.get("clientId")
                    logger.info("Access token retrieved successfully")
                else:
                    logger.error("Session script tag not found, trying again")
                    continue
            else:
                logger.error(f"Failed to get auth token, status code: {response.status_code}")
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
            
    def check_access_token(self):
        if self.access_token == None:
            self.get_access_token()
        else:
            if (datetime.datetime.now() - self.access_token_timestamp).seconds > 3600:
                self.get_access_token()
            else:
                return True