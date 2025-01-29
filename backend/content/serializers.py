from rest_framework import serializers
from .models import PDFDocument
from django.conf import settings
import boto3

class PDFDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for PDFDocument Model
    """

    file_url = serializers.SerializerMethodField()

    class Meta:
        model = PDFDocument
        fields = [
            'id',
            'title',
            'file',
            'file_url',
        ]

    def get_file_url(self, obj):
        """
        Returns a temporary presigned URL for secure access
        """
        if not obj.file:
            return None
        
        s3_key = f"pdfs/{obj.file.name}" 

        print(f"DEBUG - AWS_S3_BUCKET: {settings.AWS_STORAGE_BUCKET_NAME}")
        print(f"DEBUG - Corrected File Key: {s3_key}")  

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION
        )

        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': s3_key},
            ExpiresIn=3600  
        )

        print(f"DEBUG - Corrected Presigned URL: {presigned_url}")

        return presigned_url

    def validate(self, attrs):
        """
        validate the uploaded file to make sure it is a pdf        
        """
        file = attrs.get('file')

        if file is None:
            raise serializers.ValidationError('No file was uploaded')

        if not file.name.lower().endswith('.pdf'):
            raise serializers.ValidationError('File must be a PDF')
        
        return attrs

    def create(self, validated_data):
        """
        create a new PDFDocument instance
        """
        return PDFDocument.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        update an existing PDFDocument instance
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance