from typing import List

class Artist:
    id_: str
    url: str
    name: str
    followers: int
    is_verified: bool
    monthly_listeners: int
    listeners_location: dict
    popular_tracks: List[mTrack] #? List of popular tracks, normally 5 unless user specifies otherwise
    popular_discography: List[mAlbum] #? List of albums normally 5 unless user specifies otherwise

class Track:
    id_: str
    url: str
    name: str
    streams: int
    album: mAlbum
    release_year: str
    artists: List[mArtist]
    recommendations: List[mTrack]
    
class Album: 
    id_: str
    url: str
    name: str
    duration: int
    release_year: str
    tracks: List[mTrack]
    artists: List[mArtist]
    
class Playlist:
    id_: str
    url: str
    name: str
    duration: int
    description: str
    saved_times: int
    authors: List[mArtist]
    
#% Minified version of the track class 
class mTrack: 
    id_: str
    url: str
    name: str
    artists: List[mArtist]
    duration: int #? Should be in seconds
    
    def add_attribute(self, key: str, value: str):
        #> added date | album | streams
        setattr(self, key, value)
    
#% Minified version of the artist class
class mArtist: 
    id_: str
    url: str
    name: str
    
    def add_attribute(self, key: str, value: str):
        setattr(self, key, value)
        
#% Minified version of the playlist class
class mPlaylist:
    id_: str
    url: str
    name: str
    author_name: str

    def add_attribute(self, key: str, value: str):
        setattr(self, key, value)
        
#% Minified version of the album class
class mAlbum:
    id_: str
    url: str
    name: str
    is_single: bool
    release_year: str
    
    def add_attribute(self, key: str, value: str):
        setattr(self, key, value)