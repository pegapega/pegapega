from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from accounts.models import UserProfile

import requests

@login_required
def take_photo(request):

    fb_user = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        files = {'source': open('/Users/neto/Pictures/xx.jpg', 'r')}


        r = requests.post('https://graph.facebook.com/me/photos', params={
                'access_token': fb_user.access_token
            }, files=files)


        print r
        return 'ok'


    else:

        files = {'source': open('/Users/neto/Pictures/xx.jpg', 'r')}


        r = requests.post('https://graph.facebook.com/me/photos', params={
                'access_token': fb_user.access_token
            }, files=files)


        print r
        return 'ok'

        # r = requests.get('https://graph.facebook.com/me/photos', params={
        #         'access_token': fb_user.access_token
        #     })

        # user_accounts = r.text
        # print user_accounts

        return render_to_response('partidas/camera.html', {
            # 'facebook_id': fb_user.facebook_id,
        }, context_instance=RequestContext(request))

