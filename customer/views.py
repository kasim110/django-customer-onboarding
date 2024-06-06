import boto3
import json
from django.conf import settings
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomerDocumentModel
from .serializers import CustomerDocumentSerializer

class DocumentUploadView(generics.CreateAPIView):
    queryset = CustomerDocumentModel.objects.all()
    serializer_class = CustomerDocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        document = self.request.FILES['attached_file']
        customer = self.request.data.get('customer')

        # Save the document to the model
        instance = serializer.save(attached_file=document, customer_id=customer)

        # Initialize Textract client
        client = boto3.client(
            'textract',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME
        )

        # Read document content
        document_path = instance.attached_file.path
        with open(document_path, 'rb') as doc_file:
            image_bytes = doc_file.read()

        # Call Amazon Textract
        response = client.detect_document_text(Document={'Bytes': image_bytes})

        # Process extracted text
        extracted_text = ''
        for item in response['Blocks']:
            if item['BlockType'] == 'LINE':
                extracted_text += item['Text'] + '\n'

        # Save extracted data to the model
        extracted_json = json.dumps(response, indent=4)
        instance.extracted_json = extracted_json
        instance.save()

class DocumentDetailView(generics.RetrieveAPIView):
    queryset = CustomerDocumentModel.objects.all()
    serializer_class = CustomerDocumentSerializer