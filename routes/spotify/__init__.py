import logging
from .wrapper import Wrapper
from fastapi import APIRouter, Depends, Request

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/spotify",
    tags=["Spotify"],
    responses={404: {"description": "Not found"}},
)
wrapper = Wrapper()

@router.get("/track")
def track(track_id: str, get_raw: bool = False):
    """
    % Get a track from Spotify
        > track_id: str
            ? Song ID
        > get_raw: bool = False
            ? Get the raw response from the API wrapper
    """
    if not get_raw:
        pass
    else:
        return wrapper.get_track(track_id)

@router.get("/playlist")
def playlist(playlist_id: str, get_raw: bool = False): 
    """
    % Get a playlist from Spotify
        > playlist_id: str
            ? Playlist ID
        > get_raw: bool = False
            ? Get the raw response from the API wrapper
    """
    if not get_raw:
        pass
    else:
        return wrapper.get_playlist(playlist_id)

@router.get("/artist")
def artist(artist_id: str, get_raw: bool = False):
    """
    % Get an artist from Spotify
        > artist_id: str
            ? Artist ID
        > get_raw: bool = False
            ? Get the raw response from the API wrapper
    """
    if not get_raw:
        pass
    else:
        return wrapper.get_artist(artist_id)

@router.get("/album")
def album(album_id: str, get_raw: bool = False):
    """
    % Get an album from Spotify
        > album_id: str
            ? Album ID
        > get_raw: bool = False
            ? Get the raw response from the API wrapper
    """
    if not get_raw:
        pass
    else:
        return wrapper.get_album(album_id)