import logging
import traceback
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
    try:
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
                except (KeyError, IndexError):
                    logger.error(f"Failed to retrieve data for {artist_data}. | {traceback.format_exc()}")
                except Exception as e:
                    logger.error(f"An error occurred: {e} | {traceback.format_exc()}")
                
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
    except Exception as e:
        logger.error(f"An error occurred: {e} - {traceback.format_exc()}")
        return {"status": "error", "data": "An error occurred."}
    
@router.get("/playlist")
def playlist(playlist_id: str, offset: int = 0, limit: int = 50, get_raw: bool = False): 
    """
    % Get a playlist from Spotify
        > playlist_id: str
            ? Playlist ID
        > get_raw: bool = False
            ? Get the raw response from the API wrapper
    """
    try:
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
                except (KeyError, IndexError):
                    logger.error(f"Failed to retrieve data for {item}. | {traceback.format_exc()}")
                except Exception as e:
                    logger.error(f"An error occurred: {e} | {traceback.format_exc()}")
            
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
    except Exception as e:
        logger.error(f"An error occurred: {e} - {traceback.format_exc()}")
        return {"status": "error", "data": "An error occurred."}

@router.get("/artist")
def artist(artist_id: str, get_raw: bool = False):
    """
    % Get an artist from Spotify
        > artist_id: str
            ? Artist ID
        > get_raw: bool = False
            ? Get the raw response from the API wrapper
    """
    try: 
        raw_data = wrapper.get_artist(artist_id)
        if not raw_data:
            return {"status": "error", "data": "Either the artist was not found, we are being rate limited, or there was an error with the request."}
        
        if get_raw:
            return {"status": "success", "data": raw_data}
        else:
            
            if "__typename" not in raw_data or raw_data["__typename"] != "Artist":
                return {"status": "error", "data": "The ID provided is not an artist ID."}
            profile_data = raw_data["profile"]
            pinned_item_data = profile_data["pinnedItem"]
            pinned_item_content_data = pinned_item_data["itemV2"]["data"]
            related_content_data = raw_data["relatedContent"]
            artist_statistics = raw_data["stats"]
            artist_concerts = raw_data["goods"]["events"]["concerts"]
            
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
                except (KeyError, IndexError):
                    logger.error(f"Failed to retrieve data for {appearance}. | {traceback.format_exc()}")
                except Exception as e:
                    logger.error(f"An error occurred: {e} | {traceback.format_exc()}")
                    
            discovered_on = []
            for discovery in related_content_data["discoveredOnV2"]["items"]: #? Might need to be updated if the response changes
                try:
                    #TODO: Add other typenames (if there are any)
                    discovery = discovery["data"]
                    if discovery["__typename"] == "Playlist":
                        discovered_on.append({
                            "title": discovery["name"],
                            "id": discovery["uri"].split(":")[-1],
                            "uri": discovery["uri"],
                            "owner": discovery["ownerV2"]["data"]["name"], #? Might need to be updated if the response changes
                            "images": [image["sources"] for image in discovery["images"]["items"]],
                            "description": discovery["description"],
                        })
                except (KeyError, IndexError):
                    logger.error(f"Failed to retrieve data for {discovery}. | {traceback.format_exc()}")
                except Exception as e:
                    logger.error(f"An error occurred: {e} | {traceback.format_exc()}")
                    
            featured_in = []
            for feature in related_content_data["featuringV2"]["items"]:
                try:
                    feature = feature["data"]
                    if feature["__typename"] == "Playlist":
                        featured_in.append({
                            "title": feature["name"],
                            "id": feature["uri"].split(":")[-1],
                            "uri": feature["uri"],
                            "owner": feature["ownerV2"]["data"]["name"], #? Might need to be updated if the response changes
                            "images": [image["sources"] for image in feature["images"]["items"]],
                            "description": feature["description"],
                        })
                except (KeyError, IndexError):
                    logger.error(f"Failed to retrieve data for {feature}. | {traceback.format_exc()}")
                except Exception as e:
                    logger.error(f"An error occurred: {e} | {traceback.format_exc()}")
                
            related_artists = []
            for artist in related_content_data["relatedArtists"]["items"]:
                related_artists.append({
                    "name": artist["profile"]["name"],
                    "id": artist["uri"].split(":")[-1],
                    "uri": artist["uri"],
                    "avatar": artist["visuals"]["avatarImage"]["sources"],
                })
            
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
                except (KeyError, IndexError):
                    logger.error(f"Failed to retrieve data for {playlist}. | {traceback.format_exc()}")
                except Exception as e:
                    logger.error(f"An error occurred: {e} | {traceback.format_exc()}")
            
            top_countries = []
            for city in artist_statistics["topCities"]["items"]:
                country = city["country"]
                listeners = city["numberOfListeners"]
                for country in top_countries:
                    if country["country"] == country:
                        country["listeners"] += listeners
                        break
                else:
                    top_countries.append({
                        "country": country,
                        "listeners": listeners,
                    })
            top_countries = sorted(top_countries, key=lambda x: x["listeners"], reverse=True)
            
            top_regions = []
            for city in artist_statistics["topCities"]["items"]:
                region = city["region"]
                listeners = city["numberOfListeners"]
                for region in top_regions:
                    if region["region"] == region:
                        region["listeners"] += listeners
                        break
                else:
                    top_regions.append({
                        "region": region,
                        "listeners": listeners,
                    })
            top_regions = sorted(top_regions, key=lambda x: x["listeners"], reverse=True)
            
            top_cities = []
            for city in artist_statistics["topCities"]["items"]:
                top_cities.append({
                    "city": city["city"],
                    "country": city["country"],
                    "region": city["region"],
                    "listeners": city["numberOfListeners"],
                })
            top_cities = sorted(top_cities, key=lambda x: x["listeners"], reverse=True)
            
            concerts = []
            for concert in artist_concerts["items"]:
                try:
                    concerts.append({
                        "title": concert["title"],
                        "id": concert["uri"].split(":")[-1],
                        "uri": concert["uri"],
                        "date": concert["date"]["isoString"],
                        "venue": concert["venue"],
                        "isFestival": concert["festival"],
                    })
                except (KeyError, IndexError):
                    logger.error(f"Failed to retrieve data for {concert}. | {traceback.format_exc()}")
                except Exception as e:
                    logger.error(f"An error occurred: {e} | {traceback.format_exc()}")
            
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
                                "backgroundImage": pinned_item_data["backgroundImageV2"]["data"]["sources"] 
                                    if pinned_item_data["backgroundImageV2"] != None else None, #? Might need to be updated if the response changes
                                "thumbnailImage": pinned_item_data["thumbnailImage"]["data"]["sources"],
                            },
                            "itemData": {
                                "title": pinned_item_content_data["name"],
                                "id": pinned_item_content_data["uri"].split(":")[-1],
                                "uri": pinned_item_content_data["uri"],
                                "type": pinned_item_content_data["__typename"].upper(),
                                "coverData": pinned_item_content_data["coverArt"]["sources"] if "coverArt" in pinned_item_content_data else None,
                            }
                        },
                        "playlists": profile_playlists
                    },
                    "relatedContent": {
                        "appearsOn": appears_on,
                        "discoveredOn": discovered_on,
                        "featuredIn": featured_in,
                        "relatedArtists": related_artists
                    },
                    "statistics": {
                        "followers": artist_statistics["followers"],
                        "monthlyListeners": artist_statistics["monthlyListeners"],
                        "worldRank": artist_statistics["worldRank"],
                        "topCities": top_cities,
                        "topCountries": top_countries,
                        "topRegions": top_regions,
                    },
                    "concerts": concerts,
                    "visuals": {
                        "avatar": {
                            "colors": raw_data["visuals"]["avatarImage"]["extractedColors"]["colorRaw"]["hex"],
                            "sources": raw_data["visuals"]["avatarImage"]["sources"],
                        },
                        "gallery": raw_data["visuals"]["gallery"]["items"],
                        "header": {
                            "colors": raw_data["visuals"]["headerImage"]["extractedColors"]["colorRaw"]["hex"],
                            "sources": raw_data["visuals"]["headerImage"]["sources"],
                        }
                    }
                }
            }
    except Exception as e:
        logger.error(f"An error occurred: {e} - {traceback.format_exc()}")
        return {"status": "error", "data": "An error occurred."}

@router.get("/album")
def album(album_id: str, get_raw: bool = False):
    """
    % Get an album from Spotify
        > album_id: str
            ? Album ID
        > get_raw: bool = False
            ? Get the raw response from the API wrapper
    """
    try:
        raw_data = wrapper.get_album(album_id)
        if not raw_data:
            return {"status": "error", "data": "Either the album was not found, we are being rate limited, or there was an error with the request."}
        
        if get_raw:
            return {"status": "success", "data": raw_data}
        else:
            pass
    except Exception as e:
        logger.error(f"An error occurred: {e} - {traceback.format_exc()}")
        return {"status": "error", "data": "An error occurred."}