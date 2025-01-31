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
        self.access_token_uses = None
        self.client_token = None
        self.client_token_timestamp = None

#> Public methods
    def get_track(self, track_id: str) -> bool|dict:
        logger.info("Getting track from Spotify...")
        response = requests.get(("https://api-partner.spotify.com/pathfinder/v1/query?" + urllib.parse.urlencode({
            "operationName": "getTrack",
            "variables": json.dumps({"uri": f"spotify:track:{track_id}"}),
            "extensions": json.dumps({"persistedQuery": {"version": 1, "sha256Hash": "5c5ec8c973a0ac2d5b38d7064056c45103c5a062ee12b62ce683ab397b5fbe7d"}})
            #? sha256Hash might need to be updated if the query changes
        })), headers=self.get_headers())
        if response.status_code == 200:
            logger.info("Successfully retrieved track from Spotify.")
            return response.json()["data"]["trackUnion"]
        else:
            logger.error(f"Failed to retrieve track from Spotify. Status code: {response.status_code}")
            return False
    
    def get_playlist(self, playlist_id: str, offset: int, limit: int) -> bool|dict:
        logger.info("Getting playlist from Spotify...")
        response = requests.get(("https://api-partner.spotify.com/pathfinder/v1/query?" + urllib.parse.urlencode({
            "operationName": "fetchPlaylist",
            "variables": json.dumps({"uri": f"spotify:playlist:{playlist_id}", "offset": offset, "limit": limit}), #? default limit is 50 and offset is 0
            "extensions": json.dumps({"persistedQuery": {"version": 1, "sha256Hash": "19ff1327c29e99c208c86d7a9d8f1929cfdf3d3202a0ff4253c821f1901aa94d"}})
            #? sha256Hash might need to be updated if the query changes
        })), headers=self.get_headers())
        if response.status_code == 200:
            logger.info("Successfully retrieved playlist from Spotify.")
            return response.json()["data"]["artistUnion"]
        else:
            logger.error(f"Failed to retrieve playlist from Spotify. Status code: {response.status_code}")
            return False
    
    def get_artist(self, artist_id: str) -> bool|dict:
        logger.info("Getting artist from Spotify...")
        response = requests.get(("https://api-partner.spotify.com/pathfinder/v1/query?" + urllib.parse.urlencode({
            "operationName": "queryArtistOverview",
            "variables": json.dumps({"uri": f"spotify:artist:{artist_id}", "locale": ""}),
            "extensions": json.dumps({"persistedQuery": {"version":1,"sha256Hash":"4bc52527bb77a5f8bbb9afe491e9aa725698d29ab73bff58d49169ee29800167"}})
            #? sha256Hash might need to be updated if the query changes
        })), headers=self.get_headers())
        if response.status_code == 200:
            logger.info("Successfully retrieved artist from Spotify.")
            return response.json()["data"]["artistUnion"]
        else:
            logger.error(f"Failed to retrieve artist from Spotify. Status code: {response.status_code}")
            return False
    
    def get_album(self, album_id: str, offset: int, limit: int) -> bool|dict:
        logger.info("Getting album from Spotify...")
        response = requests.get(("https://api-partner.spotify.com/pathfinder/v1/query?" + urllib.parse.urlencode({
            "operationName": "getAlbum",
            "variables": json.dumps({"uri": f"spotify:album:{album_id}", "locale": "", "offset": offset, "limit": limit}), #? default limit is 50 and offset is 0
            "extensions": json.dumps({"persistedQuery": {"version":1,"sha256Hash":"8f4cd5650f9d80349dbe68684057476d8bf27a5c51687b2b1686099ab5631589"}})
            #? sha256Hash might need to be updated if the query changes
        })), headers=self.get_headers())
        if response.status_code == 200:
            logger.info("Successfully retrieved playlist from Spotify.")
            return response.json()["data"]
        else:
            logger.error(f"Failed to retrieve playlist from Spotify. Status code: {response.status_code}")
            return False
    
    def perform_search(self, query: str, offset: int, limit: int, top_results_num: int) -> bool|dict:
        logger.info("Performing search on Spotify...")
        response = requests.get(("https://api-partner.spotify.com/pathfinder/v1/query?" + urllib.parse.urlencode({
            "operationName": "searchDesktop",
            "variables": json.dumps({
                "searchTerm": query, "offset": offset, "limit": limit, "numberOfTopResults": top_results_num,
                "includeAudiobooks": True, "includeArtistHasConcertsField": True, "includePreReleases": True,
                "includeLocalConcertsField": True
            }), #? default limit is 10 and offset is  | default top_results_num is 5
            "extensions": json.dumps({"persistedQuery": {"version":1,"sha256Hash":"dd1513013a4ab0d9c095eac6b6d292c801bef038e11e06b746385a509be24ab0"}})
            #? sha256Hash might need to be updated if the query changes
        })), headers=self.get_headers())
        if response.status_code == 200:
            logger.info("Successfully performed search on Spotify.")
            return response.json()["data"]["searchV2"] #? This might change if searchV2 is updated
        else:
            logger.error(f"Failed to perform search on Spotify. Status code: {response.status_code}")
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
            if self.access_token_uses is None or self.access_token_uses >= 1:
                self._get_access_token()
            if (datetime.datetime.now() - self.client_token_timestamp).seconds > 1200000:
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
                    self.access_token_uses = 0
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
                