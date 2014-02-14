from django.db import models

class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

class Topic(models.Model):
    author = models.ForeignKey('UserProfile', related_name='topics')
    text = models.TextField()
    
