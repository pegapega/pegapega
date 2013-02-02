# -*- coding: utf-8 -*-
import requests

from django.http import HttpResponse
from django.views.generic import ListView, CreateView
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404

from forms import UploadPhotoForm
from accounts.models import UserProfile
from partidas.models import Partida, JogandoPartida


@csrf_exempt
@login_required
def alvo(request, partida_id):
    fb_user = UserProfile.objects.get(user=request.user)
    partida = get_object_or_404(Partida, pk=partida_id)
    proximo_alvo = partida.proximo_alvo(request.user)

    if partida.n_jogadores() <= 1:
        return render(request, 'partidas/win.html', {
            'partida': partida,
        })

    if request.method == 'GET':
        foto_do_alvo = 'http://graph.facebook.com/'+proximo_alvo.profile.facebook_id+'/picture?type=large'

        return render(request, 'partidas/alvo.html', {
            'partida': partida,
            'alvo': proximo_alvo,
            'foto_do_alvo': foto_do_alvo
        })

    elif request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():

            files = {'source': request.FILES['file']}

            mensagem = request.user.get_full_name()+u' acaba de pegar '+proximo_alvo.get_full_name()+u'. Quer jogar também? http://pegapega.seocam.com'

            r_post_photo = requests.post('https://graph.facebook.com/me/photos', params={
                    'access_token': fb_user.access_token,
                    'name': mensagem,
                }, files=files)

            picture_id = r_post_photo.json()['id']
            if picture_id:
                partida.matar(proximo_alvo)

            r_tag_photo = requests.post('https://graph.facebook.com/'+picture_id+'/tags', params={
                    'access_token': fb_user.access_token,
                    'to': proximo_alvo.profile.facebook_id
                })

        return redirect('alvo', partida_id=partida.id)


class PartidasListView(ListView):
    model = Partida
    template_name = 'partidas/list.html'

    def get_queryset(self):
        queryset = super(PartidasListView, self).get_queryset()
        queryset = queryset.filter(jogandopartida__user=self.request.user,
                                   jogandopartida__vivo=True).order_by('-id')
        return queryset


@csrf_exempt
@login_required
def partida_create(request):

    if request.method == 'GET':

        fb_user = UserProfile.objects.get(user=request.user)

        amigos_jogadores = requests.get('https://graph.facebook.com/me/friends', params={
                'access_token': fb_user.access_token,
                # 'fields': 'accounts'
        })

        amigos_jogadores = amigos_jogadores.json()['data']

        amigos_ids = [amigo['id'] for amigo in amigos_jogadores]

        jogadores = User.objects.filter(profile__facebook_id__in=amigos_ids)

        return render(request, 'partidas/create.html', {
                'jogadores': jogadores,
            })
    elif request.method == 'POST':
        nome_partida = request.POST.get('partida')
        partida = Partida.objects.create(nome=nome_partida)
        jogadores = request.POST.getlist('jogadores')

        for jogador_id in jogadores:
            user = User.objects.get(pk=jogador_id)
            JogandoPartida.objects.create(partida=partida, user=user)

        JogandoPartida.objects.create(partida=partida, user=request.user)

        partida.embaralhar()

        return redirect('partida_list')

    return redirect('home')
