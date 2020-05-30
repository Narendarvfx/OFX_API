import os
import subprocess

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from production.models import Clients, Projects, Status, Shots, Complexity
from production.serializers import ClientSerializer, ProjectSerializer, StatusSerializer, ShotsSerializer, \
    ShotsPostSerializer


class StatusInfo(APIView):
    """
    This is for getting the Status info
    """

    def get(self, request, format=None):
        status = Status.objects.all()
        serializer = StatusSerializer(status, many=True, context={"request":request} )
        return Response(serializer.data)

class ComplexityInfo(APIView):
    """
    This is for getting the Status info
    """

    def get(self, request, format=None):
        complexity = Complexity.objects.all()
        serializer = ComplexitySerializer(status, many=True, context={"request":request} )
        return Response(serializer.data)

class ClientDetail(APIView):
    """
    This is for get and post client detail
    """

    def get(self, request, format=None):
        client = Clients.objects.select_related('status').all()
        serializer = ClientSerializer(client, many=True, context={"request":request} )
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            client_dir = serializer.data['name']
            final_dir = os.path.join('//192.168.4.114//R&D_Share//OFXSTORAGE//jobs//', client_dir)
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

class ProjectDetail(APIView):
    """
    This is for edit employee detail
    """

    def get(self, request, format=None):
        project = Projects.objects.all()
        serializer = ProjectSerializer(project, many=True, context={"request":request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            project_dir = serializer.data['name']
            final_dir = os.path.join('//192.168.4.114//R&D_Share//OFXSTORAGE//jobs//'+serializer.data['client'], project_dir)
            os.makedirs(final_dir, exist_ok=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectUpdate(APIView):

    def get(self, request, projectId, format=None):
        project = Projects.objects.get(id=projectId)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, projectId):
        project = Projects.objects.get(id=projectId)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, projectId, format=None):
        model_object = Projects.objects.get(id=projectId)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FileExplorer(APIView):

    def get(self, request, projectId):
        project = Projects.objects.get(id=projectId)
        serializer = ProjectSerializer(project)
        try:
            path = os.path.realpath("//192.168.4.114//R&D_Share//OFXSTORAGE//jobs//"+serializer.data['client']+"//"+serializer.data['name'])
            os.startfile(path)
        except Exception as e:
            print(e)
        return Response(serializer.data)

class ShotsData(APIView):
    """
    This is for edit employee detail
    """

    def get(self, request, format=None):
        shot = Shots.objects.all()
        serializer = ShotsSerializer(shot, many=True, context={"request":request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShotsPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # shot_dir = serializer.data['name']
            # final_dir = os.path.join('//192.168.4.114//R&D_Share//OFXSTORAGE//jobs//'+serializer.data['project']['client']+'//'+serializer.data['project']['name'], shot_dir)
            # os.makedirs(final_dir, exist_ok=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectShotsData(APIView):

    def get(self, request, projectId, format=None):
        shot = Shots.objects.filter(project=projectId)
        serializer = ShotsSerializer(shot, many=True, context={"request":request})
        return Response(serializer.data)

class ShotUpdate(APIView):

    def get(self, request, shotId, format=None):
        shot = Shots.objects.get(id=shotId)
        serializer = ShotsSerializer(shot)
        return Response(serializer.data)

    def put(self, request, shotId):
        shot = Shots.objects.get(id=shotId)
        serializer = ShotsSerializer(shot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, shotId, format=None):
        model_object = Shots.objects.get(id=shotId)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)