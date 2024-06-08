from django.urls import path
from customer import views

urlpatterns = [
    path('user-login/',views.UserLoginView.as_view(),name='user_login'),
    path('create-customer/', views.CreateCustomerFromDocumentView.as_view(), name='create_customer'),
    # path('upload-document/', views.DocumentUploadView.as_view(), name='upload_document'),
    # path('document/<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
]