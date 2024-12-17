import bs4
import time
import json
import logging
import datetime
import requests
import urllib.parse

logger = logging.getLogger(__name__)

class Wrapper:
    def __init__(self):
        self.client_id = None
        self.access_token = None
        self.access_token_timestamp = None
        self.client_token = None
        self.client_token_timestamp = None

    #> Public methods
    def get_track(self, track_id: str) -> bool|dict:
        logger.info("Getting track from Spotify...")
        response = requests.get(("https://api-partner.spotify.com/pathfinder/v1/query?" + urllib.parse.urlencode({
            "operationName": "getTrack",
            "variables": json.dumps({"uri": f"spotify:track:{track_id}"}),
            "extensions": json.dumps({"persistedQuery": {"version": 1, "sha256Hash": "5c5ec8c973a0ac2d5b38d7064056c45103c5a062ee12b62ce683ab397b5fbe7d"}})
        })), headers=self.get_headers())
        if response.status_code == 200:
            logger.info("Successfully retrieved track from Spotify.")
            return response.json()["data"]
        else:
            logger.error(f"Failed to retrieve track from Spotify. Status code: {response.status_code}")
            return False
    
    def get_headers(self):
        self._update_tokens()
        return {"Accept": "*/*", "Authorization": f"Bearer {self.access_token}", "Client-Token": self.client_token}
    
    #> Private methods
    def _update_tokens(self):
        if self.access_token is None or self.client_token is None:
            self._get_access_token()
            self._get_client_token()
        else:
            if (datetime.datetime.now() - self.access_token_timestamp).seconds > 3600:
                self._get_access_token()
            if (datetime.datetime.now() - self.client_token_timestamp).seconds > 3600:
                self._get_client_token()
    
    def _get_access_token(self):
        while self.access_token is None:
            logger.info("Requesting access token from Spotify...")
            response = requests.get("https://open.spotify.com", headers={"Accept": "text/html"})
            if response.status_code == 200:
                logger.info("Successfully connected to Spotify.")
                soup = bs4.BeautifulSoup(response.text, "html.parser")
                script_tag = soup.find("script", {"id": "session", "data-testid": "session"})
                if script_tag:
                    logger.info("Found session script tag.")
                    session_data = script_tag.string
                    session_json = json.loads(session_data)
                    self.access_token = session_json["accessToken"]
                    self.access_token_timestamp = datetime.datetime.now()
                    self.client_id = session_json["clientId"]
                    logger.info("Access token and client ID retrieved successfully.")
                    logger.debug(f"Access token: {self.access_token}")
                    logger.debug(f"Client ID: {self.client_id}")
                else:
                    logger.error("Session script tag not found. Retrying in 2 seconds...")
                    time.sleep(2)
            else:
                logger.error(f"Failed to connect to Spotify. Status code: {response.status_code}. Retrying in 2 seconds...")
                time.sleep(2)
    
    def _get_client_token(self):
        while self.client_token is None:
            logger.info("Requesting client token from Spotify...")
            response = requests.post("https://clienttoken.spotify.com/v1/clienttoken", headers={"Accept": "application/json"}, json={
                "client_data": {
                    "client_version": "1.2.54.42.gd1ce9e40",  #? Update this if needed
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
            if response.status_code == 200:
                parsed_response = response.json()
                if parsed_response.get("response_type") == "RESPONSE_GRANTED_TOKEN_RESPONSE":
                    logger.info("Client token request was granted by the server.")
                    self.client_token = parsed_response.get("granted_token").get("token")
                    self.client_token_timestamp = datetime.datetime.now()
                    logger.debug(f"Client token: {self.client_token}")
                else:
                    logger.error(f"Client token request was denied by the server, status code: `{response.status_code}`")
                    time.sleep(2)
            else:
                logger.error(f"Failed to retrieve client token. Status code: {response.status_code}. Retrying in 2 seconds...")
                time.sleep(2)