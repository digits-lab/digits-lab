import unittest
import sqlite3
import sys
import os

# Add the app directory to the path to import database
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        """Set up a temporary, in-memory database for each test."""
        self.conn = sqlite3.connect(":memory:")
        database.create_tables(conn=self.conn)

    def tearDown(self):
        """Close the connection after each test."""
        self.conn.close()

    def test_add_and_get_song(self):
        """Test adding a song and retrieving it by its ID."""
        song_id = database.add_song("Gospel Title", "Gospel Artist", "Gospel Album", "Gospel", "path/song1.mp3", "Gospel", conn=self.conn)
        self.assertIsNotNone(song_id, "add_song should return an ID.")

        retrieved_song = database.get_song_by_id(song_id, conn=self.conn)
        self.assertIsNotNone(retrieved_song, "get_song_by_id should retrieve the added song.")
        self.assertEqual(retrieved_song[1], "Gospel Title")
        self.assertEqual(retrieved_song[2], "Gospel Artist")

    def test_set_favorite(self):
        """Test setting a song as a favorite and retrieving the favorites list."""
        song_id = database.add_song("Favorite Song", "An Artist", "An Album", "Pop", "path/fav.mp3", "Secular", conn=self.conn)
        database.set_favorite_status(song_id, 1, conn=self.conn)

        fav_songs = database.get_favorite_songs(conn=self.conn)
        self.assertEqual(len(fav_songs), 1, "There should be one favorite song.")
        self.assertEqual(fav_songs[0][0], song_id, "The favorite song's ID should match.")

    def test_update_download_status(self):
        """Test updating a song's download status and filepath."""
        song_id = database.add_song("Downloadable Song", "Artist", "Album", "Electronic", "path/online.mp3", "Secular", conn=self.conn)
        new_path = "offline_music/online.mp3"
        database.update_song_filepath_and_status(song_id, new_path, 1, conn=self.conn)

        updated_song = database.get_song_by_id(song_id, conn=self.conn)
        self.assertEqual(updated_song[5], new_path, "Filepath should be updated.")
        self.assertEqual(updated_song[9], 1, "Downloaded status should be updated to 1.")

    def test_create_and_rename_playlist(self):
        """Test creating a new playlist and then renaming it."""
        playlist_id = database.create_playlist("Oldies", conn=self.conn)
        self.assertIsNotNone(playlist_id)

        playlists = database.get_playlists(conn=self.conn)
        self.assertEqual(len(playlists), 1)
        self.assertEqual(playlists[0][1], "Oldies")

        database.rename_playlist(playlist_id, "Golden Oldies", conn=self.conn)
        renamed_playlists = database.get_playlists(conn=self.conn)
        self.assertEqual(renamed_playlists[0][1], "Golden Oldies", "Playlist name should be updated.")

    def test_add_and_remove_song_from_playlist(self):
        """Test adding a song to a playlist and then removing it."""
        song_id = database.add_song("Playlist Song", "Artist", "Album", "Rock", "path/pl.mp3", "Secular", conn=self.conn)
        playlist_id = database.create_playlist("Rock Anthems", conn=self.conn)

        database.add_song_to_playlist(playlist_id, song_id, conn=self.conn)
        playlist_songs = database.get_songs_in_playlist(playlist_id, conn=self.conn)
        self.assertEqual(len(playlist_songs), 1, "Song should be added to the playlist.")
        self.assertEqual(playlist_songs[0][0], song_id)

        database.remove_song_from_playlist(playlist_id, song_id, conn=self.conn)
        playlist_songs_after_removal = database.get_songs_in_playlist(playlist_id, conn=self.conn)
        self.assertEqual(len(playlist_songs_after_removal), 0, "Song should be removed from the playlist.")

    def test_app_state(self):
        """Test setting and getting an application state value."""
        database.set_app_state("volume", "100", conn=self.conn)
        value = database.get_app_state("volume", conn=self.conn)
        self.assertEqual(value, "100", "Should retrieve the correct state value.")

if __name__ == '__main__':
    unittest.main()
