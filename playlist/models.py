from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=300, null=False)
    artist = models.CharField(max_length=200, null=False)
    song_hotness = models.DecimalField(max_digits=12, decimal_places=11, null=True)
    artist_hotness = models.DecimalField(max_digits=12, decimal_places=11, null=True)
    artist_familiarity = models.DecimalField(max_digits=12, decimal_places=11, null=True)
    danceability = models.DecimalField(max_digits=12, decimal_places=11, null=True)
    duration = models.IntegerField(null=True)
    energy = models.DecimalField(max_digits=12, decimal_places=11, null=True)
    tempo = models.IntegerField(null=True)

    def __unicode__(self):
        return("{} -- {}".format(self.title, self.artist))

    class Meta:
        ordering = ('artist', 'title',)
        unique_together = ('artist', 'title',)

    def is_populated(self):
        return( self.song_hotness is not None and
                self.artist_hotness is not None and
                self.artist_familiarity is not None and
                self.danceability is not None and
                self.duration is not None and
                self.energy is not None and
                self.tempo is not None
              )
