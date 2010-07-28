from django.conf.urls.defaults import *

# http://api.twitter.com/1/users/show.xml?screen_name=dilmabr
urlpatterns = patterns('',
    url('', 'tweet.views.index'),
)
