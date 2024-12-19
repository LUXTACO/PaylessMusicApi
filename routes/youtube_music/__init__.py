import logging
from .wrapper import Wrapper
from fastapi import APIRouter, Depends, Request

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/youtube_music",
    tags=["Youtube Music"],
    responses={404: {"description": "Not found"}},
)
wrapper = Wrapper()

@router.get("/track")
def track(track_id: str, get_raw: bool = False):
    """
    % Get a track from Youtube Music
        > track_id: str
            ? Song ID
        > get_raw: bool = False
            ? Get the raw response from the API wrapper
    """
    if not get_raw:
        pass
    else:
        return wrapper.get_track(track_id)