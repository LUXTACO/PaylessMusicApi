from enum import Enum

class Endpoints:
    song: str = "track"
    artist: str = "artist"
    playlist: str = "playlist"
    
class RequestType(Enum):
    GET
    POST
    PUT
    DELETE