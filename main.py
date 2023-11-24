from crypt import methods
from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from pygame import mixer
import time
from queue import Queue
import math
import random
import pandas 

mixer.init()
# REQUIRED VARIABLES DECLARATION STARTS HERE


# REQUIRED VARIABLES DECLARATION ENDS HERE
app = Flask(__name__)
app.config['SECRET_KEY'] = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///App.db'
app.config['SQLAlchemy_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

#OTHER FUNCTIONS STARTS HERE
def toString(recents):
    result = ""
    for i in recents:
        result = result + str(i) + " "
    result = result[:len(result)-1]
    return result

def Distance(center, avg_values):
    dist = 0
    for i in range(len(center)):
        dist += ((center[i] - avg_values[i]) * (center[i] - avg_values[i]))
    return math.sqrt(dist)

def GiveSongs(recents):
    if len(recents) > 0:
        recent_songs = []
        for i in range(len(recents)):
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
        # print(group1_song_ids)

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
        index = languages_count.index(max(languages_count))
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
            x = songs.query.filter_by(artist_name=artist, language=preffered_language, mood=preffered_mood).all()
            for i in x:
                group2_song_ids.append(i.id)

        g1 = group1_song_ids[:5]
        g2 = group2_song_ids
        if len(g2) > 5:
            g2 = group2_song_ids[:5]

        recommended_song_ids = g1 + g2
        # for i in range(5):
        #     recommended_song_ids.append(g1[i])
        #     recommended_song_ids.append(g2[i])
    else:
        recommended_song_ids = random.sample(range(1, 1000), 10)


    sad_song_list = songs.query.filter_by(mood='Sad').all()
    sad_songs_list = random.sample(sad_song_list, 30)
    sad_song_ids = []
    for i in sad_songs_list:
        sad_song_ids.append(i.id)
    sad_song_ids = [x for x in sad_song_ids if x not in recents]

    party_song_list = songs.query.filter_by(mood='Party').all()
    party_songs_list = random.sample(party_song_list, 30)
    party_song_ids = []
    for i in party_songs_list:
        party_song_ids.append(i.id)
    party_song_ids = [x for x in party_song_ids if x not in recents]

    romance_song_list = songs.query.filter_by(mood='Romance').all()
    romance_songs_list = random.sample(romance_song_list, 30)
    romance_song_ids = []
    for i in romance_songs_list:
        romance_song_ids.append(i.id)
    romance_song_ids = [x for x in romance_song_ids if x not in recents]

    set_get_recommended.set(recommended_song_ids)
    set_get_sad.set(sad_song_ids)
    set_get_romance.set(romance_song_ids)
    set_get_party.set(party_song_ids)

    print("RECOMMENDED SONGS: ",recommended_song_ids)
    print("SAD SONGS: ", sad_song_ids[:10])
    print("PARTY SONGS: ", party_song_ids[:10])
    print("ROMANCE SONGS: ", romance_song_ids[:10])
    print("RECENTLY PLAYED SONGS: ", recents[:10])

    return recommended_song_ids, sad_song_ids[:10], party_song_ids[:10], romance_song_ids[:10]


# OTHER FUNCTIONS ENDS HERE

#ALL DATABASE CODE
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))   
    recents = db.Column(db.String(100))
     
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(100), nullable=False)
    uri = db.Column(db.String(100), nullable=False, unique=True)
    danceability = db.Column(db.Float, nullable=False)
    energy = db.Column(db.Float, nullable=False)
    key = db.Column(db.Integer, nullable=False)
    loudness = db.Column(db.Float, nullable=False)
    speechiness = db.Column(db.Float, nullable=False)
    acousticness = db.Column(db.Float, nullable=False)
    instrumentalness = db.Column(db.Float, nullable=False)
    liveness = db.Column(db.Float, nullable=False)
    valence = db.Column(db.Float, nullable=False)  
    tempo = db.Column(db.Float, nullable=False)
    artist_name = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100), nullable=False)
    mood = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Float, nullable=False)
    dc0 = db.Column(db.Float, nullable=False)
    dc1 = db.Column(db.Float, nullable=False)
    dc2 = db.Column(db.Float, nullable=False)
    dc3 = db.Column(db.Float, nullable=False)


