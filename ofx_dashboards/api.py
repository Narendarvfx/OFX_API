#  Copyright (c) 2022-2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from ofx_dashboards.models import MandayAvailability, WaitingForBids
from ofx_dashboards.serializers import MandayAvailabilitySerializer, WaitingForBidSerializer


class MandayAvailabilityView(APIView):

    def get(self, request, format=None):
        _qs = MandayAvailability.objects.filter(date__month=datetime.datetime.now().month).select_related('teamlead')
        serializer = MandayAvailabilitySerializer(_qs, many=True)
        return Response(serializer.data)

class WaitingforBidView(APIView):

    def get(self, request, format=None):
        _qs = WaitingForBids.objects.filter(date__month=datetime.datetime.now().month).select_related('dep')
        serializer = WaitingForBidSerializer(_qs, many=True)
        return Response(serializer.data)