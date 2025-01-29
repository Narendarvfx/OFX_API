#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
import json
import re

from django.contrib import auth
from django.contrib.auth.models import User, update_last_login
from django.http import Http404
from rest_framework import status, mixins, viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from hrm.models import ProductionTeam, Permissions, Grade, Leaves, Attendance, OrganizationHolidays, \
    EmployeeWorkingDays, DepartmentWorkingDays, OrganizationWorkingDays, WorkingDayTypes, EmployeeRoleBinding, \
    Department, Employee, Role, Location
from hrm.serializers import EmployeeSerializer, TeamSerializer, PermissionSerializer, EmployeePutSerializer, \
    GradeSerializer, MyProfileSerializer, LeavesSerializer, AttendanceSerializer, OrganizationHolidaysSerializer, \
    DepartmentWorkingDaysSerializer, EmpWorkingDaysSerializer, OrgWorkingDaysSerializer, EmpWorkingDaysPostSerializer, \
    OrganizationHolidaysPostSerializer, DepartmentWorkingDaysPostSerializer, WorkingDayTypesSerializer, \
    EmployeeRoleBindingSerializer, DepartmentSerializer, RoleSerializer, LocationSerializer, EmployeePostSerializer, \
    ChangePasswordSerializer, UserProfileSerializer, UserSerializer, EmployeeCompactSerializer
from production.models import Shots
from profiles.models import Profile


