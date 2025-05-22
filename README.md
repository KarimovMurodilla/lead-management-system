# Lead Management System

A Django REST Framework application for managing job application leads with automated email notifications and internal management capabilities.

## Features

- **Public Lead Submission**: Prospects can submit applications with resume uploads
- **Automated Email Notifications**: Confirmation emails to prospects and notifications to attorneys
- **Internal Lead Management**: Protected API for attorneys to view and update lead statuses
- **Status Tracking**: Leads transition from PENDING to REACHED_OUT status
- **File Upload Security**: Resume validation with size and type restrictions
- **JWT Authentication**: Secure token-based authentication for internal APIs
- **Rate Limiting**: Protection against API abuse
- **Docker Support**: Easy deployment with Docker Compose

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL 15
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Email Service**: Mailjet API
- **Containerization**: Docker, Docker Compose
- **Testing**: Django TestCase, DRF APITestCase

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Mailjet account (for email notifications)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/KarimovMurodilla/lead-management-system.git
cd lead-management-system
```

2. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` file with your configuration:
```env
# Database
DB_NAME=leads_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Mailjet (Get from https://app.mailjet.com/account/apikeys)
MAILJET_API_KEY=your_mailjet_api_key
MAILJET_SECRET_KEY=your_mailjet_secret_key
MAILJET_FROM_EMAIL=noreply@yourcompany.com
ATTORNEY_EMAIL=attorney@yourcompany.com

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

3. **Start the application**
```bash
docker-compose up --build
```

4. **Create a superuser (attorney account)**
```bash
docker-compose exec web python manage.py createsuperuser
```

5. **Access the application**
- API Base URL: `http://localhost:8000/api/`
- Admin Panel: `http://localhost:8000/admin/`

6. **Run tests**
```bash
docker-compose exec web python manage.py test
```

## API Documentation

### Public Endpoints

#### Create Lead
```
POST /api/leads/
Content-Type: multipart/form-data

Parameters:
- first_name (string, required): Prospect's first name
- last_name (string, required): Prospect's last name  
- email (string, required): Prospect's email address
- resume (file, required): Resume/CV file (PDF, DOC, DOCX, max 5MB)

Response: 201 Created
{
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "resume_url": "http://localhost:8000/media/resumes/resume.pdf",
    "status": "PENDING",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
}
```

### Protected Endpoints (Requires JWT Authentication)

#### Authentication Endpoints

##### Login (Get JWT Token)
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "attorney",
    "password": "your_password"
}

Response: 200 OK
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "attorney",
        "email": "attorney@example.com",
        "first_name": "John",
        "last_name": "Attorney",
        "is_staff": true
    }
}
```

##### Refresh Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}

Response: 200 OK
{
    "access": "new_access_token"
}
```

##### Verify Token
```http
GET /api/auth/verify/
Authorization: Bearer <access_token>

Response: 200 OK
{
    "user": {
        "id": 1,
        "username": "attorney",
        "email": "attorney@example.com",
        "first_name": "John",
        "last_name": "Attorney",
        "is_staff": true
    },
    "valid": true
}
```

##### Logout
```http
POST /api/auth/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "refresh_token": "your_refresh_token"
}

Response: 200 OK
{
    "message": "Successfully logged out"
}
```

##### Register New User (Staff Only)
```http
POST /api/auth/register/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "username": "new_attorney",
    "password": "secure_password123",
    "password_confirm": "secure_password123",
    "email": "new@example.com",
    "first_name": "Jane",
    "last_name": "Doe"
}

Response: 201 Created
{
    "id": 2,
    "username": "new_attorney",
    "email": "new@example.com",
    "first_name": "Jane",
    "last_name": "Doe"
}
```

##### Get/Update User Profile
```http
GET /api/auth/profile/
Authorization: Bearer <access_token>

Response: 200 OK
{
    "id": 1,
    "username": "attorney",
    "email": "attorney@example.com",
    "first_name": "John",
    "last_name": "Attorney",
    "is_staff": true
}

PATCH /api/auth/profile/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "first_name": "Updated Name",
    "email": "updated@example.com"
}
```

#### List All Leads
```http
GET /api/leads/list/
Authorization: Bearer <access_token>

Response: 200 OK
[
    {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "resume_url": "http://localhost:8000/media/resumes/resume.pdf",
        "status": "PENDING",
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    }
]
```

#### Get Specific Lead
```http
GET /api/leads/{id}/
Authorization: Bearer <access_token>

Response: 200 OK
{
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "resume_url": "http://localhost:8000/media/resumes/resume.pdf",
    "status": "PENDING",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
}
```

#### Update Lead Status
```http
PATCH /api/leads/{id}/update/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "status": "REACHED_OUT"
}

Response: 200 OK
{
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "resume_url": "http://localhost:8000/media/resumes/resume.pdf",
    "status": "REACHED_OUT",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:30:00Z"
}
```

#### Refresh JWT Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}

Response: 200 OK
{
    "access": "new_access_token"
}
```
