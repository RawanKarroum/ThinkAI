from .models import PDFDocument
from .serializers import PDFDocumentSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class UploadPDFView(APIView):
    permission_classes = [AllowAny]

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        print("Authenticated User:", request.user)
        print("User is authenticated:", request.user.is_authenticated)
        print("Request Data:", request.data)
        print("Request Files:", request.FILES)

        data = request.data.copy()
        data.update(request.FILES) 

        file_serializer = PDFDocumentSerializer(data=data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response({"message": "File uploaded successfully!", "data": file_serializer.data}, status=201)
        
        print("Serializer Errors:", file_serializer.errors)
        return Response(file_serializer.errors, status=400)
