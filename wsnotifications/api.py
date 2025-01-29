#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import datetime
import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from hrm.models import EmployeeGroups, Employee
from production.models import MyTask
from wsnotifications.models import Notifications, NotificationLogs, UserNotificationTags
from wsnotifications.serializers import NotificationsSerializer, WsNotificationSerializer, AttachmentCompactSerializer, \
    WsNotificationPostSerializer, UserNotificationTagSerializer, WsNotificationPutSerializer

class NotificationsDetail(APIView):

    def get(self, request, format=None):
        notification = Notifications.objects.all().order_by('-sent_date')
        serializer = NotificationsSerializer(notification, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NotificationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationsUnread(APIView):

    def get(self, request, userId, format=None):
        notification = Notifications.objects.filter(read=False, to=userId).order_by('-sent_date')
        serializer = NotificationsSerializer(notification, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NotificationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WsNotificationNotes(APIView):
    def get(self, request):
        query_params = self.request.query_params
        argumentos = {}
        if query_params.get('reference_type'):
            types = query_params.get('reference_type')

            argumentos['reference_type__name'] = types
        if len(argumentos) > 0:
            notifcationlogs = NotificationLogs.objects.filter(**argumentos, referenceId=query_params.get(
                'referenceId')).select_related('from_user', 'reference_type', 'from_group_key',
                                               'from_user_apikey').prefetch_related('to_users', 'to_groups',
                                                                                    'to_groups__department',
                                                                                    'attachments', 'read_recipients')
        else:
            notifcationlogs = NotificationLogs.objects.all().select_related('from_user', 'reference_type',
                                                                            'from_group_key',
                                                                            'from_user_apikey').prefetch_related(
                'to_users', 'to_groups', 'to_groups__department', 'attachments', 'read_recipients')
        serializer = WsNotificationSerializer(notifcationlogs, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        files_store = []
        attach = []
        for f in request.FILES.getlist('attachments'):
            type = f.name.split('.')
            type = "" if len(type) == 1 else type[-1]
            _dat = {
                'file_name': f.name,
                'file_size': f.size,
                'content_type': f.content_type,
                'file_type': type,
                'files': f
            }
            serializer = AttachmentCompactSerializer(data=_dat, partial=True)
            if serializer.is_valid():
                serializer.save()
                av = serializer.data
                files_store.append(av['id'])
                attach.append(av)
        _res_data = {
            'dataId': request.data['dataId'],
            'referenceId': request.data['referenceId'],
            'reference_type': request.data['reference_type'],
            'from_user': request.data['from_user'],
            'from_user_apikey': request.data['from_user_apikey'],
            'to_users': request.data['to_users'] if isinstance(request.data['to_users'], list) else [int(i) for i in request.data['to_users'].split(',')] if len(request.data['to_users'])>0 else [],
            'to_groups': request.data['to_groups'] if isinstance(request.data['to_groups'], list) else [int(i) for i in request.data['to_groups'].split(',')] if len(request.data['to_groups'])>0 else [],
            'attachments': files_store,
            'message': request.data['message'],
            'message_title': request.data['message_title']
        }
        noteserializer = WsNotificationPostSerializer(data=_res_data, partial=True)
        if noteserializer.is_valid():
            _serdata = noteserializer.save()
            not_data = noteserializer.data
            not_data['attachments'] = attach
            users_list = not_data['to_users']
            emp = Employee.objects.filter(employee_groups__in=not_data['to_groups']).values_list('id')
            for _emp in emp:
                if list(_emp)[0] not in users_list:
                    users_list.append(list(_emp)[0])
            for user in users_list:
                _dat = {
                    'user_id': user,
                    'notify_id': not_data['dataId']
                }
                _usertagserializer = UserNotificationTagSerializer(data=_dat, partial=True)
                if _usertagserializer.is_valid():
                    _usertagserializer.save()
            return Response(data=not_data, status=status.HTTP_201_CREATED)
        return Response(noteserializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WsNotificationNotesDetails(APIView):
    def get(self, request, format=json):
        query_params = self.request.query_params
        data_id = query_params.get('data_id')
        details = NotificationLogs.objects.get(dataId=data_id)
        serializer = WsNotificationSerializer(details)
        return Response(serializer.data)

class WsNotificationLogsAPI(APIView):

    def get(self, request):
        query_params = self.request.query_params
        argumentos = {}
        if query_params.get('reference_type'):
            types = query_params.get('reference_type')
            # for reference in query_params.get('reference_type').split('|'):
            #     types.append(reference)
            argumentos['reference_type__name'] = types
        if len(argumentos) > 0:
            notifcationlogs = NotificationLogs.objects.filter(**argumentos,
                                                              referenceId=query_params.get('referenceId')).order_by(
                'creation_date').select_related('from_user', 'reference_type', 'from_group_key',
                                                'from_user_apikey').prefetch_related('to_users', 'to_groups',
                                                                                     'to_groups__department',
                                                                                     'attachments', 'read_recipients')
        else:
            notifcationlogs = NotificationLogs.objects.all().order_by('creation_date').select_related('from_user',
                                                                                                      'reference_type',
                                                                                                      'from_group_key',
                                                                                                      'from_user_apikey').prefetch_related(
                'to_users', 'to_groups', 'to_groups__department', 'attachments', 'read_recipients')
        serializer = WsNotificationSerializer(notifcationlogs, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = WsNotificationSerializer(data=request.data, many=True, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShotsTargetsListAPI(APIView):

    def get(self, request):
        """
        param1 -- shot_id - string
        param2 -- shot_type - string
        """
        query_params = self.request.query_params
        argumentos = {}
        j_dat = {
            'users': [],
            'groups': []
        }
        if query_params.get('shot_id'):
            shots = query_params.get('shot_id')
            shot_groups = query_params.get('shot_type')
            argumentos['shot__id'] = shots
        if len(argumentos) > 0:
            tasks = list(
                MyTask.objects.select_related('shot__task_type', 'shot__sequence', 'shot__sequence__project', 'artist',
                                              'assigned_by', 'task_status').filter(**argumentos).values('artist',
                                                                                                        'artist__apikey'))
            groups = list(
                EmployeeGroups.objects.prefetch_related('department').filter(department__name=shot_groups).values('id',
                                                                                                                  'groupkey'))
            dat = json.dumps(tasks, indent=4, sort_keys=True, default=str)
            dat = json.loads(dat)
            group_dat = json.dumps(groups, indent=4, sort_keys=True, default=str)
            group_dat = json.loads(group_dat)

            for x in dat:
                j_dat['users'].append({'id': x['artist'], 'apikey': x['artist__apikey']})
            for x in group_dat:
                j_dat['groups'].append(x)

        return Response(j_dat)

    def post(self, request):
        serializer = WsNotificationSerializer(data=request.data, many=True, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserNotificationTagsAPI(APIView):

    def get(self, request):
        """
        param1 -- user_id - integer
        param2 -- date_range - from_date, to_date
        param3 -- read - boolean
        """
        query_params = self.request.query_params
        argumentos = {}
        limit = int(query_params.get('limit', 0))
        argumentos['user_id'] = query_params.get('user_id', 0)
        if query_params.get('read', None) is not None:
            argumentos['read'] = query_params.get('read')
        argumentos['creation_date__range'] = [query_params.get('from_date', "2022-12-21 00:00:00.000000"),
                                              query_params.get('to_date', datetime.datetime.now())]
        logs = UserNotificationTags.objects.filter(**argumentos).order_by('-creation_date').select_related('user_id', 'notify_id')
        _ser_data = UserNotificationTagSerializer(logs, many=True)
        _jsoned_data = json.loads(json.dumps(_ser_data.data, indent=4, sort_keys=True, default=str))

        notify_list = []
        for u in _jsoned_data:
            notify_list.append(u['notify_id'])
        if limit > 0:
            not_logs = NotificationLogs.objects.select_related('from_user', 'reference_type', 'from_group_key',
                                                               'from_user_apikey', 'from_user__department','from_user_apikey__department').prefetch_related('to_users',
                                                                                                    'to_groups',
                                                                                                    'to_groups__department',
                                                                                                    'to_users__department',
                                                                                                    'attachments',
                                                                                                    'read_recipients').filter(
                dataId__in=notify_list).order_by('-creation_date')[:limit]
        else:
            not_logs = NotificationLogs.objects.select_related('from_user', 'reference_type', 'from_group_key',
                                                               'from_user_apikey').prefetch_related('to_users',
                                                                                                    'to_groups',
                                                                                                    'to_users__department',
                                                                                                    'to_groups__department',
                                                                                                    'attachments',
                                                                                                    'read_recipients').filter(
                dataId__in=notify_list).order_by('-creation_date')
        _not_ser = WsNotificationSerializer(not_logs, many=True)
        _not_jsoned_data = json.loads(json.dumps(_not_ser.data, indent=4, sort_keys=True, default=str))

        return Response(_not_jsoned_data)

    def put(self, request):
        query_params = self.request.query_params
        argumentos = {}
        if query_params.get('user_id'):
            argumentos['user_id'] = query_params.get('user_id')
        if query_params.get('data_id'):
            argumentos['notify_id'] = query_params.get('data_id')
        users_tags = UserNotificationTags.objects.get(**argumentos)
        serializer = UserNotificationTagSerializer(users_tags, data=request.data)
        if serializer.is_valid():
            serializer.save()
            nlogs = NotificationLogs.objects.get(pk=query_params.get('data_id'))
            read_rp = list(nlogs.read_recipients.values_list('id', flat=True))
            if query_params.get('user_id') not in read_rp:
                read_rp.append(query_params.get('user_id'))
                _d = {
                    'read_recipients': read_rp
                }
                nlog_serializer = WsNotificationPutSerializer(nlogs, data=_d)
                if nlog_serializer.is_valid():
                    nlog_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
