from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth.models import User, update_last_login
from django.http import Http404
from rest_framework import status, permissions
from .models import Profile
from .serializers import UserSerializer, UserProfileSerializer, ChangePasswordSerializer


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
            profile = Profile.objects.get(user__username=username)
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
                'groups': profile.user.groups.all().values_list()
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
        serializer = UserProfileSerializer(User.objects.get(id=user_id), data=request.data)
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
            return Profile.objects.get(pk=profile_id)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, profile_id):
        user_profile_list = Profile.objects.all().filter(id=profile_id)
        profile_serializer = UserProfileSerializer(user_profile_list, many=True)
        return Response(profile_serializer.data)

    def put(self, request, profile_id):
        model_object = self.get_object(profile_id)
        serializer = UserProfileSerializer(model_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    # permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, user_id):
        user = User.objects.get(id=user_id)
        return user

    def put(self, request,user_id, *args, **kwargs):
        # query_params = self.request.query_params
        # user_id = query_params.get('user_id', None)
        self.object = self.get_object(user_id)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            #Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)