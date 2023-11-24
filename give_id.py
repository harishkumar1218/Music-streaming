from main import db, songs
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas

data = pandas.read_csv('songs.csv')
data = data.to_dict('records')
song_names = [i['name'] for i in data]
dir = '//home//emmaykoushal//SpotiFlyer//Playlists//Hindi_Item_Songs___Top_100_Hits'
files = os.listdir(dir)
for song in files:
    downloaded_name = song.replace('_', ' ')
    downloaded_name = downloaded_name.replace('.mp3', '')
    print(downloaded_name)
    max_ratio = 50
    song_id = -1
    for i in range(498, 593):
        # db_song_name = songs.query.filter_by(id=i).first().song_name 
        ratio = fuzz.ratio(song_names[i], downloaded_name)
        print(ratio)
        #print(db_song_name, " --> ", ratio)
        if ratio > max_ratio:
            max_ratio = ratio
            song_id = i

    print(song_id)
    if song_id == -1:
        print(song, " is not found")
    else:
        old = dir+'//'+song
        new = dir+'//'+str(song_id)+'.mp3'
        old = old.replace('//', '/')
        new = new.replace('//', '/')
        #print(old)
        #print(new)
        os.rename(old, new)