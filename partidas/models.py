from django.db import models
from django.contrib.auth.models import User

class Partida(models.Model):
    nome = models.CharField(max_length=30)
    num_players = models.IntegerField()

class JogandoPartida(models.Model):
    user = models.OneToOneField(User)
    partida = models.ForeignKey(Partida)
