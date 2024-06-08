import json
from django.conf import settings
from rest_framework import generics,status,views
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import CustomerDocumentModel,CountryModel
from .serializers import CustomerDocumentSerializer,CustomerSerializer
from .utils import extract_text_from_document
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token




class UserLoginView(views.APIView):

    def post(self,request,*args, **kwargs):
        data = request.data
        username = data.get('username',None)
        password = data.get('password',None)

        if not username or not password:
            return Response({'success':False, 'data':{}, 'message':'Provide username or password'},status=status.HTTP_400_BAD_REQUEST)
        
        user = None
        user = User.objects.filter(username=username).first()

        
        if not user:
            return Response({'success':False, 'data':{}, 'message':'Invalid credentials! '},status=status.HTTP_403_FORBIDDEN)
        
        if user.check_password(password):
            if user.is_active:
                resp = {
                    'user_id': user.id,
                    'first_name' : user.first_name,
                    'last_name' : user.last_name,
                    'auth_token': self.get_auth_token(user)
                }
                return Response({'success':True, 'data':resp, 'message':'Successfully Logged In! '},status=status.HTTP_200_OK)
            else:
                return Response({'success':False, 'data':{}, 'message':'Account deactivated! Contant Admin.'},status=status.HTTP_403_FORBIDDEN)
            
        return Response({'success':False, 'data':{}, 'message':'Invalid credentials! , Check username or password '},status=status.HTTP_403_FORBIDDEN)
    

    def get_auth_token(self, user:User) ->dict:
        
        token, created = Token.objects.get_or_create(user=user)
        token_reponse = {
            'token' : str(token.key),
        }
        return token_reponse

class CreateCustomerFromDocumentView(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    

    def post(self, request, *args, **kwargs):
        if 'attached_file' not in request.data:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.data['attached_file']
        extracted_data = extract_text_from_document(file)
        
        if 'surname' not in extracted_data or 'firstname' not in extracted_data:
            return Response({"error": "Required fields not found in the document"}, status=status.HTTP_400_BAD_REQUEST)

        nationality = extracted_data.get('nationality')
        if nationality:
            try:
                county_object = CountryModel.objects.get(name__icontains=nationality)
            except ObjectDoesNotExist:     
                return Response({"status":False,"message":"Country does not exist"},status=status.HTTP_404_NOT_FOUND)

        customer_data = {
            'surname': extracted_data.get('surname'),
            'firstname': extracted_data.get('firstname'),
            'nationality': county_object.id,  
            'gender': extracted_data.get('gender'),
            'created_by': request.user.id
        }

        customer_serializer = CustomerSerializer(data=customer_data)
        customer_serializer.is_valid(raise_exception=True)
        customer = customer_serializer.save()

        customer_document_serializer = CustomerDocumentSerializer(data={
            'customer': customer.id,
            'attached_file': file,
            'extracted_json': json.dumps(extracted_data),
        })
        customer_document_serializer.is_valid(raise_exception=True)
        customer_document_serializer.save()

        return Response({"status":True,"message":"Customer created successfully!"}, status=status.HTTP_201_CREATED)



# class DocumentUploadView(generics.CreateAPIView):
#     queryset = CustomerDocumentModel.objects.all()
#     serializer_class = CustomerDocumentSerializer
#     parser_classes = (MultiPartParser, FormParser)

#     def perform_create(self, serializer):
#         document = self.request.FILES['attached_file']
#         customer = self.request.data.get('customer')

#         # Save the document to the model
#         instance = serializer.save(attached_file=document, customer_id=customer)

#         # Initialize Textract client
#         client = boto3.client(
#             'textract',
#             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#             region_name=settings.AWS_REGION_NAME
#         )

#         # Read document content
#         document_path = instance.attached_file.path
#         with open(document_path, 'rb') as doc_file:
#             image_bytes = doc_file.read()

#         # Call Amazon Textract
#         response = client.detect_document_text(Document={'Bytes': image_bytes})

#         # Process extracted text
#         extracted_text = ''
#         for item in response['Blocks']:
#             if item['BlockType'] == 'LINE':
#                 extracted_text += item['Text'] + '\n'

#         # Save extracted data to the model
#         extracted_json = json.dumps(response, indent=4)
#         instance.extracted_json = extracted_json
#         instance.save()

# class DocumentDetailView(generics.RetrieveAPIView):
#     queryset = CustomerDocumentModel.objects.all()
#     serializer_class = CustomerDocumentSerializer