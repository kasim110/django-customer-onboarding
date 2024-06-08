# Django AWS Textract Integration

This project demonstrates how to integrate AWS Textract for document text extraction in a Django project using Django REST framework. The API allows users to upload documents, extract text using AWS Textract, and retrieve extracted text data.

## API Endpoints

### Document Upload and Extraction

### User Authentication Endpoints
- **Endpoint:** `POST /customer/user-login/`
- **Description:** Log in an existing user and retrieve an authentication token.
- **Request Body:**
    - `username` :"existing_user"
    - `password`: "password123"
- **Response:** Returns an authentication token for the logged-in user.

#### Customer Creation Endpoint
- **Endpoint:** `POST /customer/create-customer/`
- **Description:** Upload a document (front and back sides if applicable) and extract text using AWS Textract. Creates a customer and customer document record based on the extracted data.
- **Request Body:**
    - `Authorization`: Token `<your_token>`
    - `attached_file` (file): The document to be uploaded.

- **Response:**  Returns details of the created customer and associated document.

## Project Structure

- `customer/`: Django app containing models, serializers, views, and URLs related to document management and text extraction.
    - `models.py`: Defines models for countries, document sets, customers, and customer documents.
    - `serializers.py`: Defines serializers for the models.
    - `views.py`: Defines views to handle document upload and retrieval.
    - `urls.py`: Maps URLs to the views.
    - `utils.py`: Contains utility functions for data extraction from documents.
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