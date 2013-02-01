
import requests

from django.http import HttpResponse
from django.views.generic import ListView
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render_to_response, redirect, get_object_or_404

from forms import UploadPhotoForm
from accounts.models import UserProfile
from partidas.models import Partida, JogandoPartida


# @csrf_protect
@csrf_exempt
@login_required
def take_photo(request):
    fb_user = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():

            files = {'source': request.FILES['file']}

            r_post_photo = requests.post('https://graph.facebook.com/me/photos', params={
                    'access_token': fb_user.access_token,

                }, files=files)


            print r_post_photo.json()

            picture_id = r_post_photo.json()['id']

            r_tag_photo = requests.post('https://graph.facebook.com/'+picture_id+'/tags', params={
                    'access_token': fb_user.access_token,
                    'to': '710365352'
                })

            print r_tag_photo.text

        return redirect('take_photo')

    else:
        form = UploadPhotoForm()
        return render_to_response('partidas/camera.html', {
            'facebook_id': fb_user.facebook_id,
            'form': form
        }, context_instance=RequestContext(request))


class PartidasListView(ListView):
    model = Partida
    template_name = 'partidas/list.html'

    def get_queryset(self):
        queryset = super(PartidasListView, self).get_queryset()
        queryset = queryset.filter(jogandopartida__user=self.request.user)
        print queryset.count()
        return queryset
