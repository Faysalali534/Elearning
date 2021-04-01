import io
import json

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, \
    UpdateModelMixin
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import viewsets

from accounts.models import UserProfile
from learning_material.models import Course, Lesson, EnrollStudent
from restapi.serializers import UserProfileSerializer
from django.views.decorators.csrf import csrf_exempt
from restapi.permission import MyPermission

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
        print(json_data)
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
        # json_data = request.body
        # print(json_data)
        # stream = io.BytesIO(json_data)
        # pythondata = JSONParser().parse(stream)
        # user_id = pythondata.get('id', None)
        # user_id = 4
        # print(user_id)
        if pk is not None:
            user_profile = get_object_or_404(UserProfile, user_id=pk)
            # user_profile = UserProfile.objects.get(user_id=pk)
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


# class CourseViewSet(viewsets.ModelViewSet):
#     serializer_class = CourseSerializer
#     queryset = Course.objects.all()
#     lookup_field = 'id'
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [MyPermission]
#
#     @action(detail=True, methods=['GET'])
#     def lessons(self, request, id=None):
#         course = self.get_object()
#         lessons = Lesson.objects.filter(course=course)
#         serializer = LessonSerializer(lessons, many=True)
#         return Response(serializer.data, status=200)
#
#     @action(detail=True, methods=['POST'])
#     def lesson(self, request, id=None):
#         course = self.get_object()
#         data = request.data
#         data['course'] = course.id
#         serializer = LessonInfoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#
#
# class CourseInfoViewSet(viewsets.ModelViewSet):
#     serializer_class = CourseInfoSerializer
#     # queryset = Course.objects.all()
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [MyPermission]
#
#     def get_queryset(self):
#         if self.request.user.is_anonymous:
#             return Course.objects.all()
#         else:
#             course = Course.objects.filter(taught_by=self.request.user.id)
#             if not course:
#                 return Course.objects.all()
#             return course
#
#     def perform_create(self, serializer):
#         serializer.save(taught_by=self.request.user)
#
#     def perform_update(self, serializer):
#         serializer.save(taught_by=self.request.user)
#
#
# class LessonViewSet(viewsets.ModelViewSet):
#     serializer_class = LessonSerializer
#     queryset = Lesson.objects.all()
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [MyPermission]
#
#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)
#
#
# class EnrollStudentViewSet(viewsets.ModelViewSet):
#     serializer_class = EnrollStudentSerializer
#     queryset = EnrollStudent.objects.all()
#     lookup_field = 'id'
#
#     def create(self, request, *args, **kwargs):
#         data = request.data
#         student_enroll = EnrollStudent.objects.filter(Q(course_id=data['course_id']) & Q(student_id=request.user.id))
#         if not student_enroll:
#             data['student_id'] = request.user.id
#             data['course_id'] = data['course_id']
#             serializer = EnrollStudentSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=201)
#             return Response(serializer.errors, status=400)
#         return Response({'msg': 'Student already enrolled'})
#
#
# class EnrollUserViewSet(viewsets.ModelViewSet):
#     serializer_class = EnrollStudentSerializer
#     # queryset = EnrollStudent.objects.all()
#     # authentication_classes = [SessionAuthentication]
#     # permission_classes = [MyPermission]
#
#     def get_queryset(self):
#         print(self.kwargs)
#         return EnrollStudent.objects.filter(course_id=self.kwargs.get('pk')).all()
#
#     def get_serializer_class(self):
#         print(self.action)
#         if self.action in ['retrieve', 'list']:
#             print('kela')
#             return EnrollUserSerializer
#         else:
#             print('kela1')
#             return EnrollStudentSerializer
#
#     # def list(self, request, *args, **kwargs):
#     #     serializer = EnrollUserSerializer(self.queryset, many=True)
#     #     return Response(serializer.data)
#
#
#     @action(detail=True, methods=['GET'])
#     def enrolledstudents(self, request, pk=None):
#         id = pk
#         enroll_student = EnrollStudent.objects.filter(course_id=id).all()
#         python_data = []
#         for student in enroll_student:
#             dict = {}
#             dict['id'] = student.id
#             dict['first_name'] = student.student_id.first_name
#             dict['username'] = student.student_id.username
#             dict['last_name'] = student.student_id.last_name
#             dict['email'] = student.student_id.email
#             dict['enrolled_at'] = student.enrolled_at
#             python_data.append(dict)
#         print(python_data)
#         # json_data = JSONRenderer().render(python_data)
#         # json_data = json.dumps(python_data)
#
#         serializer = EnrollUserSerializer(data=python_data, many=True)
#         print(serializer)
#         if serializer.is_valid():
#             return Response(serializer.data, status=200)
#         return Response({'msg': 'Wrong with getting table'}, status=400)
#
#
# def user_enroll_result(request):
#     user_profile = EnrollStudent.objects.filter(course_id=1).all()
#     print(user_profile)
#     serializer = EnrollUserSerializer(user_profile, many=True)
#     json_data = JSONRenderer().render(serializer.data)
#     return HttpResponse(json_data, content_type='application/json')
