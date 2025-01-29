from rest_framework import serializers
from .models import PDFDocument
from django.conf import settings
import boto3
from adaptive_learning.utils.s3_utils import generate_presigned_url

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

        return generate_presigned_url(s3_key)

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