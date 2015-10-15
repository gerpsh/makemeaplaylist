import xml.etree.ElementTree as et
import re
from time import sleep
from pyechonest import config
from secret import API_KEY
config.ECHO_NEST_API_KEY=API_KEY
from pyechonest import song

#suppress futurewarnings, this is the present homie
import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)

replacements = {
    "Snoop Doggy Dogg": "Snoop Dogg",
    "Chance The Rapper": "Chance",
    "Jackson 5": "The Jacksons",
    "D'Angelo & The Vanguard": "D'Angelo",
    "The Jimi Hendrix Experience": "Jimi Hendrix",
}

def replace_artist(artist):
    if artist in replacements:
        artist = replacements[artist]
    return artist

#artist and song title fields, with cleaning methods
class Track():
    def clean_title(self, title):
        #remove 'feat.' nonsense
        clean = re.split("\s\(?[Ff]?(ea)?t.?\s", title)[0].strip()
        return clean

    def is_music(self, xml_track):
        audio = False
        music = False
        for idx, val in enumerate(xml_track):
            if (val.text == "Kind") and ('MPEG audio file' in xml_track[idx+1].text):
                audio = True
            if (val.text == "Artist"):
                music = True
            if audio and music:
                return True
        return False

    def extract_data(self, xml_track):
        data = {}
        for idx, val in enumerate(xml_track):
            if val.text == "Artist":
                data['artist'] = xml_track[idx+1].text
            elif val.text == "Name":
                data['title'] = self.clean_title(xml_track[idx+1].text)
            elif val.text == "Location":
                data['path'] = xml_track[idx+1].text
        return data

    def __init__(self, xml_track=None):
        if xml_track:
            track_data = self.extract_data(xml_track)
            self.artist = track_data['artist']
            self.title = self.clean_title(track_data['title'])
            self.path = track_data['path']
        else:
            self.artist = None
            self.title = None
            self.path = None

#collection of Track objects
class MusicLibrary():

    def is_music(self, xml_track):
        audio = False
        music = True
        for idx, val in enumerate(xml_track):
            if (val.text == "Kind") and ('audio file' in xml_track[idx+1].text):
                audio = True
            if (val.text == "Podcast"):
                music = False
            if audio and music:
                return True
        return False

    def parse_lib(self, path):
        t = et.parse(path)
        tracks_raw = t.getroot()[0][15].findall('dict')
        tracks = [Track(track) for track in tracks_raw if self.is_music(track)]
        return tracks

    def __init__(self, path=None):
        if path:
            self.track_list = self.parse_lib(path)
        else:
            self.track_list = []

class EchoNestSongDatum():
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.populated = False


    def get_data(self):
        try:
            s = song.search(title=self.title, artist=replace_artist(self.artist))[0]
            self.song_hotness = s.song_hotttnesss
            self.artist_hotness = s.artist_hotttnesss
            self.artist_familiarity = s.artist_familiarity
            self.danceability = s.audio_summary['danceability']
            self.duration = s.audio_summary['duration']
            self.energy = s.audio_summary['energy']
            self.tempo = s.audio_summary['tempo']
            self.populated = True
        except IndexError:
            print("Song not found: {} - {}".format(self.title.encode('utf-8'), self.artist.encode('utf-8')))
            with open("scripts/already_tried.txt", "a") as f:
                f.write("Song not found: {} - {}".format(self.title.encode('utf-8'), self.artist.encode('utf-8')) + '\n')


    def __str__(self):
        return('{0} by {1}'.format(self.title.encode('utf8'), self.artist.encode('utf8')))
