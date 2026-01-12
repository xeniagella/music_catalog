# storage.py

import sqlite3
from datetime import datetime
import tkinter


#def show_total_revenue():
#    db_name = 'music_store.db'

def create_connection(db_name='music_store.db'):
    """
    Создает подключение к базе данных SQLite.

    :param db_name: Имя файла базы данных.
    :return: Объект соединения или None при ошибке.
    """
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Не удалось подключиться к базе: {e}")
        return None

def init_db():
    """
    Инициализирует базу данных, создавая таблицы при необходимости.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        country TEXT,
        genre TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist_id INTEGER,
        album TEXT,
        genre TEXT,
        price REAL,
        FOREIGN KEY (artist_id) REFERENCES artists(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        track_id INTEGER,
        sale_date TEXT,
        FOREIGN KEY (track_id) REFERENCES tracks(id)
    )
    """)
    conn.commit()
    conn.close()

def add_artist(name, country, genre):
    """
    Добавляет нового исполнителя в базу.

    :param name: Имя исполнителя.
    :param country: Страна.
    :param genre: Жанр.
    """
    conn = sqlite3.connect('music_store.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO artists (name, country, genre) VALUES (?, ?, ?)", (name, country, genre))
    conn.commit()
    conn.close()

def add_track(title, artist_name, album, genre, price):
    """
    Добавляет новый трек в базу данных. При необходимости
    также создает нового исполнителя.

    :param title: Название трека.
    :param artist_name: Имя исполнителя.
    :param album: Название альбома или None.
    :param genre: Жанр.
    :param price: Цена.
    """
    conn = sqlite3.connect('music_store.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM artists WHERE name=?", (artist_name,))
    res = cursor.fetchone()
    if res:
        artist_id = res[0]
    else:
        cursor.execute("INSERT INTO artists (name) VALUES (?)", (artist_name,))
        artist_id = cursor.lastrowid
    cursor.execute("INSERT INTO tracks (title, artist_id, album, genre, price) VALUES (?, ?, ?, ?, ?)",
                   (title, artist_id, album, genre, price))
    conn.commit()
    conn.close()

def get_tracks():
    """
    Получает список всех треков из базы данных.

    :return: список кортежей с данными треков.
    """
    conn = sqlite3.connect('music_store.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT tracks.id, tracks.title, artists.name, tracks.album, tracks.genre, tracks.price
    FROM tracks JOIN artists ON tracks.artist_id=artists.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_sale(track_id):
    """
    Регистрирует продажу трека с указанным ID, добавляя запись
    в таблицу продаж с текущей датой.

    :param track_id: ID трека, который продается.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sales (track_id, sale_date) VALUES (?, ?)",
        (track_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    conn.commit()
    conn.close()