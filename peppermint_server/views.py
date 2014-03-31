from itertools import chain
from django.db.models import Q
from django.shortcuts import get_object_or_404
from peppermint_server.models import UserProfile, Topic, Conversation
from peppermint_server.serializers import UserProfileSerializer, TopicSerializer, ConversationSerializer, MessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TopicList(APIView):
    """
    List all topics, or create a new Topic.
    """
    def get(self, request, format=None):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TopicSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileDetail(APIView):
    """
    Get a single UserProfile.
    """
    def get(self, request, pk, format=None):
        user_profile = get_object_or_404(UserProfile, pk=pk)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
        
class UserProfileList(APIView):
    """
    List all UserProfiles, or create a new UserProfile.
    """
    def get(self, request, format=None):
        user_profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConversationList(APIView):
    """
    List all the user's conversations
    """
    def get(self, request, user_id, format=None):
        user_profile = get_object_or_404(UserProfile, pk=user_id)
        conversations = Conversation.objects.filter(
            Q(topic_author=user_profile) | Q(other_party=user_profile)
        )
        client_representations = [c.to_client_representation(user_profile) for c in conversations]
        serializer = ConversationSerializer(client_representations, many=True)
        return Response(serializer.data)

    def post(self, request, user_id, format=None):
        user_profile = get_object_or_404(UserProfile, pk=user_id)
        serializer = ConversationSerializer(data=request.DATA)
        if serializer.is_valid():
            client_representation = serializer.object
            new_conversation = client_representation.to_conversation(user_profile.pk)
            new_conversation.save()
            return_client_representation = new_conversation.to_client_representation(user_profile)
            return_serializer = ConversationSerializer(return_client_representation)
            return Response(return_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageList(APIView):
    """
    List all the user's messages
    """
    def get(self, request, user_id, format=None):
        user_profile = get_object_or_404(UserProfile, pk=user_id)
        conversations = Conversation.objects.filter(
            Q(topic_author=user_profile) | Q(other_party=user_profile)
        )
        messages_lists = [c.messages.all() for c in conversations]
        messages = chain.from_iterable(messages_lists)
        client_representations = [m.to_client_representation(user_profile) for m in messages]
        serializer = MessageSerializer(client_representations, many=True)
        return Response(serializer.data)

    def post(self, request, user_id, format=None):
        user_profile = get_object_or_404(UserProfile, pk=user_id)
        serializer = MessageSerializer(data=request.DATA)
        if serializer.is_valid():
            client_representation = serializer.object
            new_message = client_representation.to_message(user_profile.pk)
            new_message.save()
            return_client_representation = new_message.to_client_representation(user_profile)
            return_serializer = MessageSerializer(return_client_representation)
            return Response(return_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)