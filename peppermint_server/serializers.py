from rest_framework import serializers
from peppermint_server.models import UserProfile, Topic

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name')

class TopicSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(source='author', many=False, read_only=True)

    class Meta:
        model = Topic
        fields = ('id', 'author_id', 'text')