import logging
from .models import *
from .wrapper import Wrapper
from fastapi import APIRouter, Depends, Request

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/spotify",
    tags=["spotify", "provider"],
    responses={404: {"description": "Not found"}},
)

@router.get("/track", response_model=Song|dict)
def track(track_id: str):
    """
    > track_id: str
        ? Song ID
    > get_recommendations: bool|int = False
        ? Get recommendations for the track, normally 5 unless user specifies otherwise
    > get_a_pop_tracks: bool|int = False
        ? Get the artist's popular tracks, normally 5 unless user specifies otherwise
    > get_a_pop_albums: bool|int = False
        ? Get the artist's popular albums, normally 5 unless user specifies otherwise
    > get_a_pop_posts: bool|int = False
        ? Get the artist's popular posts, normally 5 unless user specifies otherwise
    """
    pass

@router.get("/playlist", response_model=Playlist|dict)
def playlist(playlist_id: str): 
    """
    > playlist_id: str
        ? Playlist ID
    > track_count: int|str = "*"
        ? Number of tracks to return, default is all (that are able to be scrapped from the playlist on first load)
    > get_a_other_albums: bool|int = False
        ? Get the artist's other albums, normally 5 unless user specifies otherwise
    """
    pass

@router.get("/artist", response_model=Artist|dict)
def artist(artist_id: str):
    """
    > artist_id: str
        ? Artist ID
    > get_popular_tracks: bool|int = False
        ? Get the artist's popular tracks, normally 5 unless user specifies otherwise
    > get_popular_discography: bool|int = False
        ? Get the artist's popular discography, normally 5 unless user specifies otherwise
    """
    pass

@router.get("/album", response_model=Album|dict)
def album(album_id: str):
    """
    > album_id: str
        ? Album ID
    > track_count: int|str = "*"
        ? Number of tracks to return, default is all
    > get_a_other_albums: bool|int = False
        ? Get the artist's other albums, normally 5 unless user specifies otherwise
    """
    pass