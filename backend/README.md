# SaaS Platform Backend

This is the backend service for the SaaS platform, built using FastAPI and PostgreSQL. The backend is designed to support multi-tenancy and provides a robust API for user and tenant management.

## Features

- **Multi-Tenant Architecture**: Supports multiple tenants with isolated data.
- **User Authentication**: Includes endpoints for user registration, login, and token management.
- **User Management**: CRUD operations for user data.
- **Tenant Management**: CRUD operations for tenant data.
- **API Versioning**: The API is versioned to ensure backward compatibility.

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Dependency Injection**: FastAPI's built-in dependency injection system
- **Authentication**: JWT (JSON Web Tokens)

## Getting Started

### Prerequisites

- Python 3.12
- PostgreSQL
- pip

### Installation

1. Clone the repository:

   git clone <repository-url>

2. Navigate to the backend directory:

   cd saas-platform/backend

3. Install the required packages:

   pip install -r requirements.txt

### Configuration

Update the `config.py` file with your database connection details and JWT secret key.

### Running the Application

To start the FastAPI application, run:

uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

### API Documentation

The API documentation is automatically generated and can be accessed at:

http://localhost:8000/docs

## Testing

To run the tests, navigate to the `tests` directory and execute:

pytest

## License

This project is licensed under the MIT License. See the LICENSE file for details.