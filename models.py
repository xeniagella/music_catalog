# models.py

# Определяем класс Artist
class Artist:
    """
    Класс для представления исполнителя.
    """
    def __init__(self, name, country, genre):
        self.__name = name
        self.__country = country
        self.__genre = genre

    @property
    def name(self):
        """
        Возвращает имя исполнителя.
        """
        return self.__name

    @property
    def country(self):
        """
        Возвращает страну исполнителя.
        """
        return self.__country

    @property
    def genre(self):
        """
        Возвращает жанр исполнителя.
        """
        return self.__genre

    def __repr__(self):
        """
        Строковое представление Artist.
        """
        return f"Artist(name={self.__name}, country={self.__country}, genre={self.__genre})"

# Определяем класс MusicTrack
class MusicTrack:
    """
    Класс для представления музыкального трека.
    """
    def __init__(self, title, artist: Artist, album, genre, price):
        """
        Инициализация объекта MusicTrack.

        :param title: Название трека.
        :param artist: Исполнитель (объект Artist).
        :param album: Название альбома или None.
        :param genre: Жанр.
        :param price: Цена трека.
        """
        self.__title = title
        self.__artist = artist
        self.__album = album
        self.__genre = genre
        self.__price = price
        self.__listening_count = 0

    @property
    def title(self):
        """
        Возвращает название трека.
        """
        return self.__title

    @property
    def artist(self):
        """
        Возвращает исполнителя (объект Artist).
        """
        return self.__artist

    @property
    def album(self):
        """
        Возвращает название альбома или None.
        """
        return self.__album

    @property
    def genre(self):
        """
        Возвращает жанр трека.
        """
        return self.__genre

    @property
    def price(self):
        """
        Возвращает цену трека.
        """
        return self.__price

    @property
    def listening_count(self):
        """
        Возвращает количество прослушиваний трека.
        """
        return self.__listening_count

    def register_listening(self):
        """
        Увеличивает счетчик прослушиваний на 1.
        """
        self.__listening_count += 1

    def __repr__(self):
        """
        Строковое представление MusicTrack.
        """
        album_name = self.__album if self.__album else "Сингл (нет альбома)"
        return f"MusicTrack({self.__title}, {self.__artist.name}, альбом={album_name}, жанр={self.__genre}, цена={self.__price})"

class Sale:
    """
    Класс для учета продажи трека.
    """
    def __init__(self, track: MusicTrack, sale_date=None):
        """
        Инициализация объекта Sale.

        :param track: Проданный трек (объект MusicTrack).
        :param sale_date: Дата продажи. По умолчанию текущая.
        """
        self.__track = track
        self.__date = sale_date if sale_date else datetime.now()

    @property
    def track(self):
        """
        Возвращает трек, связанный с этой продажей.
        """
        return self.__track

    @property
    def date(self):
        """
        Возвращает дату продажи.
        """
        return self.__date

    def __repr__(self):
        """
        Строковое представление Sale.
        """
        return f"Sale(track={self.__track.title}, date={self.__date.strftime('%Y-%m-%d')})"

from datetime import datetime

class Listening:
    """
    Класс для учета прослушивания трека.
    """
    def __init__(self, track: MusicTrack, listen_date=None):
        """
        Инициализация объекта Listening.

        :param track: Прослушанный трек (объект MusicTrack).
        :param listen_date: Дата прослушивания. По умолчанию текущая.
        """
        self.__track = track
        self.__date = listen_date if listen_date else datetime.now()

    @property
    def track(self):
        """
        Возвращает трек, который был прослушан.
        """
        return self.__track

    @property
    def date(self):
        """
        Возвращает дату прослушивания.
        """
        return self.__date

    def __repr__(self):
        """
        Строковое представление Listening.
        """
        return f"Listening(track={self.__track.title}, date={self.__date.strftime('%Y-%m-%d')})"