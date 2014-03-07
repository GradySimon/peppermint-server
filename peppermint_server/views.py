from django.shortcuts import get_object_or_404
from peppermint_server.models import UserProfile, Topic
from peppermint_server.serializers import UserProfileSerializer, TopicSerializer
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
