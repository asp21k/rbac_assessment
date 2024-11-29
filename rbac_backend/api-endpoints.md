# API Endpoints Documentation

## Base URL: `http://localhost:8000/api`

## Authentication Endpoints

### 1. Register User
- **URL:** `/auth/register/`
- **Method:** `POST`
- **Permission:** None (Public)
- **Request Body:**
```json
{
    "email": "user@example.com",
    "username": "username",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890"
}
```
- **Success Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "1234567890",
        "is_active": true
    }
}
```

### 2. Login
- **URL:** `/auth/login/`
- **Method:** `POST`
- **Permission:** None (Public)
- **Request Body:**
```json
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}
```
- **Success Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

## User Management Endpoints

### 1. List Users
- **URL:** `/users/`
- **Method:** `GET`
- **Permission:** `manage_users` or `view_users`
- **Headers:** `Authorization: Bearer <token>`
- **Success Response:**
```json
[
    {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "first_name": "John",
        "last_name": "Doe",
        "is_active": true
    }
]
```

### 2. Create User
- **URL:** `/users/`
- **Method:** `POST`
- **Permission:** `manage_users`
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
```json
{
    "email": "newuser@example.com",
    "username": "newuser",
    "password": "SecurePass123!",
    "first_name": "Jane",
    "last_name": "Smith"
}
```

### 3. Get User Detail
- **URL:** `/users/{id}/`
- **Method:** `GET`
- **Permission:** `manage_users` or `view_users`
- **Headers:** `Authorization: Bearer <token>`

### 4. Update User
- **URL:** `/users/{id}/`
- **Method:** `PUT`
- **Permission:** `manage_users`
- **Headers:** `Authorization: Bearer <token>`

### 5. Delete User
- **URL:** `/users/{id}/`
- **Method:** `DELETE`
- **Permission:** `manage_users`
- **Headers:** `Authorization: Bearer <token>`

## Role Management Endpoints

### 1. List Roles
- **URL:** `/roles/`
- **Method:** `GET`
- **Permission:** `manage_roles` or `view_roles`
- **Headers:** `Authorization: Bearer <token>`
- **Success Response:**
```json
[
    {
        "id": 1,
        "name": "Admin",
        "description": "Administrator role",
        "permissions": [
            {
                "id": 1,
                "name": "Manage Users",
                "codename": "manage_users"
            }
        ]
    }
]
```

### 2. Create Role
- **URL:** `/roles/`
- **Method:** `POST`
- **Permission:** `manage_roles`
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
```json
{
    "name": "New Role",
    "description": "Description of new role",
    "permission_ids": [1, 2, 3]
}
```

### 3. Get Role Detail
- **URL:** `/roles/{id}/`
- **Method:** `GET`
- **Permission:** `manage_roles` or `view_roles`
- **Headers:** `Authorization: Bearer <token>`

### 4. Update Role
- **URL:** `/roles/{id}/`
- **Method:** `PUT`
- **Permission:** `manage_roles`
- **Headers:** `Authorization: Bearer <token>`

### 5. Delete Role
- **URL:** `/roles/{id}/`
- **Method:** `DELETE`
- **Permission:** `manage_roles`
- **Headers:** `Authorization: Bearer <token>`

## Permission Management Endpoints

### 1. List Permissions
- **URL:** `/permissions/`
- **Method:** `GET`
- **Permission:** `manage_permissions`
- **Headers:** `Authorization: Bearer <token>`
- **Success Response:**
```json
[
    {
        "id": 1,
        "name": "Manage Users",
        "codename": "manage_users",
        "description": "Can manage user accounts"
    }
]
```

### 2. Create Permission
- **URL:** `/permissions/`
- **Method:** `POST`
- **Permission:** `manage_permissions`
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
```json
{
    "name": "New Permission",
    "codename": "new_permission",
    "description": "Description of new permission"
}
```

### 3. Get Permission Detail
- **URL:** `/permissions/{id}/`
- **Method:** `GET`
- **Permission:** `manage_permissions`
- **Headers:** `Authorization: Bearer <token>`

### 4. Update Permission
- **URL:** `/permissions/{id}/`
- **Method:** `PUT`
- **Permission:** `manage_permissions`
- **Headers:** `Authorization: Bearer <token>`

### 5. Delete Permission
- **URL:** `/permissions/{id}/`
- **Method:** `DELETE`
- **Permission:** `manage_permissions`
- **Headers:** `Authorization: Bearer <token>`

## User Role Management Endpoints

### 1. List User Roles
- **URL:** `/user-roles/`
- **Method:** `GET`
- **Permission:** `manage_user_roles`
- **Headers:** `Authorization: Bearer <token>`
- **Success Response:**
```json
[
    {
        "id": 1,
        "user": 1,
        "role": 1,
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

### 2. Assign Role to User
- **URL:** `/user-roles/`
- **Method:** `POST`
- **Permission:** `manage_user_roles`
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
```json
{
    "user": 1,
    "role": 1
}
```

### 3. Get User Role Detail
- **URL:** `/user-roles/{id}/`
- **Method:** `GET`
- **Permission:** `manage_user_roles`
- **Headers:** `Authorization: Bearer <token>`

### 4. Delete User Role
- **URL:** `/user-roles/{id}/`
- **Method:** `DELETE`
- **Permission:** `manage_user_roles`
- **Headers:** `Authorization: Bearer <token>`

## Error Responses

### Authentication Error
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Permission Error
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### Validation Error
```json
{
    "field_name": [
        "Error message"
    ]
}
```

### Not Found Error
```json
{
    "detail": "Not found."
}
```

## Testing the Endpoints

You can test these endpoints using tools like:
- cURL
- Postman
- Thunder Client
- Python requests library

Example cURL request:
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
    -H "Content-Type: application/json" \
    -d '{"email":"user@example.com","password":"SecurePass123!"}'

# Get users (with token)
curl http://localhost:8000/api/users/ \
    -H "Authorization: Bearer <your_token>"
```
