from django.shortcuts import render_to_response
from tweet.models import Status

def index(request):
    username = request.REQUEST.get('username', 'dilmabr')
    statuses = Status.objects.from_user(username)

    return render_to_response('index.html', {'statuses': statuses})
