from django.shortcuts import render
from .models import *
from django.http import HttpResponse
import sys
import json
import pandas
import random
from sklearn import linear_model
import traceback

def serialize(song):
    s = {
        "title": unicode(song.title),
        "artist": unicode(song.artist),
        "songHotness": float(song.song_hotness),
        "artistHotness": float(song.artist_hotness),
        "artistFamiliarity": float(song.artist_familiarity),
        "danceability": float(song.danceability),
        "duration": int(song.duration),
        "energy": float(song.energy),
        "tempo": int(song.tempo),
    }

    return s

def get_a_song(request):
    try:
        songs = Song.objects.all()
        song = random.choice(songs)
        song_data = serialize(song)
        song_data["status"] = 1
        response = json.dumps(song_data, indent=4, separators=(',', ': '))
        return HttpResponse(response, content_type="application/json")
    except:
        print "Unexpected error:", sys.exc_info()[0]
        response = json.dumps({"status": 0})
        return HttpResponse(response, content_type="application/json")

def get_all_songs(request):
    try:
        songs = Song.objects.all()
        song_data = map(serialize, songs)
        response_data = {"status": 1, "data": song_data}
        response = json.dumps(response_data, indent=4, separators=(',', ': '))
        return HttpResponse(response, content_type="application/json")
    except:
        print "Unexpected error:", sys.exc_info()[0]
        response = json.dumps({"status": 0})
        return HttpResponse(response, content_type="application/json")

def get_specific_song(request, title, artist):
    try:
        song = Song.objects.filter(title__iexact=title.replace("_", " "), artist__iexact=artist.replace("_", " "))[0]
        song_data = serialize(song)
        song_data["status"] = 1
        response = json.dumps(song_data)
        return HttpResponse(response, content_type="application/json")
    except:
        print "Unexpected error:", sys.exc_info()[0]
        response = json.dumps({"status": 0})
        return HttpResponse(response, content_type="application/json")

#uses logistic regression, add more models and aggregate later
def build_model(request):
    try:
        new_playlist = []
        songs = Song.objects.all()
        post_data = request.POST
        desired_length = int(post_data['length'])

        frame = pandas.read_json(post_data['data'])
        predictors = frame[['songHotness', 'artistHotness', 'artistFamiliarity', 'danceability', 'duration', 'energy', 'tempo']]
        outcome = frame['pick']
        model = linear_model.LogisticRegression()
        model.fit(predictors, outcome)

        for song in songs:
            song_data = [song.song_hotness, song.artist_hotness, song.artist_familiarity, song.danceability, song.duration, song.energy, song.tempo]
            positive_prob = model.predict_proba(song_data)[1]
            if positive_prob > 0.70 and len(new_playlist) < desired_length:
                song_obj = {"title": song.title, "artist":song.artist}
                new_playlist.append(song_obj)

        response = json.dumps({"status":1, "songs": return_playlist})
        return HttpResponse(response, content_type="application/json")

    except:
        response = json.dumps({"status": 0})
        return HttpResponse(response, content_type="application/json")
