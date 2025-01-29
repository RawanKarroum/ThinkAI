from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Quizzes, QuizQuestions
from content.models import PDFDocument
from .serializers import QuizzesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from adaptive_learning.utils.quiz_utils import generate_and_save_quiz
import traceback

class QuizzesViewSet(viewsets.ModelViewSet):
    queryset = Quizzes.objects.all()
    serializer_class = QuizzesSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    
    # def get_queryset(self):
    #     """
    #     Filter quizzes based on the authenticated user's role.
    #     """
    #     user = self.request.user

    #     # Ensure the user is authenticated
    #     if not user.is_authenticated:
    #         return Quizzes.objects.none()

    #     # If the user is a teacher, return quizzes for courses they teach
    #     if user.role == 'teacher':
    #         return Quizzes.objects.filter(course__teacher=user, deleted_at__isnull=True)

    #     # If the user is a student, return quizzes for courses they're enrolled in
    #     return Quizzes.objects.filter(course__students=user, deleted_at__isnull=True)

    def get_queryset(self):
        """
        Return all quizzes, ignoring user authentication.
        """
        return Quizzes.objects.filter(deleted_at__isnull=True)
    
class GenerateQuizView(APIView):
    """
    API to generate a quiz
    """
    def post(self, request, pdf_id):
        try: 
            pdf_doc = PDFDocument.objects.get(id=pdf_id)

            if not pdf_doc.extracted_text:
                return Response({"message": "PDF Document text not extracted"}, status=400)
            
            quiz_data = generate_and_save_quiz(pdf_doc)

            return Response({"message": "Quiz generated successfully!", "data": quiz_data}, status=201)
        
        except PDFDocument.DoesNotExist:
            return Response({"message": "PDF Document not found"}, status=404)
        except Exception as e:
            error_details = traceback.format_exc() 
            print(f"ERROR - Quiz generation failed: {e}\n{error_details}")  
            
            return Response({"message": "An error occurred while generating the quiz", "error": str(e)}, status=500)
            
            
