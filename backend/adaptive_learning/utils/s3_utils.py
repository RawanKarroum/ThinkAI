import boto3
import fitz  
import requests
from django.conf import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name=settings.AWS_REGION,
)

def generate_presigned_url(s3_key, expiration=3600):
    """
    Generate a presigned S3 URL for secure file access.
    :param s3_key: The key (path) of the file in S3.
    :param expiration: Expiration time in seconds.
    :return: Presigned URL or None.
    """
    if not s3_key:
        return None

    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": s3_key},
            ExpiresIn=expiration,
        )
        return presigned_url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None


# def extract_text_from_s3(pdf_url):
#     """
#     Downloads a PDF from S3, extracts text using PyMuPDF, and returns the text content.
#     :param pdf_url: Presigned URL of the PDF in S3.
#     :return: Extracted text.
#     """
#     try:
#         response = requests.get(pdf_url, stream=True)
#         response.raise_for_status()  
        
#         with fitz.open(stream=response.content, filetype="pdf") as doc:
#             text = "\n".join(page.get_text("text") for page in doc)
        
#         return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return None
