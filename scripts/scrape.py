from library import MusicLibrary, EchoNestSongDatum
from playlist.models import *
from time import sleep

music_library = MusicLibrary("scripts/iTunesLibrary.xml")

replacements = {"Snoop Doggy Dogg": "Snoop Dogg", "Chance The Rapper": "Chance", "Jackson 5": "The Jacksons"}

def run():
    already_tried_file = open("scripts/already_tried.txt", "r")
    already_tried = already_tried_file.readlines()
    already_tried_file.close()
    already_tried = map(lambda x: x.strip('\n'), already_tried)

    def textify(song):
        return("Song not found: {} - {}".format(song.title.encode('utf-8'), song.artist.encode('utf-8')))


    for track in music_library.track_list:
        if not Song.objects.filter(title=track.title, artist=track.artist) and textify(track) not in already_tried:
            ensd = EchoNestSongDatum(title = track.title, artist = track.artist)
            try:
                ensd.get_data()
                if ensd.populated:
                    s = Song(
                        title=ensd.title,
                        artist=ensd.artist,
                        song_hotness=ensd.song_hotness,
                        artist_hotness=ensd.artist_hotness,
                        artist_familiarity=ensd.artist_familiarity,
                        danceability=ensd.danceability,
                        duration=ensd.duration,
                        energy=ensd.energy,
                        tempo=ensd.tempo
                    )

                    s.save()
                sleep(5)
            except:
                print("Socket broke, restarting")
                sleep(60)
                continue