# class recently_played(db.Model):
#     id = db.Column(db.Integer, primary_key=True) 
#     song_id = db.Column(db.Integer, nullable=False)
#     song_mood = db.Column(db.String(100), nullable=False)
#     song_languages = db.Column(db.String(100), nullable=False)
#     song_artist = db.Column(db.String(100), nullable=False)
#     frequency = db.Column(db.Integer, nullable=False)

# DATABASE CODE ENDS HERE

# REQUIRED CALESS STARTS HERE

class Recents():
    def __init__(self):
        self.recents = []
    def set(self, recents):
        self.recents = recents

    def get(self):
        return self.recents
set_get_recents = Recents()

class Recommended():
    def __init__(self):
        self.recommended = []
    
    def set(self, recommended):
        self.recommended = recommended
    
    def get(self):
        return self.recommended
set_get_recommended = Recommended()

class Sad():
    def __init__(self):
        self.sad = []
    
    def set(self, sad):
        self.sad = sad
    
    def get(self):
        return self.sad
set_get_sad = Sad()

class Party():
    def __init__(self):
        self.party = []
    
    def set(self, party):
        self.party = party
    
    def get(self):
        return self.party
set_get_party = Party()

class Romance():
    def __init__(self):
        self.romance = []
    
    def set(self, romance):
        self.romance = romance
    
    def get(self):
        return self.romance
set_get_romance = Romance()

class SongStatus():
    def __init__(self):
        self.status = 0
    def get_status(self):
        return self.status
    def set_status(self, status):
        self.status = status

song_status = SongStatus()
rc_songs = [SongStatus(), SongStatus()]
rc_paused = [SongStatus(), SongStatus()]

recent_queue = Queue(maxsize=40)

class GetSetEmail():
    def set(self, email):
        self.email = email
    def get(self):
        return self.email
set_email = GetSetEmail()

class SetGetTime():
    def __init__(self):
        self.start = 0
        self.end = 0
    def set_start(self, start):
        self.start = start
    def set_end(self, end):
        self.end = end
    def get_start(self):
        return self.start
    def get_end(self):
        return self.end
set_get_time = SetGetTime()
#REQUIRED CLASSSES ENDS HERE

@app.route('/')
def index():
    mixer.music.stop()
    return render_template('index.html')

@app.route('/Home')
def Home():
    mixer.music.stop()
    if 'name' in session:
        name = session['name']
        return render_template('home.html',name=name)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods = ["POST", "GET"])
def login():
    mixer.music.stop()
    if request.method == 'POST':
        session.permanent = True
        email = request.form['email']
        password = request.form['pass']

        if email != "" and password != "":
            user = users.query.filter_by(email=email).first()
            if user.check_password(request.form['pass']):
                name = user.name 
                session['name'] = name
                set_email.set(user.email)
                return redirect(url_for('Home'))
            else:
                return render_template('Login.html', msg="Invalid Password !")
        else:
            return render_template('Login.html', msg="Please fill all the details!")
    else:
        if 'name' in session:
            return redirect(url_for('Home'))
        return render_template('Login.html', msg="")


@app.route('/SignUp', methods = ['POST', 'GET'])
def signup():
    mixer.music.stop()
    if request.method == 'POST':
        form = request.form
        count = users.query.filter_by(email=form['email']).count()
        if count == 0:  
            if form['name'] == "" or form['email'] == "" or form['pass'] == "":
                return render_template('SignUp.html', msg = "Please Fill All Details !")
            else:              
                user = users(
                    name = form['name'],
                    email = form['email'],
                    recents = "1"
                )
                user.set_password(form['pass'])
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
        else:
            return render_template('SignUp.html', msg = "Email Already Exists !")
    else:
        return render_template('SignUp.html', msg="")

