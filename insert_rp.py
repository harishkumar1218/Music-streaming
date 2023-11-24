# from main import db, songs, recently_played
# import pandas
# import random

# data = pandas.read_csv('songs.csv')
# data2 = data[['mood', 'language', 'artist_name', 'URI']]

# dictlist = data2.to_dict('records')

# random_samples = random.sample(dictlist, 40)
# for song in random_samples:
#     sid = songs.query.filter_by(uri=song['URI']).first()
#     rp = recently_played(
#         song_id = sid.id,
#         song_mood = song['mood'],
#         song_languages = song['language'],
#         song_artist = song['artist_name'],
#         frequency = 1
#     )
#     db.session.add(rp)
#     db.session.commit()

import re
from main import set_get_recents, db, songs
import random
import math

# set_get_recents.set("1 2 22")
# recents = set_get_recents.get()
# recents = [int(i) for i in recents.split(" ")]

def Distance(center, avg_values):
    dist = 0
    for i in range(len(center)):
        dist += ((center[i] - avg_values[i]) * (center[i] - avg_values[i]))
    return math.sqrt(dist)

recents = random.sample(range(1,1000), 40)
# print(recents)

recent_songs = []
for i in range(40):
    recent_songs.append(songs.query.filter_by(id=recents[i]).first())

avg_danceability = 0.0
avg_energy = 0.0
avg_loudness = 0.0
avg_speechiness = 0.0
avg_acousticness = 0.0
avg_instrumentalness = 0.0
avg_valence = 0.0
avg_tempo = 0.0

for song in recent_songs:
    avg_danceability += song.danceability
    avg_energy += song.energy
    avg_loudness += song.loudness
    avg_speechiness += song.speechiness
    avg_acousticness += song.acousticness
    avg_instrumentalness += song.instrumentalness 
    avg_valence += song.valence
    avg_tempo += song.tempo

avg_values = [avg_danceability/len(recent_songs), avg_energy/len(recent_songs), avg_loudness/len(recent_songs), avg_speechiness/len(recent_songs), avg_acousticness/len(recent_songs), avg_instrumentalness/len(recent_songs), 
                avg_valence/len(recent_songs), avg_tempo/len(recent_songs)]


cluster_centers = [[ 0.659498361,  0.668600000, -7.05169508,  0.0762845902,
   0.375372459,  0.0226398562,  0.574961311,  135.194666],
 [ 0.594505502,  0.618783172, -7.37893528,  0.0826200647,
   0.448067379,  0.0212014872 , 0.527019094,  86.7751262],
 [ 0.718204545,  0.697603571, -6.72354870,  0.0769487013,
   0.340668149,  0.00844623649,  0.591697078 , 109.794604],
 [ 0.538053435 , 0.652183206, -7.12552672,  0.114877863,
   0.419069389,  0.00653270901,  0.544618321,  171.526519]]

dist = 1000
for i in range(len(cluster_centers)):
    distance = Distance(cluster_centers[i], avg_values)
    if distance < dist:
        category = i
        dist = distance

# print("Category is ", category)
# print("Distance is :", dist)

category_songs = songs.query.filter_by(category=category).all()
if category == 0:
    info = [{'id': x.id, 'dist':abs(x.dc0 - dist)} for x in category_songs]
    info = sorted(info, key=lambda x: x['dist'])
    songs_ids = [info[x]['id'] for x in range(40)]
elif category == 1:
    info = [{'id': x.id, 'dist':abs(x.dc1 - dist)} for x in category_songs]
    info = sorted(info, key=lambda x: x['dist'])
    songs_ids = [info[x]['id'] for x in range(40)]
elif category == 2:
    info = [{'id': x.id, 'dist':abs(x.dc2 - dist)} for x in category_songs]
    info = sorted(info, key=lambda x: x['dist'])
    songs_ids = [info[x]['id'] for x in range(40)]
else:
    info = [{'id': x.id, 'dist':abs(x.dc3 - dist)} for x in category_songs]
    info = sorted(info, key=lambda x: x['dist'])
    songs_ids = [info[x]['id'] for x in range(40)]

group1_song_ids = [x for x in songs_ids if x not in recents]
print(group1_song_ids)
sad_count = 0
party_count = 0
romance_count = 0
artists = []
languages = []
for song_id in recents:
    artists.append(songs.query.filter_by(id=song_id).first().artist_name)
    languages.append(songs.query.filter_by(id=song_id).first().language)
    if songs.query.filter_by(id=song_id).first().mood == 'Sad':
        sad_count += 1
    elif songs.query.filter_by(id=song_id).first().mood == 'Romance':
        romance_count += 1
    else:
        party_count += 1

# print("Sad count: ", sad_count, " party count: ", party_count, " romance count: ", romance_count)

if party_count > sad_count:
    if party_count > romance_count:
        preffered_mood = 'Party'
    else:
        preffered_mood = 'Romance'
else:
    if sad_count > romance_count:
        preffered_mood = 'Sad'
    else:
        preffered_mood = 'Romance'
 # print("Preffered mood: ",  preffered_mood)

artists_count = [{'name':x,'count':artists.count(x)} for x in set(artists)]
artists_count = sorted(artists_count, key=lambda x:x['count'], reverse=True)
preffered_artists = [artists_count[i]['name'] for i in range(3)]
# print("Preffered artists:", preffered_artists)

languages_count = [languages.count('te'), languages.count('ta'), languages.count('hi'), languages.count('ma')]
index = languages.index(max(languages))
if index == 0:
    preffered_language = 'te'
elif index == 1:
    preffered_language = 'ta'
elif index == 2:
    preffered_language = 'hi'
else:
    preffered_language = 'ma'

group2_song_ids = []
for artist in preffered_artists:
    x = songs.query.filter_by(artist_name=artist).all()
    for i in x:
        group2_song_ids.append(i.id)

g1 = group1_song_ids[:5]
g2 = group2_song_ids[:5]

recommended_song_ids = []
for i in range(5):
    recommended_song_ids.append(g1[i])
    recommended_song_ids.append(g2[i])



sad_song_list = songs.query.filter_by(mood='Sad').all()
sad_songs = random.sample(sad_song_list, 30)
sad_song_ids = []
for i in sad_songs:
    sad_song_ids.append(i.id)
sad_song_ids = [x for x in sad_song_ids if x not in recents]

party_song_list = songs.query.filter_by(mood='Party').all()
party_songs = random.sample(party_song_list, 30)
party_song_ids = []
for i in party_songs:
    party_song_ids.append(i.id)
party_song_ids = [x for x in party_song_ids if x not in recents]

romance_song_list = songs.query.filter_by(mood='Romance').all()
romance_songs = random.sample(romance_song_list, 30)
romance_song_ids = []
for i in romance_songs:
    romance_song_ids.append(i.id)
romance_song_ids = [x for x in romance_song_ids if x not in recents]

print("RECOMMENDED SONGS: ",recommended_song_ids)
print("SAD SONGS: ", sad_song_ids[:10])
print("PARTY SONGS: ", party_song_ids[:10])
print("ROMANCE SONGS: ", romance_song_ids[:10])
print("RECENTLY PLAYED SONGS: ", recents[:10])