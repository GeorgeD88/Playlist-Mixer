from spotipy.oauth2 import SpotifyOAuth
from myutils import *
import spotipy
import random


class SpotipyWrapper:

    # GET_MAX = 50
    ADD_MAX = 50

    def __init__(self, client_id, client_secret, redirect_uri, scopes):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scopes
        ))

    def my_id(self) -> str:
        """ Returns the authenticated user's ID. """
        return self.sp.current_user()['id']

    def get_playlist_tracks(self, playlist_id: str) -> list:
        """ Returns all tracks (IDs) in given playlist. """
        results = self.sp.playlist_tracks(playlist_id)
        plist_tracks = [item['track']['id'] for item in results['items']]
        if results['next']:
            for more_albums in page_results(self.sp, results):
                plist_tracks.extend(item['track']['id'] for item in more_albums['items'])
        return plist_tracks

    def new_playlist(self, playlist_name: str, public: bool = True, collaborative: bool = False, description: str = None):
        """ Creates new playlist with given info and returns playlist ID. """
        return self.sp.user_playlist_create(self.my_id(), playlist_name, public=public, collaborative=collaborative, description=description)['id']

    def add_playlist_tracks(self, playlist_id: str, tracks: list):
        """ Adds list of tracks to given playlist. """
        tracks_chunks = divide_chunks(tracks, self.ADD_MAX)
        for chunk in tracks_chunks:
            self.sp.playlist_add_items(playlist_id, chunk)

    def random_playlist_tracks(self, playlist_id: str, count: int) -> list:
        """ Returns N number of random tracks (IDs) from given playlist. """
        plist_tracks = self.get_playlist_tracks(playlist_id)

        # reduces count to the playlist length if count is larger
        plist_length = len(plist_tracks)
        if count > plist_length:
            count = plist_length

        return random.sample(plist_tracks, count)
