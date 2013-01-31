from django.db import models
from django.contrib.auth.models import User

class Partida(models.Model):
    nome = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nome

class JogandoPartida(models.Model):
    user = models.ForeignKey(User)
    partida = models.ForeignKey(Partida)

    def __unicode__(self):
        return '{1}: {0}'.format(self.user.get_full_name(), self.partida.nome)
