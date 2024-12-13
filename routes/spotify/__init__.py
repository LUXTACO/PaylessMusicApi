import bs4
import logging
import requests
from .models import *
from fastapi import APIRouter, Depends, Request

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/spotify",
    tags=["spotify", "provider"],
    responses={404: {"description": "Not found"}},
)

@router.get("/track", response_model=Song)
def track(id_: str):
    pass

@router.get("/playlist", response_model=Playlist)
def playlist(id_: str, track_count: int = 99):
    pass

@router.get("/artist", response_model=Artist)
def artist(id_: str, pt_count: int = 5, pd_count: int = 5):
    pass

@router.get("/album", response_model=Album)
def album(id_: str):
    pass