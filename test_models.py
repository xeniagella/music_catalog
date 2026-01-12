# test_models.py

from models import Artist, MusicTrack, Sale, Listening

# создадим исполнителя
artist = Artist("Deceit", "Russia", "Metal/Rock")

# создадим трек
track = MusicTrack("Знамя Падших", artist, None, "Pop/Rock", 1.00)

# зафиксировали прослушивание
track.register_listening()

# создадим продажу
sale = Sale(track)

# создадим запись о прослушивании
listen = Listening(track)

# выведем объекты
print(artist)
print(track)
print(sale)
print(listen)

# проверим свойство прослушиваний
print(f"Количество прослушиваний: {track.listening_count}")
