# filter.py

import sqlite3

DB_NAME = 'music_store.db'

def get_unique_artists():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM artists")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return ['Все'] + result

def get_unique_genres():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT genre FROM tracks")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return ['Все'] + result

def filter_tracks(artist='Все', genre='Все'):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = """
    SELECT tracks.id, tracks.title, artists.name, tracks.album, tracks.genre, tracks.price
    FROM tracks JOIN artists ON tracks.artist_id=artists.id
    WHERE 1=1
    """
    params = []
    if artist != 'Все':
        query += " AND artists.name=?"
        params.append(artist)
    if genre != 'Все':
        query += " AND tracks.genre=?"
        params.append(genre)
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result