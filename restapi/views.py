import io
import json

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status, generics

from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, \
    UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import viewsets

from accounts.models import UserProfile
from restapi.serializers import UserProfileSerializer, LoginApiSerializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def user_profile_result(request):
    user_profile = UserProfile.objects.get(user_id=9)
    serializer = UserProfileSerializer(user_profile)
    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def create_user_profile(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = UserProfileSerializer(data=pythondata)
        if serializer.is_valid():
            serializer.save()
            print('serializer :', serializer)
            res = {'msg': 'Date Created.'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')


def get_user_profile(request, pk):
    if request.method == 'GET':
        if pk is not None:
            user_profile = get_object_or_404(UserProfile, user_id=pk)
            serializer = UserProfileSerializer(user_profile)
            json_data = JSONRenderer().render(serializer.data)
            print(json_data)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render({'msg': 'No data exists'})
        return HttpResponse(json_data, content_type='application/json')


def get_all_users(request):
    if request.method == 'GET':
        user_profile = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profile, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def update_user(request):
    if request.method == 'PUT':
        json_data = request.body
        print(json_data)
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        user_id = pythondata.get('id', None)
        user_profile = UserProfile.objects.get(user_id=user_id)
        serializer = UserProfileSerializer(user_profile, data=pythondata, partial=True)
        if serializer.is_valid():
            serializer.save()
            print('serializer :', serializer)
            res = {'msg': 'Data Updated.'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def delete_user(request):
    if request.method == 'DELETE':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        user_id = pythondata.get('id')
        user_profile = User.objects.get(id=user_id)
        user_profile.delete()
        res = {'msg': 'Data Deleted.'}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@method_decorator(csrf_exempt, name='dispatch')
class UserProfileAPI(View):

    def get(self, request):
        json_data = request.body
        print(json_data)
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        user_id = pythondata.get('id', None)
        if user_id is not None:
            user_profile = get_object_or_404(UserProfile, user_id=user_id)
            serializer = UserProfileSerializer(user_profile)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render({'msg': 'No data exists'})
        return HttpResponse(json_data, content_type='application/json')

    def post(self, request):
        json_data = request.body
        print(json_data)
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = UserProfileSerializer(data=pythondata)
        if serializer.is_valid():
            serializer.save()
            print('serializer :', serializer)
            res = {'msg': 'Data Created.'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    def put(self, request):
        json_data = request.body
        print(json_data)
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        user_id = pythondata.get('id', None)
        user_profile = UserProfile.objects.get(user_id=user_id)
        serializer = UserProfileSerializer(user_profile, data=pythondata, partial=True)
        if serializer.is_valid():
            serializer.save()
            print('serializer :', serializer)
            res = {'msg': 'Data Updated.'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    def delete(self, request):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        user_id = pythondata.get('id')
        user_profile = User.objects.get(id=user_id)
        user_profile.delete()
        res = {'msg': 'Data Deleted.'}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


class UserAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            user_profile = UserProfile.objects.get(user__id=id)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        user_profile = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profile, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.body)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'User created Successfully'}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'User creation failed'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        id = pk
        user_profile = UserProfile.objects.get(user__id=pk)
        serializer = UserProfileSerializer(user_profile, data=request.body)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'User update Successfully'})
        return Response({'msg': 'User update failed'}, status=status.HTTP_400_BAD_REQUEST)


class UserListAPI(GenericAPIView, ListModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserCreateAPI(GenericAPIView, CreateModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserRetrieveAPI(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserCreateAPIView(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserListCreateAPIView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileViewSet(viewsets.ViewSet):
    def list(self, request):
        user_profile = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profile, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            user_profile = UserProfile.objects.get(user__id=id)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)

    def create(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data created'}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        id = pk
        user_profile = UserProfile.objects.get(user__id=id)
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Updated'}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        id = pk
        user_profile = UserProfile.objects.get(user__id=id)
        user_profile.delete()
        return Response({'msg': 'Data Deleted'})


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginApiSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
        })
