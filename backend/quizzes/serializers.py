from rest_framework import serializers
from .models import Quizzes, QuizQuestions

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
        'pdf',
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
    
class QuizQuestionsSerializer(serializers.ModelSerializer):
    """"
    Serializer for QuizQuestions model
    """

    class Meta:
        model = QuizQuestions

        fields = [
            'id',
            'quiz',
            'question_text',
            'question_type',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_answer',
            'explanation',
        ]

    def validate(self, attrs):
        """
        Validate the input data for the quiz questions.
        """
        question_type = attrs.get('question_type')

        if question_type == 'multiple_choice':
            if not attrs.get('correct answer') or attrs['correct_answer'] not in ['A', 'B', 'C', 'D']:
                raise serializers.ValidationError({'correct_answer': 'Must be A, B, C, or D for multiple choice questions.'})
            
            if not all([attrs.get('option_a'), attrs.get('option_b'), attrs.get('option_c'), attrs.get('option_d')]):
                raise serializers.ValidationError({'options': 'All options must be provided for multiple choice questions.'})
            
        elif question_type == 'true_false':
            if not attrs.get('correct_answer') or attrs['correct_answer'] not in [True, False]:
                raise serializers.ValidationError({'correct_answer': 'Must be True or False for true/false questions.'})
            
        elif question_type == 'short_answer':
            if not attrs.get('correct_answer'):
                raise serializers.ValidationError({'correct_answer': 'Correct answer must be provided for short answer questions.'})
            
        return attrs
    
    def create(self, validated_data):
        """
        Create a new quiz question.
        """
        return QuizQuestions.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update an existing quiz question.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
