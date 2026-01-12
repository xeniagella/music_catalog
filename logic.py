# logic.py

import storage
from filter import filter_tracks

def update_table(tree, rows):
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values=row)

def refresh_table_from_db(tree):
    rows = storage.get_tracks()
    update_table(tree, rows)

def apply_filter(tree, artist, genre):
    rows = filter_tracks(artist, genre)
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values=row)

def add_track_and_refresh(tree, title, artist, album, genre, price):
    storage.add_track(title, artist, album, genre, price)
    update_table(tree)