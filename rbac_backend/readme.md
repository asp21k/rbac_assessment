# RBAC Backend System

A Role-Based Access Control (RBAC) system built with Django REST Framework, providing secure authentication and authorization management.

## Features

- JWT-based authentication
- Role-based access control (RBAC)
- User management
- Permission management
- Role management
- Secure API endpoints
- Automated testing suite

## Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rbac-backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Unix/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in the root directory:
```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Load initial test data :
```bash
python manage.py setup_test_data
```

## Running the Server

```bash
python manage.py runserver
```

The server will start at http://localhost:8000

## API Endpoints

### Authentication
- POST `/api/auth/register/` - Register new user
- POST `/api/auth/login/` - Login user

### Users
- GET `/api/users/` - List all users
- POST `/api/users/` - Create new user
- GET `/api/users/{id}/` - Get user details
- PUT `/api/users/{id}/` - Update user
- DELETE `/api/users/{id}/` - Delete user

### Roles
- GET `/api/roles/` - List all roles
- POST `/api/roles/` - Create new role
- GET `/api/roles/{id}/` - Get role details
- PUT `/api/roles/{id}/` - Update role
- DELETE `/api/roles/{id}/` - Delete role

### Permissions
- GET `/api/permissions/` - List all permissions
- POST `/api/permissions/` - Create new permission
- GET `/api/permissions/{id}/` - Get permission details
- PUT `/api/permissions/{id}/` - Update permission
- DELETE `/api/permissions/{id}/` - Delete permission

### User Roles
- GET `/api/user-roles/` - List all user roles
- POST `/api/user-roles/` - Assign role to user
- DELETE `/api/user-roles/{id}/` - Remove role from user

## Authentication

The API uses JWT (JSON Web Token) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-token>
```

## Testing
You can test the application using Django's built-in test framework or Postman. For detailed API specifications and testing with Postman, refer to the api-endpoints.md file.


### Running Tests
```bash
# Run all tests
python manage.py test accounts.tests

# Run specific test file
python manage.py test accounts.tests.test_auth

# Run specific test class
python manage.py test accounts.tests.test_auth.AuthenticationTests
```

### Test Users

The `setup_test_data` command creates the following test users:

```
Super Admin:
- Email: superadmin@example.com
- Password: SuperAdmin123!

Admin:
- Email: admin@example.com
- Password: Admin123!

Moderator:
- Email: moderator@example.com
- Password: Moderator123!

User:
- Email: user@example.com
- Password: User123!
```

## Role Hierarchy

1. Super Admin
   - All permissions
   - Can manage roles and permissions
   - Can manage users

2. Admin
   - Can manage users
   - Can view roles
   - Limited system configuration

3. Moderator
   - Can view users
   - Can view roles
   - Limited user management

4. User
   - Basic access
   - Can view own profile
   - Can update own information

## Security Features

- Password hashing
- JWT token authentication
- Role-based authorization
- Permission-based access control
- CORS configuration
- Input validation
- XSS protection
- CSRF protection

## Development

### Adding New Endpoints

1. Create serializer in `accounts/serializers.py`
2. Create view in `accounts/views.py`
3. Add URL to `rbac_backend/urls.py`
4. Create tests in `accounts/tests/`

### Adding New Roles/Permissions

1. Create permission in Django admin or via API
2. Create role and assign permissions
3. Update tests accordingly

## Deployment Considerations

1. Set `DEBUG=False` in production
2. Use strong `SECRET_KEY`
3. Configure proper `ALLOWED_HOSTS`
4. Set up proper CORS configuration
5. Use HTTPS in production
6. Configure proper database (e.g., PostgreSQL)
7. Set up proper logging

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
