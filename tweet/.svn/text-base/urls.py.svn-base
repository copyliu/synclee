from django.conf.urls.defaults import *

urlpatterns = patterns('synclee.tweet.views',
    url(r'^add_tweet/$', 'add_tweet', name='AddTweet'),
    url(r'^reply_tweet/$', 'reply_tweet', name='ReplyTweet'),
    url(r'^del_tweet/$', 'del_tweet', name='DelTweet'),
    url(r'^del_reply_tweet/$', 'del_tweet_reply', name='DelReplyTweet'),
    url(r'^refresh_tweet/(?P<username>[\w-]+)/$', 'refresh_person_tweet', name='RefreshPersonTweet'),
    url(r'^refresh_tweet/$', 'refresh_tweet', name='RefreshTweet'),
)