@app.route('/music',methods = ['GET', 'POST'])
def music():
    categories =["Recommended Songs","Recently Played","Mass","Love","Sad"]
    # ALL MACHINE LEARNING PART SHOULD BE DONE HERE
    song_status.set_status(0)
    for i in rc_songs:
        i.set_status(0)
    for i in rc_paused:
        i.set_status(0)
    
    user_email = set_email.get()
    print(user_email)
    recent = users.query.filter_by(email=user_email).first()
    recent = recent.recents.split(" ")
    recents = [int(i) for i in recent]
    set_get_recents.set(recents)
    recent_song_ids = set_get_recents.get()
    recommended_song_ids, sad_song_ids, party_song_ids, romance_song_ids = GiveSongs(recents)
    #return render_template('music.html', recommended_song_ids=recommended_song_ids, sad_song_ids=sad_song_ids, party_song_ids=party_song_ids, romance_song_ids=romance_song_ids)
    return render_template('test.html', data = {'Recommended Songs': recommended_song_ids, 'Recently Played': recent_song_ids,'Sad': sad_song_ids, 'Party': party_song_ids, 'Romance': romance_song_ids})
@app.route('/logout')
def logout():
    mixer.music.stop()
    session.pop('name', None)
    return redirect(url_for('login'))

@app.route('/playsong',methods = ['GET', 'POST'])
def playsong():
    if request.method == 'POST':
        index_no = request.form.get("todo")
        print("PLAYING SONG OF INDEX NO: ", index_no)
        index_no  = int(index_no)
        song = songs.query.filter_by(id=index_no).first()
        song_name = song.song_name
        print("PLAYING SONG: ", song_name)
        link = "https://docs.google.com/uc?export=download&id=1lZGKX_dtBa8j3zkLxV18g5WhMylB6t_s"
        mixer.music.load(link)
        mixer.music.play()
        time.sleep(10)
        mixer.music.stop()
        
        
    return render_template('test.html')
# #background process happening without any refreshing
# @app.route('/rc1')
# def rc1():
#     index = 0
#     user = users.query.filter_by(email=set_email.get()).first()
#     recents = set_get_recents.get()
#     recommended_song_ids = set_get_recommended.get()
#     recents.append(recommended_song_ids[index])
#     if len(recents) > 40:
#         recents = recents[-40:]
#     result = toString(recents)
#     print(result)
#     user.recents = result
#     db.session.commit()
#     playing = song_status.get_status()
#     this_playing = rc_songs[index].get_status()
#     this_paused = rc_paused[index].get_status()

#     if playing == 0 and this_playing == 0 and this_paused == 0:
#         mixer.music.stop()
#         mixer.init()
#         mixer.music.load('/home/emmaykoushal/Documents/Toofan.mp3')
#         song_status.set_status(1)
#         for i in rc_songs:
#             i.set_status(0)
#         rc_songs[index].set_status(1)
#         mixer.music.play()

#     elif playing == 0 and this_playing == 0 and this_paused == 1:
#         song_status.set_status(1)   
#         for i in rc_songs:
#             i.set_status(0)
#         for i in rc_paused:
#             i.set_status(0)
#         rc_songs[index].set_status(1)
#         mixer.music.unpause()

#     elif playing == 1 and this_playing == 1:
#         song_status.set_status(0)
#         for i in rc_songs:
#             i.set_status(0)
#         for i in rc_paused:
#             i.set_status(0)
#         rc_paused[index].set_status(1)
#         mixer.music.pause()


#     elif playing == 1 and this_playing == 0:
#         mixer.music.stop()
#         mixer.init()
#         mixer.music.load('/home/emmaykoushal/Documents/Toofan.mp3')
#         song_status.set_status(1)
#         for i in rc_songs:
#             i.set_status(0)
#         rc_songs[index].set_status(1)
#         mixer.music.play()


