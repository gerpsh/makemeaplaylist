import json
import urllib2
import random
from pandas import DataFrame
from sklearn import linear_model

songs_data = json.loads(urllib2.urlopen('http://104.236.246.87/playlist/get-all-songs/').read())['data']

songs = []

num_songs = int(raw_input("How many songs do you want in this playlist? "))
print("Enter y if you want the song,\nn if you don't,\nd if you don't know the song,\nand x if you want to stop")

resp = ''
while resp != 'x':
    current_song = random.choice(songs_data)
    artist = current_song['artist']
    title = current_song['title']
    resp = raw_input('Would you put {} by {} on your playlist? '.format(title.encode('utf-8'), artist.encode('utf-8')))
    if resp == 'y':
        current_song['include'] = 1
        songs.append(current_song)
    elif resp == 'n':
        current_song['include'] = 0
        songs.append(current_song)

frame = DataFrame(songs)
predictors = frame[['songHotness', 'artistHotness', 'artistFamiliarity', 'danceability', 'energy', 'tempo']]
outcome = frame['include']
model = linear_model.LogisticRegression()
model.fit(predictors, outcome)

for song in songs_data:
    song_data = [song['songHotness'], song['artistHotness'], song['artistFamiliarity'], song['danceability'], song['energy'], song['tempo']]
    positive_prob = model.predict_proba(song_data)[0][1]
    song['log_prob'] = positive_prob

songs_data = reversed(sorted(songs_data, key=lambda x: x['log_prob']))
for i, song in enumerate(songs_data):
    if i < num_songs:
        print('{}. {} - {}'.format((i+1), song['title'].encode('utf-8'), song['artist'].encode('utf-8')))