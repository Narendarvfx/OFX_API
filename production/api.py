import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from production.models import Clients
from production.serializers import ClientSerializer


class ClientDetail(APIView):
    """
    This is for edit employee detail
    """

    def get(self, request, format=None):
        client = Clients.objects.all()
        serializer = ClientSerializer(client, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            client_dir = serializer.data['name']
            final_dir = os.path.join('C:/TestProject/Clients/', client_dir)
            os.makedirs(final_dir, exist_ok=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientUpdate(APIView):

    def get(self, request, client_id, format=None):
        client = Clients.objects.get(id=client_id)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, client_id):
        client = Clients.objects.get(id=client_id)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, client_id, format=None):
        model_object = Clients.objects.get(id=client_id)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)