class UserAuthentication(ObtainAuthToken):
    """
    This class will return user authentication
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user.is_active:
            update_last_login(None, user)
            profile = User.objects.get(username=username)
            photo = profile.employee.photo
            if photo:
                photo = profile.employee.photo.url
            else:
                photo = '/media/hrm/employees/photo/default.jpg'
            data = {
                'token': token.key,
                'id': profile.id,
                'full_name': profile.employee.fullName,
                'employee_id': profile.employee.employee_id,
                'photo': photo,
                'groups': profile.groups.all().values_list()
            }
            return Response(data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):

    def get(self, request, format=None):
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserEdit(APIView):
    def get(self, request, user_id, format=None):
        serializer = UserSerializer(User.objects.get(id=user_id))
        return Response(serializer.data)

    def put(self, request, user_id):
        serializer = UserProfileSerializer(User.objects.get(id=user_id), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, format=None):
        model_object = User.objects.get(id=user_id)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserProfileAPIView(APIView):
    """
    This class will return json data of user profile
    """
    def get_object(self, profile_id):
        try:
            return User.objects.get(pk=profile_id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, profile_id):
        user_profile_list = User.objects.all().filter(id=profile_id)
        profile_serializer = UserProfileSerializer(user_profile_list, many=True)
        return Response(profile_serializer.data)

    def put(self, request, profile_id):
        model_object = self.get_object(profile_id)
        serializer = UserProfileSerializer(model_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenUser(APIView):
    def get(self, request, format=None):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            user_id = Token.objects.get(key=token.split(" ")[-1]).user_id
            serializer = UserSerializer(User.objects.get(id=user_id))
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, user_id):
        user = User.objects.get(id=user_id)
        return user

    def put(self, request,user_id, *args, **kwargs):
        # query_params = self.request.query_params
        # user_id = query_params.get('user_id', None)
        self.object = self.get_object(user_id)
        serializer = ChangePasswordSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            #Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response("Current Password is incorrect",
                                status=status.HTTP_400_BAD_REQUEST)
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"

            # compiling regex
            pat = re.compile(reg)

            # searching regex
            mat = re.search(pat, serializer.data.get("new_password"))

            # validating conditions
            if not mat:
                return Response("Password Should be the combination of Uppercase, Lowercase, \n Numeric, Special Character and minimum 8 character length",
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.is_resetpwd = False
            Profile.objects.filter(user=self.object).update(force_password_change=False)
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyAccount(APIView):
    """
    This is for MyAccount detail
    """
    def get(self, request, format=None):
        user = request.user
        employee = Employee.objects.select_related('department','grade','role','employement_status','team_lead','supervisor').prefetch_related('permissions').get(profile__username=user.username)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, profile_id, format=None):
        permission_classes = (IsAuthenticated,)  # permission classes
        employee = Employee.objects.get(profile=profile_id)

        serializer = EmployeePutSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetail(APIView):
    """
    This is for edit employee detail
    """
    def get(self, request, profile_id, format=None):
        employee = Employee.objects.select_related('department','grade','role','employement_status','team_lead','supervisor').prefetch_related('permissions').get(profile=profile_id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, profile_id, format=None):
        permission_classes = (IsAuthenticated,)  # permission classes
        employee = Employee.objects.get(pk=profile_id)
        serializer = EmployeePutSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyProfileDetail(APIView):
    """
    This is for edit employee detail
    """
    def get(self, request, id, format=None):
        employee = Employee.objects.select_related('department','grade','role','employement_status','team_lead','supervisor').prefetch_related('permissions').get(pk=id)
        serializer = MyProfileSerializer(employee)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        permission_classes = (IsAuthenticated,)  # permission classes
        employee = Employee.objects.get(pk=id)

        serializer = EmployeePutSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeavesData(APIView):
    """
    Returns ALl Leaves Data
    """
    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('targetDate_from_date') and query_params.get('targetDate_to_date'):
                argumentos['targetDate__range'] = [query_params.get('targetDate_from_date'), query_params.get('targetDate_to_date')]
            if query_params.get('creation_from_date') and query_params.get('creation_to_date'):
                argumentos['creationDate__range'] = [query_params.get('creation_from_date'), query_params.get('creation_to_date')]
            if query_params.get('employee_id'):
                argumentos['employee__profile__id'] = query_params.get('employee_id')
            if query_params.get('ofx_id'):
                argumentos['employee__employee_id'] = query_params.get('ofx_id')
            if query_params.get('dateFrom_from') and query_params.get('dateFrom_to'):
                argumentos['dateFrom__range'] = [query_params.get('dateFrom_from'), query_params.get('dateFrom_to')]
            if query_params.get('dateTo_from') and query_params.get('dateTo_to'):
                argumentos['dateTo__range'] = [query_params.get('dateTo_from'), query_params.get('dateTo_to')]
            leaves = Leaves.objects.select_related('employee', 'employee__profile','employee__grade', 'employee__department', 'employee__employement_status', 'employee__location', 'sessionFrom','sessionTo').filter(**argumentos)
        else:
            leaves = Leaves.objects.select_related('employee', 'employee__profile','employee__grade', 'employee__department', 'employee__employement_status', 'employee__location', 'sessionFrom','sessionTo').all()
        serializer = LeavesSerializer(leaves, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LeavesSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        query_params = self.request.query_params
        if query_params.get('id'):
            leaves = Leaves.objects.get(pk=query_params.get('id'))
            serializer = LeavesSerializer(leaves, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        query_params = self.request.query_params
        if query_params.get('id'):
            model_object = Leaves.objects.get(pk=query_params.get('id'))
            model_object.delete()
            return Response(status=status.HTTP_201_CREATED)
        return Response({'msg':'id required'}, status=status.HTTP_400_BAD_REQUEST)

class AttendanceData(APIView):
    """
    Returns ALl Attendance Data
    """
    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('targetDate_from_date') and query_params.get('targetDate_to_date'):
                argumentos['attendanceDate__range'] = [query_params.get('targetDate_from_date'), query_params.get('targetDate_to_date')]
            if query_params.get('creation_from_date') and query_params.get('creation_to_date'):
                argumentos['creationDate__range'] = [query_params.get('creation_from_date'), query_params.get('creation_to_date')]
            if query_params.get('from_date') and query_params.get('to_date'):
                argumentos['attendanceDate__range'] = [query_params.get('from_date'), query_params.get('to_date')]
            if query_params.get('employee_id'):
                argumentos['employee__employee_id'] = query_params.get('employee_id')
            if query_params.get('profile_id'):
                argumentos['employee__id'] = query_params.get('profile_id')
            attendance = Attendance.objects.select_related('employee', 'employee__profile','employee__grade', 'employee__department', 'employee__employement_status', 'employee__location').filter(**argumentos)
        else:
            attendance = Attendance.objects.select_related('employee', 'employee__profile','employee__grade', 'employee__department', 'employee__employement_status', 'employee__location').all()
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AttendanceSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        query_params = self.request.query_params
        if query_params.get('id'):
            leaves = Attendance.objects.get(pk=query_params.get('id'))
            serializer = AttendanceSerializer(leaves, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, format=None):
        query_params = self.request.query_params
        if query_params.get('id'):
            model_object = Attendance.objects.get(pk=query_params.get('id'))
            model_object.delete()
            return Response(status=status.HTTP_201_CREATED)
        return Response({'msg':'id required'}, status=status.HTTP_400_BAD_REQUEST)

class WorkingDayTypesApi(APIView):
    """
    Returns ALl Holidays Data
    """
    def get(self, request, format=None):

        holidays = WorkingDayTypes.objects.all()
        serializer = WorkingDayTypesSerializer(holidays, many=True)
        return Response(serializer.data)

class HolidaysDataApi(APIView):
    """
    Returns ALl Holidays Data
    """
    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('from_date') and query_params.get('to_date'):
                argumentos['targetDate__range'] = [query_params.get('from_date'), query_params.get('to_date')]
            if query_params.get('id'):
                argumentos['pk'] = query_params.get('id')
            if query_params.get('location'):
                argumentos['location__name'] = query_params.get('location')
            holidays = OrganizationHolidays.objects.select_related('updatedBy','createdBy', 'type').filter(**argumentos)
        else:
            holidays = OrganizationHolidays.objects.select_related('updatedBy','createdBy', 'type').all()
        serializer = OrganizationHolidaysSerializer(holidays, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrganizationHolidaysPostSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        query_params = self.request.query_params
        if query_params.get('id'):
            holidays = OrganizationHolidays.objects.get(pk=query_params.get('id'))
            serializer = OrganizationHolidaysPostSerializer(holidays, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        To Delete a particular object Primary Key is required
        [ref]: api/calendar/holidays/?id=''
        query_params:
        'id'
        """
        query_params = self.request.query_params

        if query_params:
            id = query_params.get('id', None)
            model_object = OrganizationHolidays.objects.get(pk=id)
            model_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

