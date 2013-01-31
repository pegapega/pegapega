
from __future__ import absolute_import

from django.contrib import admin
from .models import Partida, JogandoPartida

admin.site.register(Partida, admin.ModelAdmin)
admin.site.register(JogandoPartida, admin.ModelAdmin)
