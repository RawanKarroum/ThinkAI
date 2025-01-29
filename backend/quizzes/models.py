from django.db import models
from AbstractSoftDelete.models import AbstractSoftDeleteModel
from courses.models import Courses
from content.models import PDFDocument

class Quizzes(AbstractSoftDeleteModel):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    pdf = models.ForeignKey(PDFDocument , on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'quizzes'

    def __str__(self):        
        return self.title

class QuizQuestions(AbstractSoftDeleteModel):
    """
    Model to store the questions for a quiz
    """
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    question_text = models.TextField()

    OPTON_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer')
    ]
    question_type = models.CharField(max_length=15, choices=OPTON_CHOICES)

    option_a = models.CharField(max_length=255, null=True, blank=True)
    option_b = models.CharField(max_length=255, null=True, blank=True)
    option_c = models.CharField(max_length=255, null=True, blank=True)
    option_d = models.CharField(max_length=255, null=True, blank=True)

    correct_answer = models.TextField(null=True, blank=True)
    explanation = models.TextField(null=True, blank=True)    

    class Meta:
        db_table = 'quiz_questions'

    def __str__(self):
        return f"Question {self.id} - {self.quiz.title}"
