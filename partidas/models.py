
from random import shuffle

from django.db import models
from django.contrib.auth.models import User


class JogandoPartida(models.Model):
    user = models.ForeignKey(User)
    partida = models.ForeignKey('Partida')
    vivo = models.BooleanField(default=True)
    codigo_partida = models.IntegerField(default=-1)

    def __unicode__(self):
        return '{1}: {0}'.format(self.user.get_full_name(), self.partida.nome)

    def save(self, *args, **kwargs):
        if self.codigo_partida == -1:
            partida = JogandoPartida.objects.filter(partida=self.partida)
            try:
                partida = partida.order_by("-codigo_partida")[0]
                max_codigo = partida.codigo_partida
            except (JogandoPartida.DoesNotExist, IndexError):
                max_codigo = -1

            self.codigo_partida = max_codigo + 1
        super(JogandoPartida, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('partida', 'user')


class Partida(models.Model):
    nome = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        if not self.nome:
            self.nome = '(partida sem nome)'
        return super(Partida, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.nome

    def jogadores_ativos(self):
        jp = JogandoPartida.objects.filter(partida=self, vivo=True)
        return jp.order_by('codigo_partida')

    def n_jogadores(self):
        return self.jogadores_ativos().count()

    def proximo_alvo(self, user):
        jp = self.jogadores_ativos()
        n = self.n_jogadores()
        jogandopartida = user.jogandopartida_set.get(partida=self)
        codigo_alvo = (jogandopartida.codigo_partida + 1) % n
        return jp[codigo_alvo].user

    def embaralhar(self):
        codes = range(self.jogandopartida_set.count())
        shuffle(codes)

        for i, jogador in enumerate(self.jogadores_ativos()):
            jogador.codigo_partida = codes[i]
            jogador.save()

    def matar(self, user):
        jp = proximo_alvo.jogandopartida_set.get(partida=partida)
        jp.vivo = False
        jp.save()

        jogadores_ativos = self.jogadores_ativos().order_by('codigo_partida')
        for i, jogador in enumerate(jogadores_ativos):
            jogador.codigo_partida = i
            jogador.save()

