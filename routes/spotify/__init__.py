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
    if not raw_data:
        return {"status": "error", "data": "Either the track was not found, we are being rate limited, or there was an error with the request."}

    if get_raw:
        return {"status": "success", "data": raw_data}
    else:
        artist_data = raw_data["firstArtist"]["items"][0]
        main_artist = {
            "name": artist_data["profile"]["name"],
            "id": artist_data["uri"].split(":")[-1],
            "uri": artist_data["uri"],
            "avatar": artist_data["visuals"]["avatarImage"]["sources"],
            "relatedArtists": artist_data["relatedContent"]["relatedArtists"]["items"],
        }
        
        artists = raw_data["otherArtists"]["items"]
        secondary_artists = []
        for artist_data in artists:
            try:
                secondary_artists.append({
                    "name": artist_data["profile"]["name"],
                    "id": artist_data["uri"].split(":")[-1],
                    "uri": artist_data["uri"],
                    "avatar": artist_data["visuals"]["avatarImage"]["sources"],
                    "relatedArtists": artist_data["relatedContent"]["relatedArtists"]["items"],
                })
            except [KeyError, IndexError]:
                logger.error(f"Failed to retrieve data for {artist_data}.")
            except Exception as e:
                logger.error(f"An error occurred: {e}")
            
        track_album_data = raw_data["albumOfTrack"]
        track_album_cover_data = track_album_data["coverArt"]
        duration = raw_data["duration"]["totalMilliseconds"]
        return {
            "status": "success",
            "data": {
                "title": raw_data["name"],
                "id": raw_data["uri"].split(":")[-1],
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
                    "id": track_album_data["uri"].split(":")[-1],
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
        }

@router.get("/playlist")
def playlist(playlist_id: str, offset: int = 0, limit: int = 50, get_raw: bool = False): 
    """
    % Get a playlist from Spotify
        > playlist_id: str
            ? Playlist ID
        > get_raw: bool = False
            ? Get the raw response from the API wrapper
    """
    raw_data = wrapper.get_playlist(playlist_id, offset, limit)["playlistV2"]
    if not raw_data:
        return {"status": "error", "data": "Either the playlist was not found, we are being rate limited, or there was an error with the request."}
    
    if get_raw:
        return {"status": "success", "data": raw_data}
    else:
        owner_data = raw_data["ownerV2"]["data"]
        
        playlist_contents = raw_data["content"]["items"]
        playlist_tracks = []
        for item in playlist_contents:
            try:
                track_data = item["itemV2"]["data"] #? Might need to be updated if the response changes
                track_album_data = track_data["albumOfTrack"]
                track_album_cover_data = track_album_data["coverArt"]
                artists = track_data["artists"]["items"]
                duration = track_data["trackDuration"]["totalMilliseconds"]
                    
                playlist_tracks.append({
                    "title": track_data["name"],
                    "id": track_data["uri"].split(":")[-1],
                    "uri": track_data["uri"],
                    "artists": [{
                        "name": artist["profile"]["name"],
                        "id": artist["uri"].split(":")[-1],
                        "uri": artist["uri"],
                    } for artist in artists],
                    "contentRating": track_data["contentRating"]["label"],
                    "playCount": track_data["playcount"],
                    "duration": {
                        "milliseconds": duration,
                        "seconds": duration / 1000,
                        "minutes": duration / 60000
                    },
                    "trackAlbum": {
                        "title": track_album_data["name"],
                        "id": track_album_data["uri"].split(":")[-1],
                        "uri": track_album_data["uri"],
                        "artists": [{
                            "name": artist["profile"]["name"],
                            "id": artist["uri"].split(":")[-1],
                            "uri": artist["uri"],
                        } for artist in track_album_data["artists"]["items"]],
                        "coverData": {
                            "sources": track_album_cover_data["sources"]
                        }
                    },
                    "discNumber": track_data["discNumber"],
                    "trackNumber": track_data["trackNumber"],
                })
            except [KeyError, IndexError]:
                logger.error(f"Failed to retrieve data for {item}.")
            except Exception as e:
                logger.error(f"An error occurred: {e}")
        
        return {
            "status": "success",
            "data": {
                "title": raw_data["name"],
                "id": raw_data["uri"].split(":")[-1],
                "uri": raw_data["uri"],
                "description": raw_data["description"],
                "followers": raw_data["followers"],
                "owner": {
                    "name": owner_data["name"],
                    "username": owner_data["username"],
                    "uri": owner_data["uri"],
                    "avatar": owner_data["avatar"]["sources"],
                },
                "playlistTracks": playlist_tracks
            }
        }

@router.get("/artist")
def artist(artist_id: str, get_raw: bool = False):
    """
    % Get an artist from Spotify
        > artist_id: str
            ? Artist ID
        > get_raw: bool = False
            ? Get the raw response from the API wrapper
    """
    raw_data = wrapper.get_artist(artist_id)
    if not raw_data:
        return {"status": "error", "data": "Either the artist was not found, we are being rate limited, or there was an error with the request."}
    
    if get_raw:
        return {"status": "success", "data": raw_data}
    else:
        profile_data = raw_data["profile"]
        pinned_item_data = profile_data["pinnedItem"]
        pinned_item_content_data = pinned_item_data["itemV2"]["data"]
        related_content_data = raw_data["relatedContent"]
        
        appears_on = []
        for appearance in related_content_data["appearsOn"]["items"]:
            try:
                for data in appearance["releases"]["items"]:
                    appears_on.append({
                        "title": data["name"],
                        "id": data["uri"].split(":")[-1],
                        "uri": data["uri"],
                        "type": data["type"],
                        "date": data["date"],
                        "artists": [data["profile"]["name"] for data in data["artists"]["items"]],
                        "coverData": data["coverArt"]["sources"],
                    })
            except [KeyError, IndexError]:
                logger.error(f"Failed to retrieve data for {appearance}.")
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                
        discovered_on = []
        for discovery in related_content_data["discoveredOnV2"]["items"]:
            try:
                discovery = discovery["data"]
                if discovery["__typename"] != "GenericError":
                    pass
            except [KeyError, IndexError]:
                logger.error(f"Failed to retrieve data for {discovery}.")
            except Exception as e:
                logger.error(f"An error occurred: {e}")
         
        profile_playlists = []
        for playlist in profile_data["playlistsV2"]["items"]:
            try: 
                playlist = playlist["data"]
                profile_playlists.append({
                    "title": playlist["name"],
                    "id": playlist["uri"].split(":")[-1],
                    "uri": playlist["uri"],
                    "description": playlist["description"],
                    "images": playlist["images"]["items"],
                    "owner": playlist["ownerV2"]["data"]["name"],
                })
            except [KeyError, IndexError]:
                logger.error(f"Failed to retrieve data for {playlist}.")
            except Exception as e:
                logger.error(f"An error occurred: {e}")
        
        return {
            "status": "success",
            "data": {
                "name": profile_data["name"],
                "id": raw_data["uri"].split(":")[-1],
                "uri": raw_data["uri"],
                "verified": profile_data["verified"],
                "profile": {
                    "biography": profile_data["biography"],
                    "externalLinks": profile_data["externalLinks"]["items"],
                    "pinnedItem": {
                        "title": pinned_item_data["title"],
                        "subtitle": pinned_item_data["subtitle"],
                        "type": pinned_item_data["type"],
                        "uri": pinned_item_data["uri"],
                        "comment": pinned_item_data["comment"],
                        "assets": {
                            "backgroundImage": pinned_item_data["backgroundImageV2"]["data"]["sources"], #? Might need to be updated if the response changes
                            "thumbnailImage": pinned_item_data["thumbnailImage"]["data"]["sources"],
                        },
                        "itemData": {
                            "title": pinned_item_content_data["name"],
                            "id": pinned_item_content_data["uri"].split(":")[-1],
                            "uri": pinned_item_content_data["uri"],
                            "type": pinned_item_content_data["type"],
                            "coverData": pinned_item_content_data["coverArt"]["sources"],
                        }
                    },
                    "playlists": profile_playlists
                },
                "relatedContent": {
                    "appearsOn": appears_on,
                }
            }
        }

@router.get("/album")
def album(album_id: str, get_raw: bool = False):
    """
    % Get an album from Spotify
        > album_id: str
            ? Album ID
        > get_raw: bool = False
            ? Get the raw response from the API wrapper
    """
    raw_data = wrapper.get_album(album_id)
    if not raw_data:
        return {"status": "error", "data": "Either the album was not found, we are being rate limited, or there was an error with the request."}
    
    if get_raw:
        return {"status": "success", "data": raw_data}
    else:
        pass