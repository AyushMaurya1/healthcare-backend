# Healthcare Backend

A Django REST Framework (DRF) backend for a healthcare application, built with Django, PostgreSQL, and JWT authentication. This project allows users to register, log in, and manage patient and doctor records securely, including assigning doctors to patients.

## Project Overview

This project fulfills the requirements of the **Django Assignment: Building a Healthcare Backend**. It provides RESTful API endpoints for user authentication, patient management, doctor management, and patient-doctor mappings, using Django ORM for database interactions and `djangorestframework-simplejwt` for JWT-based authentication.

### Features
- **User Authentication**: Register and log in users with JWT tokens.
- **Patient Management**: CRUD operations for patients, restricted to the authenticated user’s own patients.
- **Doctor Management**: CRUD operations for doctors, accessible to all authenticated users.
- **Patient-Doctor Mappings**: Assign doctors to patients and manage mappings with permission checks.
- **Security**: Uses JWT authentication and custom permissions to ensure users can only manage their own data.
- **Database**: PostgreSQL with Django ORM for efficient data handling.
- **Admin Panel**: Fully functional Django admin interface for managing all models.
- **Environment Variables**: Secure configuration using a `.env` file.

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip and virtualenv
- Git (optional, for cloning)
- Postman or another API client for testing

### Installation
1. **Clone the Repository** (if using Git):
   ```bash
   git clone <repository-url>
   cd healthcare_backend
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   See `requirements.txt` for the full list of dependencies.

4. **Set Up PostgreSQL**:
   - Install PostgreSQL and create a database named `healthcare_db`.
   - Configure the database credentials in a `.env` file in the project root:
     ```ini
     SECRET_KEY=your-secret-key-here
     DEBUG=True
     DB_NAME=healthcare_db
     DB_USER=your-db-user
     DB_PASSWORD=your-db-password
     DB_HOST=localhost
     DB_PORT=5432
     ```
   - Ensure `.env` is included in `.gitignore` for security.

5. **Apply Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser** (for admin panel access):
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set up an email, name, and password.

7. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   The server will start at `http://127.0.0.1:8000/`.

8. **Access the Application**:
   - **API Root**: `http://127.0.0.1:8000/` (returns a JSON with available endpoints)
   - **Admin Panel**: `http://127.0.0.1:8000/admin/` (log in with superuser credentials)

## API Endpoints

All endpoints are prefixed with `/api/`. Authenticated endpoints require an `Authorization: Bearer <access_token>` header, obtained from the login endpoint.

