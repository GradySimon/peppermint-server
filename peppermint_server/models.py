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
    topic_author = models.ForeignKey('UserProfile', related_name='initiated_conversations')
    other_party = models.ForeignKey('UserProfile', related_name='received_conversations')
    start_date = models.DateTimeField(auto_now_add=True)

    # Should error check for party not being part of this conversation
    def get_counterparty_to(self, party):
        if party == self.topic_author:
            return self.other_party
        if party == self.other_party:
            return self.topic_author

    def to_client_representation(self, client_party):
        counterparty = self.get_counterparty_to(client_party)
        return self.ClientRepresentation(self.pk, self.topic.pk, counterparty.pk)

    class ClientRepresentation:
        def __init__(self, conversation_id, topic_id, counterparty_id):
            self.conversation_id = conversation_id
            self.topic_id = topic_id
            self.counterparty_id = counterparty_id

        def to_conversation(self, client_id):
            if self.conversation_id == -3: # -1 is what clients set id to if they have just created it. TODO: make this more robust
                topic = Topic.objects.get(pk=self.topic_id)
                topic_author = topic.author
                other_party = UserProfile.objects.get(pk=client_id)
                return Conversation(topic=topic, topic_author=topic_author, other_party=other_party)
            return Conversation.objects.get(pk=self.conversation_id)

class Message(models.Model):
    conversation = models.ForeignKey('Conversation', related_name='messages')
    sender = models.ForeignKey('UserProfile')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def recipient(self):
        if self.sender == self.conversation.topic_author:
            return self.conversation.other_party
        else:
            return self.conversation.topic_author

    def to_client_representation(self, client_party):
        from_counterparty = None
        if client_party == self.sender:
            from_counterparty = False
        elif client_party == self.recipient:
            from_counterparty = True
        else:
            raise Exception
        return self.ClientRepresentation(self.pk, self.conversation.pk, from_counterparty, self.text)

    class ClientRepresentation:
        def __init__(self, message_id, conversation_id, from_counterparty, text):
            self.message_id = message_id
            self.conversation_id = conversation_id
            self.from_counterparty = from_counterparty
            self.text = text

        def to_message(self, client_id):
            """
            Returns the Message that this ClientRepresentation is based on, or creates a new
            Message if it doesn't exist (i.e. it's new from a client)
            """
            if self.message_id == -3: # -1 is what clients set id to if they have just created it. TODO: make this more robust
                conversation = Conversation.objects.get(pk=self.conversation_id)
                sender = UserProfile.objects.get(pk=client_id)
                text = self.text
                return Message(conversation=conversation, sender=sender, text=text)
            return Message.objects.get(pk=self.message_id)