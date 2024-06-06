# Django AWS Textract Integration

This project demonstrates how to integrate AWS Textract for document text extraction in a Django project using Django REST framework. The API allows users to upload documents, extract text using AWS Textract, and retrieve extracted text data.

## API Endpoints

### Document Upload and Extraction

#### Upload Document
- **Endpoint:** `POST /customer/upload-document/`
- **Description:** Upload a document and extract text using AWS Textract.
- **Request Body:**
    - `attached_file` (file): The document to be uploaded.
    - `customer` (integer): The ID of the customer associated with the document.
- **Example Request (cURL):**
    ```bash
    curl -X POST http://127.0.0.1:8000/customer/upload-document/ \
    -H "Content-Type: multipart/form-data" \
    -F "attached_file=@/path/to/your/document.pdf" \
    -F "customer=1"
    ```
- **Response:** Returns details of the uploaded document and extracted text data.

#### Retrieve Document Details
- **Endpoint:** `GET /customer/document/<int:pk>/`
- **Description:** Retrieve details of a specific document, including extracted text data.
- **Example Request (cURL):**
    ```bash
    curl -X GET http://127.0.0.1:8000/customer/document/1/
    ```
- **Response:** Returns details of the specified document, including extracted text data.

## Project Structure

- `customer/`: Django app containing models, serializers, views, and URLs related to document management and text extraction.
    - `models.py`: Defines models for countries, document sets, customers, and customer documents.
    - `serializers.py`: Defines serializers for the models.
    - `views.py`: Defines views to handle document upload and retrieval.
    - `urls.py`: Maps URLs to the views.
- `customer_onboarding/settings.py`: Django project settings, including AWS credentials configuration.

## Running the Project

1. **Install required packages:**
    ```bash
    pip install -r requirement.txt
    ```
2. **Apply migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
3. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```
4. **Start the development server:**
    ```bash
    python manage.py runserver
    ```

## Configuration

### AWS Credentials

Configure your AWS credentials in `settings.py`:

```python
# settings.py

AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
AWS_REGION_NAME = 'your-region'  # e.g., 'us-east-1'