### Authentication APIs
- **POST /api/auth/register/**: Register a new user.
  - **Body**:
    ```json
    {
        "name": "string",
        "email": "string",
        "password": "string"
    }
    ```
  - **Response** (201 Created):
    ```json
    {
        "user": {
            "id": 1,
            "name": "Alice Smith",
            "email": "alice@example.com"
        },
        "message": "User registered successfully"
    }
    ```
  - **Error**: Duplicate email (400 Bad Request):
    ```json
    {
        "email": ["user with this email already exists."]
    }
    ```

- **POST /api/auth/login/**: Log in and obtain JWT tokens.
  - **Body**:
    ```json
    {
        "email": "string",
        "password": "string"
    }
    ```
  - **Response** (200 OK):
    ```json
    {
        "refresh": "<refresh_token>",
        "access": "<access_token>"
    }
    ```
  - **Error**: Invalid credentials (401 Unauthorized):
    ```json
    {
        "detail": "No active account found with the given credentials"
    }
    ```

- **POST /api/auth/token/refresh/**: Refresh an access token.
  - **Body**:
    ```json
    {
        "refresh": "<refresh_token>"
    }
    ```
  - **Response** (200 OK):
    ```json
    {
        "access": "<new_access_token>"
    }
    ```

### Patient Management APIs (Authenticated)
- **POST /api/patients/**: Create a new patient.
  - **Body**:
    ```json
    {
        "first_name": "string",
        "last_name": "string",
        "date_of_birth": "YYYY-MM-DD",
        "gender": "M|F|O",
        "address": "string",
        "phone_number": "string",
        "email": "string",
        "medical_history": "string"
    }
    ```
  - **Response** (201 Created):
    ```json
    {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
        "gender": "M",
        "address": "123 Health St",
        "phone_number": "1234567890",
        "email": "john.doe@example.com",
        "medical_history": "No major issues",
        "created_by": "alice@example.com",
        "created_at": "2025-09-20T18:30:00Z"
    }
    ```

- **GET /api/patients/**: List patients created by the authenticated user.
  - **Response** (200 OK):
    ```json
    [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "gender": "M",
            "address": "123 Health St",
            "phone_number": "1234567890",
            "email": "john.doe@example.com",
            "medical_history": "No major issues",
            "created_by": "alice@example.com",
            "created_at": "2025-09-20T18:30:00Z"
        }
    ]
    ```

- **GET /api/patients/<id>/**: Get details of a specific patient.
- **PUT /api/patients/<id>/**: Update patient details.
- **DELETE /api/patients/<id>/**: Delete a patient.
  - **Response** (204 No Content):
    ```json
    {
        "message": "Patient deleted successfully"
    }
    ```

### Doctor Management APIs (Authenticated)
- **POST /api/doctors/**: Create a new doctor.
  - **Body**:
    ```json
    {
        "first_name": "string",
        "last_name": "string",
        "specialty": "string",
        "phone_number": "string",
        "email": "string",
        "license_number": "string"
    }
    ```
  - **Response** (201 Created):
    ```json
    {
        "id": 1,
        "first_name": "Emily",
        "last_name": "Carter",
        "specialty": "Cardiology",
        "phone_number": "9876543210",
        "email": "emily.carter@example.com",
        "license_number": "LIC123",
        "created_at": "2025-09-20T18:30:00Z"
    }
    ```

- **GET /api/doctors/**: List all doctors.
- **GET /api/doctors/<id>/**: Get details of a specific doctor.
- **PUT /api/doctors/<id>/**: Update doctor details.
- **DELETE /api/doctors/<id>/**: Delete a doctor.
  - **Response** (204 No Content):
    ```json
    {
        "message": "Doctor deleted successfully"
    }
    ```

### Patient-Doctor Mapping APIs (Authenticated)
- **POST /api/mappings/**: Assign a doctor to a patient.
  - **Body**:
    ```json
    {
        "patient": <patient_id>,
        "doctor": <doctor_id>
    }
    ```
  - **Response** (201 Created):
    ```json
    {
        "id": 1,
        "patient": 1,
        "doctor": 1,
        "patient_name": "John Doe",
        "doctor_name": "Dr. Emily Carter",
        "assigned_at": "2025-09-20T18:30:00Z"
    }
    ```
  - **Error**: Non-owned patient (400 Bad Request):
    ```json
    {
        "detail": "You can only assign doctors to your own patients."
    }
    ```

- **GET /api/mappings/**: List all patient-doctor mappings.
- **GET /api/mappings/by-patient/<patient_id>/**: List doctors assigned to a patient.
- **DELETE /api/mappings/<id>/**: Remove a doctor from a patient.
  - **Response** (204 No Content):
    ```json
    {
        "message": "Mapping deleted successfully"
    }
    ```

## Authentication
- **JWT**: Uses `djangorestframework-simplejwt` for token-based authentication.
- **Process**:
  1. Register or log in to obtain an `access` token.
  2. Include `Authorization: Bearer <access_token>` in headers for protected endpoints.
  3. Refresh tokens using `/api/auth/token/refresh/` if expired.
- **Permissions**:
  - `IsAuthenticated`: Required for all endpoints except `/api/auth/register/`.
  - `IsOwner`: Ensures users can only manage their own patients and mappings.

## Database
- **Backend**: PostgreSQL.
- **ORM**: Django ORM for all database interactions (model definitions, queries, relationships).
- **Models**:
  - `User`: Custom user model with email as the primary identifier.
  - `Patient`: Stores patient details, linked to the creating user.
  - `Doctor`: Stores doctor details.
  - `PatientDoctorMapping`: Manages patient-doctor relationships.

## Testing
- **Tool**: Postman was used to test all API endpoints.
- **Test Cases**:
  - Successful CRUD operations for all endpoints (200, 201, 204).
  - Error handling: Invalid inputs (400), unauthorized access (401), forbidden actions (403).
- **Admin Panel**: Accessible at `/admin/`, showing all models (`Users`, `Patients`, `Doctors`, `PatientDoctorMappings`) with data.

## Project Structure
```
healthcare_backend/
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
├── .env
├── .gitignore
├── manage.py
├── requirements.txt
├── README.md
```

## Notes
- **Security**: Environment variables in `.env` (excluded from version control via `.gitignore`).
- **Best Practices**: Modular app structure, custom permissions, and error handling.
- **Error Handling**: Validation errors, authentication failures, and permission checks are implemented.
- **Admin Panel**: Registered all models for easy data management.

## Troubleshooting
- **Database Issues**: Ensure PostgreSQL is running and `.env` credentials are correct.
- **401 Unauthorized**: Refresh the JWT token using `/api/auth/token/refresh/`.
- **405 Method Not Allowed**: Verify correct URL and method (e.g., `DELETE /api/mappings/<id>/`).
- **Test Evidence**: Run all API endpoints requests in POSTMAN.

For further assistance, contact the developer or refer to the Django/DRF documentation.