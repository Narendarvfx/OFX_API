from rest_framework import serializers

from production.models import Clients


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'