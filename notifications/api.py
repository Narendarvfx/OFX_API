from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Notifications
from notifications.serializers import NotificationsSerializer


class NotificationsDetail(APIView):

    def get(self, request, format=None):
        notification = Notifications.objects.all().order_by('-sent_date')
        serializer = NotificationsSerializer(notification, many=True, context={"request":request} )
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NotificationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationsUnread(APIView):

    def get(self, request,userId, format=None):
        notification = Notifications.objects.filter(read=False, to=userId).order_by('-sent_date')
        serializer = NotificationsSerializer(notification, many=True, context={"request":request} )
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NotificationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)