#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from rest_framework import serializers

from hrm.models import Employee
from hrm.serializers import EmployeeCompactSerializer, EmployeeGroupSerializer
from wsnotifications.models import Notifications, NotificationLogs, NotifyTypes, Attachments, UserNotificationTags


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'


class AttachmentCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachments
        fields = '__all__'


class WsNotificationPostSerializer(serializers.ModelSerializer):
    reference_type = serializers.SlugRelatedField(queryset=NotifyTypes.objects.all(), slug_field="name", required=False)
    from_user_apikey = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field='apikey',
                                                    required=False)

    class Meta:
        model = NotificationLogs
        fields = '__all__'

class WsNotificationSerializer(serializers.ModelSerializer):
    reference_type = serializers.SlugRelatedField(queryset=NotifyTypes.objects.all(), slug_field="name", required=False)
    from_user = EmployeeCompactSerializer(read_only=True)
    to_users = EmployeeCompactSerializer(read_only=True, many=True)
    to_groups = EmployeeGroupSerializer(read_only=True, many=True)
    read_recipients = EmployeeCompactSerializer(read_only=True, many=True)
    # to_users = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.values('fullName'), required=False, many=True)
    from_user_apikey = EmployeeCompactSerializer(read_only=True)
    attachments = AttachmentCompactSerializer(read_only=True, many=True)

    class Meta:
        model = NotificationLogs
        fields = '__all__'
class WsNotificationPutSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationLogs
        fields = '__all__'


class UserNotificationTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotificationTags
        fields = '__all__'
