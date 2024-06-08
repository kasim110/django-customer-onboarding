from rest_framework import serializers
from .models import CustomerDocumentModel, CustomerModel

class CustomerDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDocumentModel
        fields = ['id', 'customer', 'attached_file','extracted_json']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = ['id', 'surname', 'firstname', 'nationality', 'gender', 'created_by']