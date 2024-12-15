import logging
from .models import *
from fastapi import APIRouter, Depends, Request

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/spotify",
    tags=["spotify", "provider"],
    responses={404: {"description": "Not found"}},
)

@router.get("/track", response_model=Song)
def track(id_: str, get_recommendations: bool|int = False, get_a_pop_tracks: bool|int = False, get_a_pop_albums: bool|int = False, get_a_pop_posts: bool|int = False):
    """
    > id_: str
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

@router.get("/playlist", response_model=Playlist)
def playlist(id_: str, track_count: int|str = "*", get_a_other_albums: bool|int = False): 
    """
    > id_: str
        ? Playlist ID
    > track_count: int|str = "*"
        ? Number of tracks to return, default is all (that are able to be scrapped from the playlist on first load)
    > get_a_other_albums: bool|int = False
        ? Get the artist's other albums, normally 5 unless user specifies otherwise
    """
    pass

@router.get("/artist", response_model=Artist)
def artist(id_: str, get_popular_tracks: bool|int = False, get_popular_discography: bool|int = False):
    """
    > id_: str
        ? Artist ID
    > get_popular_tracks: bool|int = False
        ? Get the artist's popular tracks, normally 5 unless user specifies otherwise
    > get_popular_discography: bool|int = False
        ? Get the artist's popular discography, normally 5 unless user specifies otherwise
    """
    pass

@router.get("/album", response_model=Album)
def album(id_: str, track_count: int|str = "*", get_a_other_albums: bool|int = False):
    """
    > id_: str
        ? Album ID
    > track_count: int|str = "*"
        ? Number of tracks to return, default is all
    > get_a_other_albums: bool|int = False
        ? Get the artist's other albums, normally 5 unless user specifies otherwise
    """
    pass