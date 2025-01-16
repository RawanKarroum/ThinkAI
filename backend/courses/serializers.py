from rest_framework import serializers
from .models import Courses

class CoursesSerializer(serializers.ModelSerializer):
    """
    Serializer for Courses model
    """

    class Meta:
        model = Courses
        
        fields = [
        'id',
        'title',
        'description',
        'teacher',
        ]
        # read_only_fields = ['teacher', 'students']

    def validate(self, attrs):
        """
        Check if the teacher is a teacher
        """
        teacher = attrs.get('teacher')

        if teacher is None:
            raise serializers.ValidationError({'teacher': "Teacher field is required."})

        if not hasattr(teacher, 'role') or teacher.role != 'teacher':
            raise serializers.ValidationError({'teacher': "Teacher must have the role 'teacher'."})

        return attrs

    def create(self, validated_data):
        """
        Create a new course
        """
        return Courses.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing course
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance