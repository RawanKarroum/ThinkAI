from rest_framework import serializers
from .models import Quizzes

class QuizzesSerializer(serializers.ModelSerializer):
    """
    Serializer for Quizzes model
    """

    class Meta:
        model = Quizzes
        
        fields = [
        'id',
        'title',
        'course',
        ]

    def validate(self, attrs):
        """
        Validate the input data for the quizzes.
        """
        if not attrs.get('course'):
            raise serializers.ValidationError({'course': 'A valid course is required.'})
        return attrs

    def create(self, validated_data):
        """
        Create a new quiz.
        """
        return Quizzes.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing quiz.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    