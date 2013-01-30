from django.db import models

class Partida(models.Model):
    nome = models.CharField(max_length=30)
    num_players = models.IntegerField()

class JogandoPartida(models.Model):
    user = models.OneToOneField('auth.User')
    partida = models.ForeignKey(Partida)
