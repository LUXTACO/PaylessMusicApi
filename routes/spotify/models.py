from typing import List

class Track:
    id_: str
    url: str
    name: str
    streams: int
    album: mAlbum
    release_date: str
    artists: List[mArtist]
    
    def add_attribute(self, key: str, value: str):
        #> recommendations | artist_popular_tracks | artist_popular_albums | artist_popular_posts
        #? List of recommended |albums/tracks/posts/recommendations|, normally 5 unless user specifies otherwise
        setattr(self, key, value)
    
class Playlist:
    id_: str
    url: str
    name: str
    duration: int
    description: str
    saved_times: int
    authors: List[mArtist]
    
    def add_attribute(self, key: str, value: str):
        #> similar_content
        #? List of similar content, normally 5 unless user specifies otherwise
        setattr(self, key, value)
        
class Artist:
    id_: str
    url: str
    name: str
    followers: int
    is_verified: bool
    monthly_listeners: int
    listeners_location: dict
    
    def add_attribute(self, key: str, value: str):
        #> popular_tracks | popular_discography
        #? List of popular |albums/tracks| normally 5 unless user specifies otherwise
        setattr(self, key, value)

class Album: 
    id_: str
    url: str
    name: str
    duration: int
    release_date: str
    tracks: List[mTrack]
    artists: List[mArtist]
    
    def add_attribute(self, key: str, value: str):
        #> artist_other_albums
        #? List of other albums by the artist, normally 5 unless user specifies otherwise
        setattr(self, key, value)
    
#% Minified version of the track class 
class mTrack: 
    id_: str
    url: str
    name: str
    artists: List[mArtist]
    duration: int #? Should be in seconds
    
    def add_attribute(self, key: str, value: str):
        #> added_date | album | streams
        #? added_date is the date the track was added to the playlist, album is the album the track belongs to, streams is the number of streams the track has
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
    
    def add_attribute(self, key: str, value: str):
        #> is_single | release_year
        #? is_single is a boolean value, release_year is the year the album was released
        setattr(self, key, value)