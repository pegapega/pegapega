from django.db import models
from django.contrib.auth.models import User

class Partida(models.Model):
    nome = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nome


class JogandoPartida(models.Model):
    user = models.ForeignKey(User)
    partida = models.ForeignKey(Partida)
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
            except JogandoPartida.DoesNotExist:
                max_codigo = -1

            self.codigo_partida = max_codigo + 1
        super(JogandoPartida, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('partida', 'user')
