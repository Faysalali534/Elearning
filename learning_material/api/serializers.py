from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import UserProfile
from learning_material.models import Lesson, Course, EnrollStudent
from restapi.models import Blog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'last_name']


class LessonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Lesson
        fields = [
            'id',
            'lesson_id',
            'name',
            'created_by',
            'created_at',
            'course'
        ]
        read_only_fields = ('course',)


class CourseLessonSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'course_id',
            'name',
            'description',
            'taught_by',
            'lessons'
        ]

    def create(self, validated_data):
        lessons = validated_data.pop('lessons')
        course = Course.objects.create(**validated_data)
        for lesson in lessons:
            Lesson.objects.create(**lesson, course=course)
        return course

    def update(self, instance, validated_data):
        lessons = validated_data.pop('lessons')
        instance.course_id = validated_data.get('course_id', instance.course_id)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.taught_by = validated_data.get('taught_by', instance.taught_by)
        keep_choice = []
        # existing_ids = [lesson.id for lesson in instance.lessons]
        for lesson in lessons:
            if 'id' in lesson.keys():
                if Lesson.objects.filter(id=lesson['id']).exists():
                    l = Lesson.objects.get(id=lesson['id'])
                    l.name = lesson.get('name', l.name)
                    l.created_by = lesson.get('created_by', l.created_by)
                    l.save()
                    keep_choice.append(l.id)
                else:
                    continue
            else:
                l = Lesson.objects.create(**lesson, course=instance)
                keep_choice.append(l.id)
        for lesson in instance.lessons:
            if lesson.id not in keep_choice:
                lesson.delete()


class CourseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'course_id',
            'name',
            'description',
            'taught_by'
        ]


class LessonInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Lesson
        fields = [
            'id',
            'lesson_id',
            'name',
            'created_by',
            'created_at',
            'course'
        ]


class EnrollStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnrollStudent
        fields = [
            'id',
            'student_id',
            'course_id'
        ]


# class EnrollUserSerializer(serializers.ModelSerializer):
#     enroll_student = EnrollStudentSerializer
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'username', 'last_name', 'email', 'enroll_student']

# Working fine
class EnrollUserSerializer(serializers.Serializer):
    # student_id = UserSerializer()
    #
    # class Meta:
    #     model = EnrollStudent
    #     fields = ['id', 'student_id', 'enrolled_at']





    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=30)
    username = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.CharField(max_length=30)
    enrolled_at = serializers.DateTimeField()
