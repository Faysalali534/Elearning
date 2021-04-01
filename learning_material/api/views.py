from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from learning_material.api.serializers import CourseLessonSerializer, LessonSerializer, CourseInfoSerializer, \
    LessonInfoSerializer, EnrollStudentSerializer, EnrollUserSerializer
from learning_material.models import Course, Lesson, EnrollStudent
from restapi.permission import MyPermission
from rest_framework_simplejwt.authentication import JWTAuthentication


class CourseLessonApiViewSet(viewsets.ModelViewSet):
    serializer_class = CourseLessonSerializer
    queryset = Course.objects.all()
    lookup_field = 'id'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, MyPermission]

    @action(detail=True, methods=['GET'])
    def lessons(self, request, id=None):
        id = self.kwargs.get('id')
        lessons = Lesson.objects.filter(course__id=id)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=['GET', 'POST'])
    def lesson(self, request, id=None):
        course = self.get_object()
        data = request.data
        data['course'] = course.id
        serializer = LessonInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CourseInfoViewSet(viewsets.ModelViewSet):
    serializer_class = CourseInfoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, MyPermission]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Course.objects.all()
        else:
            course = Course.objects.filter(taught_by=self.request.user.id)
            if not course:
                return Course.objects.all()
            return course

    def perform_create(self, serializer):
        serializer.save(taught_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(taught_by=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, MyPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EnrollStudentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollStudentSerializer
    queryset = EnrollStudent.objects.all()
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        data = request.data
        student_enroll = EnrollStudent.objects.filter(Q(course_id=data['course_id']) & Q(student_id=request.user.id))
        if not student_enroll:
            data['student_id'] = request.user.id
            data['course_id'] = data['course_id']
            serializer = EnrollStudentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        return Response({'msg': 'Student already enrolled'})


class EnrollUserViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EnrollStudent.objects.filter(course_id=self.kwargs.get('pk')).all()

    def get_serializer_class(self):
        print(self.action)
        if self.action in ['retrieve', 'list']:
            return EnrollUserSerializer
        else:
            return EnrollStudentSerializer

    @action(detail=True, methods=['GET'])
    def enrolledstudents(self, request, pk=None):
        id = pk
        enroll_student = EnrollStudent.objects.filter(course_id=id).all()
        python_data = []
        for student in enroll_student:
            dict = {}
            dict['id'] = student.id
            dict['first_name'] = student.student_id.first_name
            dict['username'] = student.student_id.username
            dict['last_name'] = student.student_id.last_name
            dict['email'] = student.student_id.email
            dict['enrolled_at'] = student.enrolled_at
            python_data.append(dict)
        serializer = EnrollUserSerializer(data=python_data, many=True)
        if serializer.is_valid():
            return Response(serializer.data, status=200)
