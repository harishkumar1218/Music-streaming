# # import pandas
# # import math
# # #from main import db
# # from sklearn.cluster import KMeans

# # data = pandas.read_csv('songs.csv')
# # data2 = data[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
# #                 'valence', 'tempo']]

# # model = KMeans(n_clusters = 4)
# # clusters = model.fit_predict(data2)

# # data['category'] = clusters
# # cluster_centers = model.cluster_centers_
# # print(cluster_centers)

# # def distance(lst, center):
# #     dist = 0
# #     for i in range(8):
# #         dist += ((lst[i] - center[i]) ** 2)
# #     return math.sqrt(dist)

# # dictlist = data.to_dict('records')

# # for song in dictlist:
# #     lst = [song['danceability'], song['energy'], song['loudness'], song['speechiness'], song['acousticness'], song['instrumentalness'],
# #                 song['valence'], song['tempo']]
# #     dist = []
# #     for z in range(4):
# #         dist.append(distance(lst, cluster_centers[z]))
# #     song['dc0'] = dist[0]
# #     song['dc1'] = dist[1]
# #     song['dc2'] = dist[2]
# #     song['dc3'] = dist[3]


# # features_dataframe = pandas.DataFrame.from_dict(dictlist)
# # features_dataframe.to_csv(r'Clusters.csv', index = False, header = True)


# import threading
# import random
# import math
# from main import db, songs, recently_played, users
# import numpy

# def Distance(center, avg_values):
#     dist = 0
#     for i in range(len(center)):
#         dist += ((center[i] - avg_values[i]) * (center[i] - avg_values[i]))
#     return math.sqrt(dist)

# rp_songs = recently_played.query.filter_by().all()
# rp_count = recently_played.query.filter_by().count()

# rp_danceability = 0.0
# rp_energy = 0.0
# rp_loudness = 0.0
# rp_speechiness = 0.0
# rp_acousticness = 0.0
# rp_instrumentalness = 0.0
# rp_valence = 0.0
# rp_tempo = 0.0

# for i in range(rp_count):
#     rp_song = songs.query.filter_by(id=rp_songs[i].song_id).first()
#     rp_danceability += rp_song.danceability
#     rp_energy += rp_song.energy
#     rp_loudness += rp_song.loudness
#     rp_speechiness += rp_song.speechiness
#     rp_acousticness += rp_song.acousticness
#     rp_instrumentalness += rp_song.instrumentalness
#     rp_valence += rp_song.valence
#     rp_tempo += rp_song.tempo

# avg_danceability = rp_danceability/rp_count
# avg_energy = rp_energy/rp_count
# avg_loudness = rp_loudness/rp_count
# avg_speechiness = rp_speechiness/rp_count
# avg_acousticness = rp_acousticness/rp_count
# avg_instrumentalness = rp_instrumentalness/rp_count
# avg_valence = rp_valence/rp_count
# avg_tempo = rp_tempo/rp_count

# avg_values = [avg_danceability, avg_energy, avg_loudness, avg_speechiness, avg_acousticness, avg_instrumentalness, 
#                 avg_valence, avg_tempo]

# cluster_centers = [[ 0.659498361,  0.668600000, -7.05169508,  0.0762845902,
#    0.375372459,  0.0226398562,  0.574961311,  135.194666],
#  [ 0.594505502,  0.618783172, -7.37893528,  0.0826200647,
#    0.448067379,  0.0212014872 , 0.527019094,  86.7751262],
#  [ 0.718204545,  0.697603571, -6.72354870,  0.0769487013,
#    0.340668149,  0.00844623649,  0.591697078 , 109.794604],
#  [ 0.538053435 , 0.652183206, -7.12552672,  0.114877863,
#    0.419069389,  0.00653270901,  0.544618321,  171.526519]]

# dist = 1000
# for i in range(len(cluster_centers)):
#     distance = Distance(cluster_centers[i], avg_values)
#     if distance < dist:
#         category = i
#         dist = distance

# print("Category is ", category)
# print("Distance is :", dist)
# category_songs = songs.query.filter_by(category=category).all()
# if category == 0:
#     info = [{'id': x.id, 'dist':abs(x.dc0 - dist)} for x in category_songs]
#     info = sorted(info, key=lambda x: x['dist'])
#     songs_ids = [info[x]['id'] for x in range(20)]
# elif category == 1:
#     info = [{'id': x.id, 'dist':abs(x.dc1 - dist)} for x in category_songs]
#     info = sorted(info, key=lambda x: x['dist'])
#     songs_ids = [info[x]['id'] for x in range(20)]
# elif category == 2:
#     info = [{'id': x.id, 'dist':abs(x.dc2 - dist)} for x in category_songs]
#     info = sorted(info, key=lambda x: x['dist'])
#     songs_ids = [info[x]['id'] for x in range(20)]
# else:
#     info = [{'id': x.id, 'dist':abs(x.dc3 - dist)} for x in category_songs]
#     info = sorted(info, key=lambda x: x['dist'])
#     songs_ids = [info[x]['id'] for x in range(20)]
# # print("Info about songs: ", info)

# rp_songs_ids = [rp_songs[x].song_id for x in range(rp_count)]
# final_song_ids = [x for x in songs_ids if x not in rp_songs_ids]
# # final_song_ids = [final_song_ids[i] for i in range(len(final_song_ids))]

