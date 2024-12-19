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
    raw_data = wrapper.get_track(track_id)

    if get_raw:
        return raw_data
    else:
        artist_data = raw_data["firstArtist"]["items"][0]
        main_artist = {
            "name": artist_data["profile"]["name"],
            "id": artist_data["id"],
            "uri": artist_data["uri"],
            "avatar": artist_data["visuals"]["avatarImage"]["sources"],
            "relatedArtists": artist_data["relatedContent"]["relatedArtists"]["items"],
        }
        
        artists = raw_data["otherArtists"]["items"]
        secondary_artists = []
        for artist_data in artists:
            secondary_artists.append({
                "name": artist_data["profile"]["name"],
                "id": artist_data["id"],
                "uri": artist_data["uri"],
                "avatar": artist_data["visuals"]["avatarImage"]["sources"],
                "relatedArtists": artist_data["relatedContent"]["relatedArtists"]["items"],
            })
            
        track_album_data = raw_data["albumOfTrack"]
        track_album_cover_data = track_album_data["coverArt"]
        duration = raw_data["duration"]["totalMilliseconds"]
        return {
            "title": raw_data["name"],
            "id": raw_data["id"],
            "uri": raw_data["uri"],
            "artists": {
                "main": main_artist,
                "secondary": secondary_artists
            },
            "contentRating": raw_data["contentRating"]["label"],
            "playCount": raw_data["playcount"],
            "duration": {
                "milliseconds": duration,
                "seconds": duration / 1000, 
                "minutes": duration / 60000
            },
            "trackAlbum": {
                "title": track_album_data["name"],
                "id": track_album_data["id"],
                "uri": track_album_data["uri"],
                "type": track_album_data["type"],
                "date": track_album_data["date"],
                "tracks": [track["track"] for track in track_album_data["tracks"]["items"]],
                "coverData": {
                    "colors": track_album_cover_data["extractedColors"]["colorRaw"],
                    "sources": track_album_cover_data["sources"]
                }
            }
        }

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