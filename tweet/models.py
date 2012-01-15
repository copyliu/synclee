from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    user = models.ForeignKey(User, related_name='tweet')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def get_reply_url(self):
        return '/tweet/reply_tweet/?tweet_id=%s' % self.id
    
    def get_absolute_url(self):
        return '/%s/' % self.user.username
    
    def get_name(self):
        if len(self.content) < 5:
            result = self.content
        else:
            result = self.content[:5]
        return result
    
    def get_del_url(self):
        return '/tweet/del_tweet/?tid=%s' % self.id
    
class TweetComment(models.Model):
    user = models.ForeignKey(User)
    tweet = models.ForeignKey(Tweet, related_name='comment')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)