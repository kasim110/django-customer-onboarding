from django.urls import path
from .views import DocumentUploadView, DocumentDetailView

urlpatterns = [
    path('upload-document/', DocumentUploadView.as_view(), name='upload_document'),
    path('document/<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
]