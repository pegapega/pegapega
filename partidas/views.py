from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse

from accounts.models import UserProfile
from forms import UploadPhotoForm

import requests

# @csrf_protect
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

