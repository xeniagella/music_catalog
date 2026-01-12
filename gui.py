# gui.py

import tkinter as tk
from tkinter import ttk, messagebox
import storage
import filter
import logic
import analytics
import matplotlib.pyplot as plt
import re

def validate_title(title):
    """
    Проверка корректности названия трека с помощью regex.

    :param title: Строка названия.
    :return: True, если название корректное, иначе False.
    """
    pattern = r"^[\w\s\-,ёЁА-Яа-я]+$"
    return re.match(pattern, title) is not None

def validate_price(price_str):
    """
    Проверка корректности цены.

    :param price_str: Ввод цены в виде строки.
    :return: True, если цена число, иначе False.
    """
    pattern = r"^\d+(\.\d+)?$"  # число с точкой
    return re.match(pattern, price_str) is not None

def refresh_table():
    """
    Обновляет таблицу отображения треков из базы данных.
    """
    logic.refresh_table_from_db(tree)

def run_filter():
    """
    Применяет выбранные фильтры по исполнителю и жанру,
    обновляет отображаемую таблицу треков.
    """
    artist = artist_cb.get()
    genre = genre_cb.get()
    print(f"Фильтр исполнитель = {artist}, жанр = {genre}")
    rows = filter.filter_tracks(artist, genre)
    print(f"Найдено записей: {len(rows)}")
    for r in rows:
        print(r)
    logic.update_table(tree, rows)

def add_new_track():
    """
    Открывает окно для добавления нового трека и сохраняет данные.
    """
    def save():
        title = entries['Название'].get()
        artist = entries['Исполнитель'].get()
        album = entries['Альбом'].get()
        genre = entries['Жанр'].get()
        price_str = entries['Цена'].get()

        if not validate_title(title):
            messagebox.showerror("Ошибка", "Некорректное название трека.")
            return
        if not validate_price(price_str):
            messagebox.showerror("Ошибка", "Некорректное значение цены.")
            return
        price = float(price_str)

 #       try:
 #           price = float(entries['Цена'].get())
 #       except:
 #           messagebox.showerror("Ошибка", "Некорректная цена")
 #           return

        logic.add_track_and_refresh(tree, title, artist, album, genre, price)
        artist_cb['values'] = filter.get_unique_artists()
        genre_cb['values'] = filter.get_unique_genres()
        artist_cb.current(0)
        genre_cb.current(0)
        run_filter()
        add_win.destroy()

    add_win = tk.Toplevel()
    add_win.title("Добавить трек")
    labels = ['Название', 'Исполнитель', 'Альбом', 'Жанр', 'Цена']
    entries = {}
    for i, lbl in enumerate(labels):
        tk.Label(add_win, text=lbl).grid(row=i, column=0, padx=5, pady=2, sticky='w')
        ent = tk.Entry(add_win)
        ent.grid(row=i, column=1, padx=5, pady=2)
        entries[lbl] = ent
    tk.Button(add_win, text="Сохранить", command=save).grid(row=5, column=0, columnspan=2, pady=5)

def show_total_revenue():
    """
    Показывает сообщение с общим доходом от продаж треков.
    """
    revenue = analytics.get_total_revenue()
    messagebox.showinfo("Общий доход", f"Общий доход от продаж: {revenue:.2f} у.е.")

def show_total_sales():
    """
    Показывает сообщение с количеством проданных треков.
    """
    count = analytics.get_total_sales_count()
    messagebox.showinfo("Общее число продаж", f"Общее число проданных треков: {count}")

def sell_selected_track():
    """
    Регистрирует продажу выбранного пользователем трека.
    """
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Нет выбранного трека", "Выберите трек для продажи")
        return
    track_id = tree.item(selected_item)['values'][0]
    storage.add_sale(track_id)
    messagebox.showinfo("Продано", "Трек продан")

def show_analysis():
    """
    Запускает и отображает график аналитики доходов за период.
    """
    analytics.plot_revenue_over_time()
    plt.show()

