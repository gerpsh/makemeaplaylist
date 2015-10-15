from library import MusicLibrary, Track
from playlist.models import *
import urllib

def run():
    ml = MusicLibrary('/Users/Jerry/Music/iTunes/iTunes Library.xml')
    for track in ml.track_list:
        matches = Song.objects.all().filter(artist=track.artist, title=track.clean_title(track.title))
        if matches:
            match = matches[0]
            match.path = track.path
            #match.path = urllib.unquote(track.path)
            match.save()
