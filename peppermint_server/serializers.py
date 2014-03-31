from rest_framework import serializers
from peppermint_server.models import UserProfile, Topic, Conversation, Message

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name')

class TopicSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(source='author', many=False)

    class Meta:
        model = Topic
        fields = ('id', 'author_id', 'text')

class ConversationSerializer(serializers.Serializer):
    conversation_id = serializers.IntegerField()
    topic_id = serializers.IntegerField()
    counterparty_id = serializers.IntegerField()

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.conversation_id = attrs.get('conversation_id', instance.conversation_id)
            instance.topic_id = attrs.get('topic_id', instance.topic_id)
            instance.counterparty_id = attrs.get('counterparty_id', instance.counterparty_id)
            return instance
        return Conversation.ClientRepresentation(**attrs)

class MessageSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    conversation_id = serializers.IntegerField()
    from_counterparty = serializers.BooleanField()
    text = serializers.CharField()

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.message_id = attrs.get('message_id', instance.message_id)
            instance.conversation_id = attrs.get('conversation_id', instance.conversation_id)
            instance.from_counterparty = attrs.get('from_counterparty', instance.from_counterparty)
            instance.text = attrs.get('text', instance.text)
        return Message.ClientRepresentation(**attrs)