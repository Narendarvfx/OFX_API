#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
from requests import Response
from rest_framework.views import APIView

from time_management.models import TimeManagement
from time_management.serializers import TimeManagementSerializer


class TimingData(APIView):

    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('id'):
                argumentos['pk'] = query_params.get('id')
            _tm = TimeManagement.objects.select_related('updatedBy','createdBy', 'type').filter(**argumentos)
        else:
            _tm = TimeManagement.objects.select_related('employee').all()
        serializer = TimeManagementSerializer(_tm, many=True)
        return Response(serializer.data)
