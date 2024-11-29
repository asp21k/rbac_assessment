from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User, Role, Permission, UserRole

class AuthenticationTests(APITestCase):
    def setUp(self):
        # Create test permission
        self.permission = Permission.objects.create(
            name='Test Permission',
            codename='test_permission'
        )
        
        self.user_data = {
            'email': 'test1@example.com',
            'username': 'test1user',
            'password': 'Test1Pass123!',
            'first_name': 'Test1',
            'last_name': 'User1'
        }

    def test_user_registration(self):
        url = reverse('auth-register')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_user_login(self):
        # Create user first
        User.objects.create_user(
            email='test1@example.com',
            username='test1user',
            password='Test1Pass123!'
        )
        
        url = reverse('auth-login')
        login_data = {
            'email': 'test1@example.com',
            'password': 'Test1Pass123!'
        }
        response = self.client.post(url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class RolePermissionTests(APITestCase):
    def setUp(self):
        # Create permissions
        permission = Permission.objects.create(name="manage_roles", codename="manage_roles")
        permission1 = Permission.objects.create(name="manage_users", codename="manage_user_roles")
        
        # Create a role and assign permissions to the role
        role = Role.objects.create(name="Admin")
        role.permissions.add(permission, permission1)

        # Create a user and assign the role to the user
        user = User.objects.create_user(email="testuser@example.com", password="password123", username="testuser")
        UserRole.objects.create(user=user, role=role)

        self.user = user
        # self.role = role
        self.permission = permission
        self.permission1 = permission1
        self.role = role
        # Assign user to a role (if needed in your tests)
        self.client.force_authenticate(user=self.user)

    def test_acreate_role(self):
        url = reverse('role-list')
        data = {"name": "New Role", "description": "A new role description"}
        
        response = self.client.post(url, data)
       
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       
    def test_assign_role_to_user(self):
        url = reverse('userrole-list')

        # Check if the user already has the role assigned
        if not UserRole.objects.filter(user=self.user, role=self.role).exists():
            data = {"user": self.user.id, "role": self.role.id}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        else:
            print(f"User {self.user.id} already has role {self.role.id}.")
            # Optionally, you can assert that this role already exists, if necessary.
            self.assertTrue(UserRole.objects.filter(user=self.user, role=self.role).exists())