def show_track_sales():
    """
    Показывает график продаж для выбранного трека.
    """
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Не выбран трек", "Выберите трек для анализа")
        return
    track_id = tree.item(selected)['values'][0]
    analytics.show_sales_for_track(track_id)

def show_total_income():
    """
    Отображает информацию о суммарном доходе.
    """
    analytics.show_total_revenue()

def show_total_sales():
    """
    Отображает общее число продаж.
    """
    analytics.show_total_sales_count()

def show_sales_by_selected_artist():
    """
    Показывает отчёт о продажах выбранного исполнителя.
    """
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Нет выбранной строки", "Выберите строку таблицы.")
        return
    row_values = tree.item(selected)['values']
    artist_name = row_values[2]
    msg = analytics.show_sales_by_artist(artist_name)
    messagebox.showinfo("Продажи по исполнителю", msg)


root = tk.Tk()
root.title("Каталог музыки")

style = ttk.Style()
style.theme_use('default')

style.configure('Accent.TButton', background='#3498db', foreground='white', font=('Arial', 12, 'bold'))
style.map('Accent.TButton',
          background=[('active', '#2980b9')],
          foreground=[('active', 'white')])

style.configure('Success.TButton', background='#2ecc71', foreground='white', font=('Arial', 12, 'bold'))
style.map('Success.TButton',
          background=[('active', '#27ae60')],
          foreground=[('active', 'white')])

style.configure('Warning.TButton', background='#f39c12', foreground='white', font=('Arial', 12, 'bold'))
style.map('Warning.TButton',
          background=[('active', '#e67e22')],
          foreground=[('active', 'white')])

style.configure('Danger.TButton', background='#e74c3c', foreground='white', font=('Arial', 12, 'bold'))
style.map('Danger.TButton',
          background=[('active', '#c0392b')],
          foreground=[('active', 'white')])


top_frame = ttk.Frame(root)
top_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)


ttk.Label(top_frame, text='Исполнитель:').grid(row=0, column=0, padx=5, pady=2, sticky='w')
artist_cb = ttk.Combobox(top_frame, values=filter.get_unique_artists(), state='readonly')
artist_cb.current(0)
artist_cb.grid(row=0, column=1, padx=5, pady=2, sticky='w')

ttk.Label(top_frame, text='Жанр:').grid(row=0, column=2, padx=5, pady=2, sticky='w')
genre_cb = ttk.Combobox(top_frame, values=filter.get_unique_genres(), state='readonly')
genre_cb.current(0)
genre_cb.grid(row=0, column=3, padx=5, pady=2, sticky='w')


ttk.Button(top_frame, text="Фильтр", style='Accent.TButton', command=run_filter).grid(row=0, column=4, padx=5)
ttk.Button(top_frame, text="Сбросить", style='Success.TButton', command=refresh_table).grid(row=0, column=5, padx=5)
ttk.Button(top_frame, text="Добавить трек", style='Warning.TButton', command=add_new_track).grid(row=0, column=6, padx=5)


ttk.Button(top_frame, text="Общий доход", style='Info.TButton', command=show_total_revenue).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(top_frame, text="Число продаж", style='Info.TButton', command=show_total_sales).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(top_frame, text="Продать выбранный", style='Primary.TButton', command=sell_selected_track).grid(row=1, column=2, padx=5, pady=5)
ttk.Button(top_frame, text="Показать аналитику", style='Primary.TButton', command=show_analysis).grid(row=1, column=3, padx=5, pady=5)
ttk.Button(top_frame, text="Продажи по треку", style='Primary.TButton', command=show_track_sales).grid(row=1, column=4, padx=5, pady=5)
ttk.Button(top_frame, text="Продажи по исполнителю", style='Primary.TButton', command=show_sales_by_selected_artist).grid(row=1, column=5, padx=5)

columns = ('id', 'title', 'artist', 'album', 'genre', 'price')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)


root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)


refresh_table()
root.mainloop()