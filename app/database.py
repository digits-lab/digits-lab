import sqlite3

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect('music_library.db')
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn=None):
    close_conn = False
    if conn is None:
        conn = create_connection()
        close_conn = True

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, artist TEXT NOT NULL, album TEXT,
                genre TEXT, filepath TEXT NOT NULL UNIQUE, category TEXT NOT NULL, album_art_path TEXT,
                is_favorite INTEGER DEFAULT 0, downloaded INTEGER DEFAULT 0
            );''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE);''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlist_songs (
                playlist_id INTEGER NOT NULL, song_id INTEGER NOT NULL, PRIMARY KEY (playlist_id, song_id),
                FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE,
                FOREIGN KEY (song_id) REFERENCES songs (id) ON DELETE CASCADE
            );''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS recently_played (
                id INTEGER PRIMARY KEY AUTOINCREMENT, song_id INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (song_id) REFERENCES songs (id) ON DELETE CASCADE
            );''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_state (key TEXT PRIMARY KEY, value TEXT);''')
            cursor.execute("INSERT OR IGNORE INTO app_state (key, value) VALUES ('last_played_song_id', NULL)")
            cursor.execute("INSERT OR IGNORE INTO app_state (key, value) VALUES ('last_played_position', '0.0')")
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
        finally:
            if close_conn:
                conn.close()

# --- Refactored Functions ---

def add_song(title, artist, album, genre, filepath, category, album_art_path=None, is_favorite=0, downloaded=0, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    sql = ''' INSERT INTO songs(title, artist, album, genre, filepath, category, album_art_path, is_favorite, downloaded)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    last_id = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (title, artist, album, genre, filepath, category, album_art_path, is_favorite, downloaded))
        conn.commit()
        last_id = cur.lastrowid
    except sqlite3.IntegrityError:
        print(f"Song with filepath {filepath} already exists.")
    finally:
        if close_conn and conn: conn.close()
    return last_id

def get_all_songs(conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    rows = []
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM songs")
        rows = cur.fetchall()
    finally:
        if close_conn and conn: conn.close()
    return rows

def get_song_by_id(song_id, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    row = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM songs WHERE id=?", (song_id,))
        row = cur.fetchone()
    finally:
        if close_conn and conn: conn.close()
    return row

def get_songs_by_category(category, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    rows = []
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM songs WHERE category=?", (category,))
        rows = cur.fetchall()
    finally:
        if close_conn and conn: conn.close()
    return rows

def search_songs(query, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    rows = []
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM songs WHERE title LIKE ? OR artist LIKE ? OR album LIKE ?", (f'%{query}%', f'%{query}%', f'%{query}%'))
        rows = cur.fetchall()
    finally:
        if close_conn and conn: conn.close()
    return rows

def set_favorite_status(song_id, is_favorite, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    sql = 'UPDATE songs SET is_favorite = ? WHERE id = ?'
    try:
        cur = conn.cursor(); cur.execute(sql, (is_favorite, song_id)); conn.commit()
    finally:
        if close_conn and conn: conn.close()

def update_song_filepath_and_status(song_id, new_filepath, downloaded_status, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    sql = 'UPDATE songs SET filepath = ?, downloaded = ? WHERE id = ?'
    try:
        cur = conn.cursor(); cur.execute(sql, (new_filepath, downloaded_status, song_id)); conn.commit()
    finally:
        if close_conn and conn: conn.close()

def get_favorite_songs(conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    rows = []
    try:
        cur = conn.cursor(); cur.execute("SELECT * FROM songs WHERE is_favorite=1"); rows = cur.fetchall()
    finally:
        if close_conn and conn: conn.close()
    return rows

def create_playlist(name, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    sql = 'INSERT INTO playlists(name) VALUES(?)'
    last_id = None
    try:
        cur = conn.cursor(); cur.execute(sql, (name,)); conn.commit(); last_id = cur.lastrowid
    except sqlite3.IntegrityError: print(f"Playlist with name {name} already exists.")
    finally:
        if close_conn and conn: conn.close()
    return last_id

def get_playlists(conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    rows = []
    try:
        cur = conn.cursor(); cur.execute("SELECT * FROM playlists"); rows = cur.fetchall()
    finally:
        if close_conn and conn: conn.close()
    return rows

def delete_playlist(playlist_id, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    sql = 'DELETE FROM playlists WHERE id=?'
    try:
        cur = conn.cursor(); cur.execute(sql, (playlist_id,)); conn.commit()
    finally:
        if close_conn and conn: conn.close()

def rename_playlist(playlist_id, new_name, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    sql = 'UPDATE playlists SET name = ? WHERE id = ?'
    try:
        cur = conn.cursor(); cur.execute(sql, (new_name, playlist_id)); conn.commit()
    except sqlite3.IntegrityError: print(f"Playlist with name {new_name} already exists.")
    finally:
        if close_conn and conn: conn.close()

def add_song_to_playlist(playlist_id, song_id, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    sql = 'INSERT INTO playlist_songs(playlist_id, song_id) VALUES(?,?)'
    try:
        cur = conn.cursor(); cur.execute(sql, (playlist_id, song_id)); conn.commit()
    except sqlite3.IntegrityError: print(f"Song {song_id} is already in playlist {playlist_id}.")
    finally:
        if close_conn and conn: conn.close()

def get_songs_in_playlist(playlist_id, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    rows = []
    sql = "SELECT s.* FROM songs s JOIN playlist_songs ps ON s.id = ps.song_id WHERE ps.playlist_id = ?"
    try:
        cur = conn.cursor(); cur.execute(sql, (playlist_id,)); rows = cur.fetchall()
    finally:
        if close_conn and conn: conn.close()
    return rows

def remove_song_from_playlist(playlist_id, song_id, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    sql = 'DELETE FROM playlist_songs WHERE playlist_id=? AND song_id=?'
    try:
        cur = conn.cursor(); cur.execute(sql, (playlist_id, song_id)); conn.commit()
    finally:
        if close_conn and conn: conn.close()

def add_to_recently_played(song_id, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    sql = 'INSERT INTO recently_played(song_id) VALUES(?)'
    try:
        cur = conn.cursor(); cur.execute(sql, (song_id,)); conn.commit()
    finally:
        if close_conn and conn: conn.close()

def get_recently_played(limit=20, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    rows = []
    sql = "SELECT s.* FROM songs s JOIN recently_played rp ON s.id = rp.song_id ORDER BY rp.played_at DESC LIMIT ?"
    try:
        cur = conn.cursor(); cur.execute(sql, (limit,)); rows = cur.fetchall()
    finally:
        if close_conn and conn: conn.close()
    return rows

def get_app_state(key, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    row = None
    try:
        cur = conn.cursor(); cur.execute("SELECT value FROM app_state WHERE key=?", (key,)); row = cur.fetchone()
    finally:
        if close_conn and conn: conn.close()
    return row[0] if row else None

def set_app_state(key, value, conn=None):
    close_conn = conn is None
    if close_conn: conn = create_connection()
    sql = 'INSERT OR REPLACE INTO app_state (key, value) VALUES (?, ?)'
    try:
        cur = conn.cursor(); cur.execute(sql, (key, value)); conn.commit()
    finally:
        if close_conn and conn: conn.close()

if __name__ == '__main__':
    create_tables()
