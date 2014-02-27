from django.db import models

class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    intersted_topics = models.ManyToManyField('Topic', through='Interest', related_name='interested_users')
    bored_topics = models.ManyToManyField('Topic', through='Boredom', related_name='bored_users')
    conversations = models.ManyToManyField('self', through='Conversation', symmetrical=False)

class Topic(models.Model):
    author = models.ForeignKey('UserProfile', related_name='topics')
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

class Interest(models.Model):
    user = models.ForeignKey('UserProfile')
    topic = models.ForeignKey('Topic')
    date = models.DateTimeField(auto_now=True)

class Boredom(models.Model):
    user = models.ForeignKey('UserProfile')
    topic = models.ForeignKey('Topic')
    date = models.DateTimeField(auto_now=True)

class Conversation(models.Model):
    topic = models.ForeignKey('Topic')
    initiator = models.ForeignKey('UserProfile', related_name='initiated_conversations')
    recipient = models.ForeignKey('UserProfile', related_name='received_conversations')
    start_date = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey('Conversation')
    sender = models.ForeignKey('UserProfile')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
