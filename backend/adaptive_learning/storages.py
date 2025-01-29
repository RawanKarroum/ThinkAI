from storages.backends.s3boto3 import S3Boto3Storage

class PDFStorage(S3Boto3Storage):
    location = 'pdfs/'  
    file_overwrite = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(f"📌 PDFStorage initialized with bucket: {self.bucket_name}") 