# rp_sad_count = recently_played.query.filter_by(song_mood='Sad').count()
# rp_party_count = recently_played.query.filter_by(song_mood='Party').count()
# rp_romance_count = recently_played.query.filter_by(song_mood='Romance').count()

# print("Sad count: ", rp_sad_count, " party count: ", rp_party_count, " romance count: ", rp_romance_count)


# if rp_party_count > rp_sad_count:
#     if rp_party_count > rp_romance_count:
#         preffered_mood = 'Party'
#     else:
#         preffered_mood = 'Romance'
# else:
#     if rp_sad_count > rp_romance_count:
#         preffered_mood = 'Sad'
#     else:
#         preffered_mood = 'Romance'
# print("Preffered mood: ",  preffered_mood)

# rp_te_count = recently_played.query.filter_by(song_languages='te').count()
# rp_ta_count = recently_played.query.filter_by(song_languages='ta').count()
# rp_hi_count = recently_played.query.filter_by(song_languages='hi').count()
# rp_ma_count = recently_played.query.filter_by(song_languages='ma').count()

# rp_languages_count = [rp_te_count, rp_ta_count, rp_hi_count, rp_ma_count]
# print("Rp languages count: ",rp_languages_count)
# index = rp_languages_count.index(max(rp_languages_count))
# if index == 0:
#     preffered_language = 'te'
# elif index == 1:
#     preffered_language = 'ta'
# elif index == 2:
#     preffered_language = 'hi'
# else:
#     preffered_language = 'ma'

# print("Preffered Language: ", preffered_language)
# rp_artists = [x.song_artist for x in rp_songs]
# rp_artists_count = [{'name':x,'count':rp_artists.count(x)} for x in set(rp_artists)]
# rp_artists_count = sorted(rp_artists_count, key=lambda x:x['count'], reverse=True)

# print("Rp_artists_count: {}".format(rp_artists_count))
# preffered_artists = [rp_artists_count[i]['name'] for i in range(3)]
# print("Preffered artists:", preffered_artists)
# fs1 = songs.query.filter_by(artist_name=preffered_artists[0], language=preffered_language, mood=preffered_mood).all()
# fs2 = songs.query.filter_by(artist_name=preffered_artists[1], language=preffered_language, mood=preffered_mood).all()
# fs3 = songs.query.filter_by(artist_name=preffered_artists[2], language=preffered_language, mood=preffered_mood).all()
# final_songs = []

# for i in range(len(fs1)):
#     final_songs.append(fs1[i].id)
# for i in range(len(fs2)):
#     final_songs.append(fs2[i].id)
# for i in range(len(fs3)): 
#     final_songs.append(fs3[i].id)
# final_songs = [x for x in final_songs if x not in rp_songs_ids]
# print("Final songs:", final_songs)
# final_song_ids.append(final_songs)

# print("RECOMMENDED SONGS: ",final_song_ids)

# sad_song_list = songs.query.filter_by(mood='Sad').all()
# sad_songs = random.sample(sad_song_list, 30)
# sad_song_ids = []
# for i in sad_songs:
#     sad_song_ids.append(i.id)
# sad_song_ids = [x for x in sad_song_ids if x not in rp_songs_ids]

# party_song_list = songs.query.filter_by(mood='Party').all()
# party_songs = random.sample(party_song_list, 30)
# party_song_ids = []
# for i in party_songs:
#     party_song_ids.append(i.id)
# party_song_ids = [x for x in party_song_ids if x not in rp_songs_ids]

# romance_song_list = songs.query.filter_by(mood='Romance').all()
# romance_songs = random.sample(romance_song_list, 30)
# romance_song_ids = []
# for i in romance_songs:
#     romance_song_ids.append(i.id)
# romance_song_ids = [x for x in romance_song_ids if x not in rp_songs_ids]

# print("SAD SONGS: ", sad_song_ids)
# print("PARTY SONGS: ", party_song_ids)
# print("ROMANCE SONGS: ", romance_song_ids)
# print("RECENTLY PLAYED SONGS: ", rp_songs_ids)

# file1 = open('uris.txt', 'r')
# file2 = open('urls.txt', 'a')
# Lines = file1.readlines()

# for line in Lines:
#     parts = line.split(":")
#     line = "https://open.spotify.com/track/"+parts[len(parts)-1]
#     file2.write(line)
# file2.close()

# import os
# from main import db, songs

# file = open('urls.txt', 'r')
# Lines = file.readlines()

# for line in Lines:
#     os.system("spotdl "+line)



import os
from pathlib import Path

entries = Path('/home/emmaykoushal/Documents/MusicApp/songs/temp')

file1 = open('urls.txt', 'r')
urls = file1.readlines()
file2 = open('uris.txt', 'r')
uris = file2.readlines()
i = 0
for url in urls:
    #song = songs.query.filter_by(uri=uris[i]).first()
    id = i+1
    print(id)
    cmd = "Spotify_dl -l "+url+" -o /home/emmaykoushal/Documents/MusicApp/songs/temp"
    os.system(cmd)
    for entry in entries.iterdir():
        os.rename('/home/emmaykoushal/Documents/MusicApp/songs/temp/'+entry.name, '/home/emmaykoushal/Documents/MusicApp/songs/'+id+'.mp3')
        os.remove('/home/emmaykoushal/Documents/MusicApp/songs/temp/'+entry.name)
    i+=1