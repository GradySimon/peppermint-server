from peppermint_server.models import UserProfile, Topic

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name')

class TopicSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(many=False)

    class Meta:
        model = Topic
        fields = ('id', 'author', 'text')