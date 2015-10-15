from playlist.models import *
import json

def run():
    songs = Song.objects.exclude(path__isnull=True)
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
            "path": song.path,
        }

        return s

    song_collection = list(map(serialize, songs))
    with open('dump.json', 'w') as f:
        f.write(json.dumps(song_collection,
            sort_keys=True, indent=4, separators=(',', ': ')))
