from django.db import models


class Gra(models.Model):
    bgg_id = models.IntegerField(blank=True, null=True)
    tytul = models.CharField(max_length=255)
    min_graczy = models.IntegerField(blank=True, null=True)
    max_graczy = models.IntegerField(blank=True, null=True)
    czas_gry = models.IntegerField(blank=True, null=True)
    opis = models.TextField(blank=True, null=True)
    publikacja = models.IntegerField(blank=True, null=True)
    dodany = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tytul
