# PaylessMusicApi

PaylessMusicApi is a free and open-source API that allows you to access music data from various platforms without the constraints of paywalls. This project aims to provide developers with the tools they need to innovate and create amazing music-related applications.

## Features

- Access music data from Spotify, YouTube Music, SoundCloud, Deezer, and more.
- Retrieve detailed information about tracks, playlists, artists, and albums.
- Easy-to-use FastAPI-based endpoints.
- No paywalls or usage limits.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/LUXTACO/PaylessMusicApi.git
    cd PaylessMusicApi
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the application:
    ```sh
    uvicorn main:app --reload
    ```

## Usage

### Endpoints

- **Spotify**
  - [x] `/spotify/track?track_id={track_id}&get_raw={get_raw}`
  - [x] `/spotify/playlist?playlist_id={playlist_id}&offset={offset}&limit={limit}&get_raw={get_raw}`
  - [ ] `/spotify/artist?artist_id={artist_id}&get_raw={get_raw}`
  - [ ] `/spotify/album?album_id={album_id}&get_raw={get_raw}`

- **YouTube Music**
  - [ ] `/youtube_music/track?track_id={track_id}&get_raw={get_raw}`

### Example Request

To get a track from Spotify:
```sh
curl -X GET "http://localhost:8000/spotify/track?track_id=3n3Ppam7vgaVa1iaRUc9Lp&get_raw=false"
```

## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, feel free to open an issue or contact us at [tacomastabusiness@gmail.com].
