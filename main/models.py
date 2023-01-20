from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Thread(models.Model):

    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_pub = models.DateTimeField(verbose_name='Published at')
    content = models.TextField(max_length=500)
    votes = models.IntegerField(default=0)
    topic = models.ForeignKey('Topic', default="1", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def vote(self, inc_vote):
        self.votes += inc_vote
        self.save()


class Comment(models.Model):

    for_post = models.ForeignKey(Thread, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)

    def __str__(self):
        return "{0}: {1}".format(self.for_post, self.content)

class Topic(models.Model):

    topic_name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.topic_name.replace('"', '')

class Vote(models.Model):

    for_post = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


