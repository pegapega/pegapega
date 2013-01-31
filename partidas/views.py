from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from accounts.models import UserProfile

import requests

@login_required
def test(request):

    fb_user = UserProfile.objects.get(user=request.user)

    r = requests.get('https://graph.facebook.com/me/photos', params={
            'access_token': fb_user.access_token
        })

    user_accounts = r.text
    print user_accounts

    return render_to_response('partidas/test.html', {
        'facebook_id': fb_user.facebook_id,
    }, context_instance=RequestContext(request))