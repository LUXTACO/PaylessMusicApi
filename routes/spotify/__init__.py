import bs4
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
def track(id_: str):
    pass

@router.get()
def playlist(id_: str):
    pass

@router.get()
def artist(id_: str):
    pass