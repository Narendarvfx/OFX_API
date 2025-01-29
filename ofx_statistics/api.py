#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Count, Sum, Max, OuterRef, Subquery, IntegerField, CharField, Value
from django.db.models.functions import Cast, Coalesce
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ofx_statistics.models import EmployeeDailyStatistics, TLDailyStatistics, LeadDailyStatistics, ClientStatistics
from ofx_statistics.serializers import EmployeeDailyStatisticserializer, TLDailyStatisticsSerializer, \
    LeadDailyStatisticsSerializer, ClientStatisticsSerializer
from production.models import Shots, Task_Type
from production.serializers import ShotsSerializer


class Ofxstatistics(APIView):
    """
    This for OFX Employee Daily Statistics
    """
    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('profile_id'):
                argumentos['employee__profile__id'] = query_params.get('profile_id')
            if query_params.get('ofx_id'):
                argumentos['employee__employee_id'] = query_params.get('ofx_id')
            if query_params.get('from_date') and query_params.get('to_date'):
                argumentos['logDate__range'] = [query_params.get('from_date'), query_params.get('to_date')]
            ofxstat = EmployeeDailyStatistics.objects.select_related('employee').filter(**argumentos)
        else:
            ofxstat = EmployeeDailyStatistics.objects.select_related('employee').all()
        serializer = EmployeeDailyStatisticserializer(ofxstat, many=True)
        return Response(serializer.data)

    def put(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('id'):
                argumentos['pk'] = query_params.get('id')
        ofxstat = EmployeeDailyStatistics.objects.get(**argumentos)
        serializer = EmployeeDailyStatisticserializer(ofxstat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request,format=None):
        serializer = EmployeeDailyStatisticserializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class teamLeaadstatistics(APIView):
    """
    This for OFX Team Lead Daily Statistics
    """

    def put(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('id'):
                argumentos['pk'] = query_params.get('id')
        ofxstat = TLDailyStatistics.objects.get(**argumentos)
        serializer = TLDailyStatisticsSerializer(ofxstat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request,format=None):
        serializer = TLDailyStatisticsSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientStatisticsAPI(APIView):

    def get(self, request):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('id'):
                argumentos['pk'] = query_params.get('id')

            if query_params.get('client_id'):
                argumentos['client'] = query_params.get('client_id')

            if query_params.get('project_id'):
                argumentos['project'] = query_params.get('project_id')

            if query_params.get('dep'):
                argumentos['dep__name'] = query_params.get('dep')
        try:
            clientstat = ClientStatistics.objects.get(**argumentos)
            serializer = ClientStatisticsSerializer(clientstat)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response([])

    def post(self, request,format=None):
        serializer = ClientStatisticsSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('id'):
                argumentos['pk'] = query_params.get('id')
        ofxstat = ClientStatistics.objects.get(**argumentos)
        serializer = ClientStatisticsSerializer(ofxstat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class leadstatistics(APIView):
    """
    This for OFX Team Lead Daily Statistics
    """

    def put(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('id'):
                argumentos['pk'] = query_params.get('id')
        ofxstat = LeadDailyStatistics.objects.get(**argumentos)
        serializer = LeadDailyStatisticsSerializer(ofxstat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request,format=None):
        serializer = LeadDailyStatisticsSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