# @app.route('/rc2')
# def rc2():
#     index = 1
#     user = users.query.filter_by(email=set_email.get()).first()
#     recents = set_get_recents.get()
#     recommended_song_ids = set_get_recommended.get()
#     recents.append(recommended_song_ids[index])
#     if len(recents) > 40:
#         recents = recents[-40:]
#     result = toString(recents)
#     print(result)
#     user.recents = result
#     db.session.commit()
#     playing = song_status.get_status()
#     this_playing = rc_songs[index].get_status()
#     this_paused = rc_paused[index].get_status()

#     if playing == 0 and this_playing == 0 and this_paused == 0:
#         mixer.music.stop()
#         mixer.init()
#         mixer.music.load('/home/emmaykoushal/Documents/Poolane.mp3')
#         song_status.set_status(1)
#         for i in rc_songs:
#             i.set_status(0)
#         rc_songs[index].set_status(1)
#         mixer.music.play()

#     elif playing == 0 and this_playing == 0 and this_paused == 1:
#         song_status.set_status(1)   
#         for i in rc_songs:
#             i.set_status(0)
#         for i in rc_paused:
#             i.set_status(0)
#         rc_songs[index].set_status(1)
#         mixer.music.unpause()

#     elif playing == 1 and this_playing == 1:
#         song_status.set_status(0)
#         for i in rc_songs:
#             i.set_status(0)
#         for i in rc_paused:
#             i.set_status(0)
#         rc_paused[index].set_status(1)
#         mixer.music.pause()


#     elif playing == 1 and this_playing == 0:
#         mixer.music.stop()
#         mixer.init()
#         mixer.music.load('/home/emmaykoushal/Documents/Poolane.mp3')
#         song_status.set_status(1)
#         for i in rc_songs:
#             i.set_status(0)
#         rc_songs[index].set_status(1)
#         mixer.music.play()

# @app.route('/playsong/<index>', methods=['GET','POST'])
# def playsong(index):
#     print(index)
#     user = users.query.filter_by(email=set_email.get()).first()
#     recents = set_get_recents.get()
#     recommended_song_ids = set_get_recommended.get()
#     recents.append(recommended_song_ids[index])
#     if len(recents) > 40:
#         recents = recents[-40:]
#     result = toString(recents)
#     print(result)
#     user.recents = result
#     db.session.commit()
#     playing = song_status.get_status()
#     this_playing = rc_songs[index].get_status()
#     this_paused = rc_paused[index].get_status()

#     if playing == 0 and this_playing == 0 and this_paused == 0:
#         mixer.music.stop()
#         mixer.init()
#         mixer.music.load('/home/emmaykoushal/Documents/Toofan.mp3')
#         song_status.set_status(1)
#         for i in rc_songs:
#             i.set_status(0)
#         rc_songs[index].set_status(1)
#         mixer.music.play()

#     elif playing == 0 and this_playing == 0 and this_paused == 1:
#         song_status.set_status(1)   
#         for i in rc_songs:
#             i.set_status(0)
#         for i in rc_paused:
#             i.set_status(0)
#         rc_songs[index].set_status(1)
#         mixer.music.unpause()

#     elif playing == 1 and this_playing == 1:
#         song_status.set_status(0)
#         for i in rc_songs:
#             i.set_status(0)
#         for i in rc_paused:
#             i.set_status(0)
#         rc_paused[index].set_status(1)
#         mixer.music.pause()


#     elif playing == 1 and this_playing == 0:
#         mixer.music.stop()
#         mixer.init()
#         mixer.music.load('/home/emmaykoushal/Documents/Toofan.mp3')
#         song_status.set_status(1)
#         for i in rc_songs:
#             i.set_status(0)
#         rc_songs[index].set_status(1)
#         mixer.music.play()


if __name__ == '__main__':
    app.run(debug=True)