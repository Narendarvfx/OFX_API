#  Copyright (c) 2022-2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
from rest_framework import serializers

from hrm.models import Employee
from ofx_dashboards.models import MandayAvailability, WaitingForBids


class MandayAvailabilitySerializer(serializers.ModelSerializer):
    teamlead = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field="fullName", required=False)
    class Meta:
        model = MandayAvailability
        fields = '__all__'

class WaitingForBidSerializer(serializers.ModelSerializer):

    class Meta:
        model = WaitingForBids
        fields = '__all__'