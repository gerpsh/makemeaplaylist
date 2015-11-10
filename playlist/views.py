from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sys
import traceback
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
        "path": song.path
    }

    return s

#get a random song from the collection
def get_a_song(request):
    try:
        songs = Song.objects.all()
        song = random.choice(songs)
        song_data = serialize(song)
        song_data["status"] = 1
        response = json.dumps(song_data, indent=4, separators=(',', ': '))
        print(response)
        return HttpResponse(response, content_type="application/json")
    except:
        print "Unexpected error:", sys.exc_info()[0]
        response = json.dumps({"status": 0})
        return HttpResponse(response, content_type="application/json")

#get all of the songs from the collection
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

#get a song by name
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

#build logistic model
@csrf_exempt
def build_model(request):
    try:
        new_playlist = []
        songs = Song.objects.all()
        post_data = json.loads(request.body)
        songs_data = json.loads(request.body)['songs']
        desired_length = int(json.loads(request.body)['length'])
        frame = pandas.DataFrame(songs_data)
        predictors = frame[['songHotness', 'artistHotness', 'artistFamiliarity', 'danceability', 'duration', 'energy', 'tempo']]
        outcome = frame['include']
        #apply l1 penalty to diminish unimportant covariates
        model = linear_model.LogisticRegression(penalty='l1')
        model.fit(predictors, outcome)
        #r-squared score
        score = model.score(predictors, outcome)

        new_playlist = []
        for song in songs:
            song_data = [song.song_hotness, song.artist_hotness, song.artist_familiarity, song.danceability, song.duration, song.energy, song.tempo]
            #positive probability for each song
            positive_prob = model.predict_proba(song_data)[0][1]
            song_obj = {"title": song.title, "artist":song.artist, "prob": positive_prob}
            new_playlist.append(song_obj)

        #sort by probability
        new_playlist = list(reversed(sorted(new_playlist, key=lambda x:x['prob'])))
        new_playlist = new_playlist[:desired_length]
        response = json.dumps({"status":1, "songs": new_playlist, "score": score})
        return HttpResponse(response, content_type="application/json")

    except:
        print traceback.print_exc()
        response = json.dumps({"status": 0})
        return HttpResponse(response, content_type="application/json")


@csrf_exempt
def build_workout(request):
    from block import build_block, is_tempo_match

    post_data = json.loads(request.body)
    post_data = post_data['parameters']

    try:
        #grab post data, refactor this later
        section_one_upper = post_data['section1upper']
        section_one_lower = post_data['section1lower']
        section_one_cadence = post_data['section1cadence']
        section_one_obj = {
            "upper": section_one_upper,
            "lower": section_one_lower,
            "cadence": section_one_cadence
        }

        section_two_upper = post_data['section2upper']
        section_two_lower = post_data['section2lower']
        section_two_cadence = post_data['section2cadence']
        section_two_obj = {
            "upper": section_two_upper,
            "lower": section_two_lower,
            "cadence": section_two_cadence
        }

        section_three_upper = post_data['section3upper']
        section_three_lower = post_data['section3lower']
        section_three_cadence = post_data['section3cadence']
        section_three_obj = {
            "upper": section_three_upper,
            "lower": section_three_lower,
            "cadence": section_three_cadence
        }

        section_four_upper = post_data['section4upper']
        section_four_lower = post_data['section4lower']
        section_four_cadence = post_data['section4cadence']
        section_four_obj = {
            "upper": section_four_upper,
            "lower": section_four_lower,
            "cadence": section_four_cadence
        }

        section_five_upper = post_data['section5upper']
        section_five_lower = post_data['section5lower']
        section_five_cadence = post_data['section5cadence']
        section_five_obj = {
            "upper": section_five_upper,
            "lower": section_five_lower,
            "cadence": section_five_cadence
        }


        all_blocks = [
            section_one_obj,
            section_two_obj,
            section_three_obj,
            section_four_obj,
            section_five_obj]

        return_data = []
        duration = 600 #600s (10 minutes), algo starts to slow down past this point
        for block in all_blocks:
            upper = block['upper']
            lower = block['lower']
            tempo = block['cadence']
            #filter songs for energy and tempo
            #also filter songs for length > 1 min as well, we don't want songs
            #to be too short/rap album skits
            cands = Song.objects.filter(energy__range=(lower, upper)).filter(duration__gte=60)
            cands = [song for song in cands if is_tempo_match(tempo, song)]
            #see block.py
            song_block = build_block(cands, duration)
            songs = []
            for song in song_block:
                obj = {}
                obj['title'] = song.title
                obj['artist'] = song.artist
                obj['energy'] = float(song.energy)
                obj['tempo'] = int(song.tempo)
                obj['duration'] = int(song.duration)
                songs.append(obj)
            return_data.append(songs)
        response = json.dumps({"blocks": return_data, "status": 1})
        return HttpResponse(response, content_type="application/json")
    except:
        print traceback.print_exc()
        response = json.dumps({"status": 0})
        return HttpResponse(response, content_type="application/json")
