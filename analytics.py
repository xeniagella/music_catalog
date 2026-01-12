# analytics.py

import storage
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from filter import DB_NAME
import tkinter


def get_total_revenue():
    conn = storage.create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(tracks.price)
        FROM sales JOIN tracks ON sales.track_id = tracks.id
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result if result else 0

def get_total_sales_count():
    conn = storage.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def load_sales_data():
    conn = storage.create_connection()
    df_sales = pd.read_sql_query("SELECT * FROM sales", conn)
    df_tracks = pd.read_sql_query("SELECT * FROM tracks", conn)
    df_artists = pd.read_sql_query("SELECT * FROM artists", conn)
    conn.close()
    return df_sales, df_tracks, df_artists

def plot_revenue_over_time():
    sales_df, tracks_df, _ = load_sales_data()
    df = sales_df.merge(tracks_df, left_on='track_id', right_on='id')
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    daily_revenue = df.groupby(df['sale_date'].dt.date)['price'].sum()

    plt.figure(figsize=(10,5))
    daily_revenue.plot()
    plt.title('Доход за период')
    plt.xlabel('Дата')
    plt.ylabel('Общий доход')
    plt.show()

def show_sales_for_track(track_id):
    df_sales, df_tracks, df_artists = load_sales_data()
    df = df_sales.merge(df_tracks, left_on='track_id', right_on='id')
    df_track_sales = df[df['track_id'] == track_id]
    title = df_track_sales['title'].iloc[0] if not df_track_sales.empty else 'не найдено'
    print(f"Продажи для трека ID = {track_id} ({title}): {len(df_track_sales)} раз")
    if not df_track_sales.empty:
        df_track_sales = df_track_sales.copy()
        df_track_sales['sale_date'] = pd.to_datetime(df_track_sales['sale_date'])
        df_track_sales.groupby(df_track_sales['sale_date'].dt.date)['track_id'].count().plot(kind='bar')
        plt.title(f'Продажи трека ID {track_id}')
        plt.xlabel('Дата')
        plt.ylabel('Количество продаж')
        plt.show()

def show_total_revenue():
    df_sales, df_tracks = load_sales_data()
    df = df_sales.merge(df_tracks, left_on='track_id', right_on='id')
    total = df['price'].sum()
    print(f"Общий доход  за период: {total:.2f}")
    plt.figure(figsize=(6,4))
    plt.text(0.5,
             0.5,
             f"Общий доход:\n{total:.2f} у.е.",
             ha='center',
             va='center',
             fontsize=16)
    plt.axis('off')
    plt.show()

def show_total_sales_count():
    df_sales, df_tracks, df_artists = load_sales_data()
    count = len(df_sales)
    print(f"Общее число продаж: {count}")
    plt.figure(figsize=(6,4))
    plt.text(0.5,
             0.5,
             f"Число продаж:\n{count}",
             ha='center',
             va='center',
             fontsize=16)
    plt.axis('off')
    plt.show()


"""def show_sales_by_selected_artist(artist_name):
    df_sales, df_tracks, df_artists = load_sales_data()
    print("Колонки df_tracks:", df_tracks.columns)
    print("Колонки df_artists:", df_artists.columns)
    df_tracks_artists = df_tracks.merge(df_artists, on='id')
    artist_row = df_artists[df_artists['name'] == artist_name]
    if artist_row.empty:
        return f"Артист '{artist_name}' не найден."
    artist_id = artist_row['id'].iloc[0]

    df_full = df_sales.merge(df_tracks_artists, left_on='track_id', right_on='id')
    df_artist_sales = df_full[df_full['name'] == artist_name]

    total_sales = len(df_artist_sales)
    total_revenue = df_artist_sales['price'].sum()

    msg = f"Продажи исполнителя '{artist_name}':\n" \
          f"Количество треков: {total_sales}\n" \
          f"Общий доход: {total_revenue:.2f} у.е."

    return msg"""

def show_sales_by_selected_artist(artist_name):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Нет выбранной строки", "Выберите строку таблицы.")
        return
    row_values = tree.item(selected)['values']
    artist_name = row_values[2]
    msg = analytics.show_sales_by_artist(artist_name)
    messagebox.showinfo("Продажи исполнителя", msg)