class DepartmentWorkingDaysApi(APIView):
    """
    Returns ALl Department Working Days Data
    """
    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:

            if query_params.get('from_date') and query_params.get('to_date'):
                argumentos['targetDate__range'] = [query_params.get('from_date'), query_params.get('to_date')]
            if query_params.get('department'):
                argumentos['department__name'] = query_params.get('department')
            if query_params.get('id'):
                argumentos['pk'] = query_params.get('id')
            if query_params.get('location'):
                argumentos['location__name'] = query_params.get('location')

            deptWrkDays = DepartmentWorkingDays.objects.select_related('updatedBy','assignedBy').filter(**argumentos)

        else:
            deptWrkDays = DepartmentWorkingDays.objects.select_related('updatedBy','assignedBy').all()
        serializer = DepartmentWorkingDaysSerializer(deptWrkDays, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepartmentWorkingDaysPostSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        query_params = self.request.query_params
        if query_params.get('id'):
            deptWrkDays = DepartmentWorkingDays.objects.get(pk=query_params.get('id'))
            serializer = DepartmentWorkingDaysPostSerializer(deptWrkDays, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        To Delete a particular object Primary Key is required
        [ref]: api/calendar/deptworkingdays/?id=''
        query_params:
        'id'
        """
        query_params = self.request.query_params

        if query_params:
            id = query_params.get('id', None)
            model_object = DepartmentWorkingDays.objects.get(pk=id)
            model_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

class EmpWorkingDaysApi(APIView):
    """
    Returns ALl Employee Working Days Data
    """
    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('from_date') and query_params.get('to_date'):
                argumentos['targetDate__range'] = [query_params.get('from_date'),query_params.get('to_date')]
            if query_params.get('isSystem'):
                argumentos['isSystem'] = query_params.get('isSystem')
            if query_params.get('employee_id'):
                argumentos['employee__profile__id'] = query_params.get('employee_id')
            if query_params.get('id'):
                argumentos['pk'] = query_params.get('id')
            if query_params.get('location'):
                argumentos['location__name'] = query_params.get('location')
            empWrkDays = EmployeeWorkingDays.objects.select_related('updatedBy','assignedBy', 'employee').filter(**argumentos)
        else:
            empWrkDays = EmployeeWorkingDays.objects.select_related('updatedBy','assignedBy', 'employee','employee__grade','employee__profile','employee__location','employee__employement_status','employee__department','employee__role').all()
        serializer = EmpWorkingDaysSerializer(empWrkDays, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmpWorkingDaysPostSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        query_params = self.request.query_params
        if query_params.get('id'):
            empWrkDays = EmployeeWorkingDays.objects.get(pk=query_params.get('id'))
            serializer = EmpWorkingDaysPostSerializer(empWrkDays, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        To Delete a particular object Primary Key is required
        [ref]: api/calendar/empworkingdays/?id=''
        query_params:
        'id'
        """
        query_params = self.request.query_params

        if query_params:
            id = query_params.get('id', None)
            model_object = EmployeeWorkingDays.objects.get(pk=id)
            model_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

class AllGrades(APIView):
    """
    This is for edit employee detail
    """
    def get(self, request, format=None):
        query_params = self.request.query_params
        print(query_params.get('name'))
        if query_params.get('id'):
            grades = Grade.objects.filter(id=query_params.get('id'))
        elif query_params.get('name'):
            grades = Grade.objects.filter(name=query_params.get('name'))
        else:
            grades = Grade.objects.all()
        serializer = GradeSerializer(grades, many=True, context={"request":request})
        return Response(serializer.data)

    def post(self,request, format=None):
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        query_params = self.request.query_params
        if query_params.get('id'):
            grade_obj = Grade.objects.get(pk=query_params.get('id'))
            serializer = GradeSerializer(grade_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllDepartments(APIView):
    """
        This is for edit department detail
        """

    def get(self, request, format=None):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True, context={"request": request})
        return Response(serializer.data)

class AllRole(APIView):
    """
            This is for edit role detail
            """
    def get(self, request, format=None):
        role = Role.objects.all()
        serializer = RoleSerializer(role, many=True, context={"request": request})
        return Response(serializer.data)

class AllLocation(APIView):
    """
            This is for edit location detail
            """
    def get(self, request, format=None):
        location = Location.objects.all()
        serializer = LocationSerializer(location, many=True, context={"request": request})
        return Response(serializer.data)
class ListModelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass
class AllEmployeeDetail(APIView):
    """
    This is for edit employee detail
    """
    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # General filtering logic
        argumentos = {'employement_status__name': query_params.get('status', 'Active')}
        if query_params.get('dept'):
            dept_param = query_params.get('dept')
            if '|' in dept_param:
                argumentos['department__name__in'] = dept_param.split('|')
            else:
                argumentos['department__name'] = dept_param

        if query_params.get('role'):
            role_param = query_params.get('role')
            if '|' in role_param:
                argumentos['role__name'] = role_param.split('|')
            else:
                argumentos['role__name'] = role_param

        if query_params.get('location'):
            location_param = query_params.get('location')
            if '|' in location_param:
                argumentos['location__name__in'] = location_param.split('|')
            else:
                argumentos['location__name'] = location_param

        if query_params.get('ofx_id'):
            argumentos['employee_id'] = query_params.get('ofx_id')
        if query_params.get('id'):
            argumentos['pk'] = query_params.get('id')
        if query_params.get('lead'):
            argumentos['team_lead__profile__pk'] = query_params.get('lead')

        queryset = Employee.objects.select_related(
            'profile', 'department', 'role', 'location', 'employement_status', 'grade', 'profile__auth_token'
        ).prefetch_related(
            'team_lead', 'team_lead__department', 'team_lead__profile',
            'supervisor', 'supervisor__department', 'profile__groups', 'profile__user_permissions'
        ).filter(**argumentos)

        # Paginate or return all results
        if query_params.get('page'):
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = EmployeeSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = EmployeeSerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self,request, format=None):
        serializer = EmployeePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class employee_role_binding(APIView):
    """
    
    """
    def get(self, request, format=None):
        query_params = self.request.query_params
        argumentos = {}
        # argumentos['employement_status__name'] = query_params.get('status','Active')
        if query_params.get('department'):
            argumentos['department__name'] = query_params.get('department')

        if query_params.get('role'):
            argumentos['role__name'] = query_params.get('role')

        if query_params.get('employee_id'):
            argumentos['employee__id'] = query_params.get('employee_id')

        if query_params.get('employee_ofx_id'):
            argumentos['employee__employee_id'] = query_params.get('employee_ofx_id')

        if query_params.get('bind_with_id'):
            argumentos['bindWith__id'] = query_params.get('bind_with_id')

        if query_params.get('bind_with_ofx_id'):
            argumentos['bindWith__employee_id'] = query_params.get('bind_with_ofx_id')

        if query_params.get('id'):
            argumentos['pk'] = query_params.get('id')

        _EmployeeRoleBinding = EmployeeRoleBinding.objects.select_related('employee', 'department', 'role', 'bindWith', 'created_by', 'updated_by').filter(**argumentos)
        serializer = EmployeeRoleBindingSerializer(_EmployeeRoleBinding, many=True, context={"request":request})
        return Response(serializer.data)

    def post(self,request, format=None):
        serializer = EmployeeRoleBindingSerializer(data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request,id):
        bind = EmployeeRoleBinding.objects.get(pk=id)
        serializer = EmployeeRoleBindingSerializer(bind, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            serializer = EmployeeRoleBindingSerializer(bind)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        model_object = EmployeeRoleBinding.objects.get(id=id)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AllTeams(APIView):

    def get(self, request, format=None):
        team= ProductionTeam.objects.all()
        serializer = TeamSerializer(team, many=True, context={"request":request})
        return Response(serializer.data)

class DeptLeads(APIView):

    def get(self, request, format=None):
        team= Employee.objects.filter()
        serializer = TeamSerializer(team, many=True, context={"request":request})
        return Response(serializer.data)

class TeamById(APIView):
    def get(self, request,id, format=None):
        team= ProductionTeam.objects.get(id=id)
        serializer = TeamSerializer(team, context={"request":request})
        return Response(serializer.data)

class AllPermissions(APIView):
    def get(self, request, format=None):
        permission= Permissions.objects.select_related('role').all()
        serializer = PermissionSerializer(permission, many=True, context={"request":request})
        return Response(serializer.data)

class RolePermissions(APIView):
    """
    This is for edit employee detail
    """
    def get(self, request, role_id, format=None):
        rpermission = Permissions.objects.select_related('role').get(role=role_id)
        serializer = PermissionSerializer(rpermission, context={"request":request})
        return Response(serializer.data)

class OrgWorkingdays(APIView):
    """
    Returns ALl Organization Working Days Data
    """
    def get(self, request, format=None ):
        query_params = self.request.query_params
        argumentos = {}
        if query_params:
            if query_params.get('from_date') and query_params.get('to_date'):
                argumentos['targetDate__range'] = [query_params.get('from_date'), query_params.get('to_date')]
            if query_params.get('name'):
                argumentos['name'] = query_params.get('name')
            if query_params.get('isWorkingDay'):
                argumentos['isWorkingDay'] = query_params.get('isWorkingDay')
            if query_params.get(' workingHours'):
                argumentos[' workingHours'] = query_params.get(' workingHours')
            if query_params.get('id'):
                argumentos['pk'] = query_params.get('id')
            if query_params.get('location'):
                argumentos['location__name'] = query_params.get('location')
            orgWrkDays = OrganizationWorkingDays.objects.select_related('updatedBy').filter(
                **argumentos)
        else:
            orgWrkDays = OrganizationWorkingDays.objects.select_related('updatedBy').all()
        serializer =  OrgWorkingDaysSerializer(orgWrkDays, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrgWorkingDaysSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        serializer = OrgWorkingDaysSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
