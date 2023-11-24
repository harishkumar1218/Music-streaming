import pandas
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


dir = '//home//emmaykoushal//SpotiFlyer//Playlists//Hindi_Item_Songs___Top_100_Hits'
data_frame = pandas.read_csv('songs.csv')
song_names_in_csv = list(data_frame.name)
song_names_in_csv = song_names_in_csv[497:592]
downloaded_song_names = os.listdir(dir)

for song in downloaded_song_names:
    downloaded_name = song.replace('_', ' ')
    downloaded_name = downloaded_name.replace('.mp3', '')
    status = False
    for song_name in song_names_in_csv:
        ratio = fuzz.ratio(song_name, downloaded_name)
        if ratio > 70:
            status = True   
            break
    
    if not status:
        file = dir+'//'+song
        file = file.replace('//', '/')
        os.remove(file)