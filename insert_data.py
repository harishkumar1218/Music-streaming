from main import db, songs
import pandas

data = pandas.read_csv('songs.csv')
data = data[['name', 'URI', 'danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                'valence', 'tempo', 'artist_name', 'album', 'mood', 'language', 'category', 'dc0', 'dc1', 'dc2', 'dc3']]

dictlist = data.to_dict('records')
print("Converted to list")
def insert_songs(dictlist):
    for song in dictlist:
        Song = songs(
            song_name = song['name'],
            uri = song['URI'],
            danceability = song['danceability'],
            energy = song['energy'],
            key = song['key'],
            loudness = song['loudness'],
            speechiness = song['speechiness'],
            acousticness = song['acousticness'],
            instrumentalness = song['instrumentalness'],
            liveness = song['liveness'],
            valence = song['valence'],
            tempo = song['tempo'],
            artist_name = song['artist_name'],
            album = song['album'],
            mood = song['mood'],
            language = song['language'],
            category = song['category'],
            dc0 = song['dc0'],
            dc1 = song['dc1'],
            dc2 = song['dc2'],
            dc3 = song['dc3']
        )
        db.session.add(Song)
        db.session.commit()

insert_songs(dictlist)
# song = songs.query.filter_by(mood = "Sad").limit(10).all()
print("Done!!")
# for i in song:
#     print(i.song_name)
