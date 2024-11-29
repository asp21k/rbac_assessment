from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User, Role, Permission, UserRole

class RolePermissionTests(APITestCase):
    def setUp(self):
        # Create required permissions
        self.manage_user_roles_perm = Permission.objects.create(name="Manage User Roles", codename="manage_user_roles")
        self.manage_roles_perm = Permission.objects.create(name="Manage Roles", codename="manage_roles")
        self.view_roles_perm = Permission.objects.create(name="View Roles", codename="view_roles")

        # Create roles and assign permissions
        self.admin_role = Role.objects.create(name="Admin")
        self.admin_role.permissions.add(self.manage_user_roles_perm, self.manage_roles_perm, self.view_roles_perm)

        self.moderator_role = Role.objects.create(name="Moderator")
        self.moderator_role.permissions.add(self.view_roles_perm)

        # Create an admin user and assign role
        self.admin_user = User.objects.create_user(email="admin@example.com", password="Admin123!", username="admin")
        UserRole.objects.create(user=self.admin_user, role=self.admin_role)

        # Create a regular user
        self.regular_user = User.objects.create_user(email="user@example.com", password="User123!", username="user")

    def test_assign_role_to_user(self):
        print("🔍 Testing assigning a role to a user...")

        # Create a new user
        new_user = User.objects.create_user(email="newuser@example.com", password="User123!", username="newuser")

        # Test assigning a role
        self.client.force_authenticate(user=self.admin_user)  # Authenticate as Admin
        url = reverse('userrole-list')
        data = {"user": new_user.id, "role": self.moderator_role.id}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertTrue(UserRole.objects.filter(user=new_user, role=self.moderator_role).exists())
        print("✅ Role assignment passed.")

    def test_assign_role_no_permission(self):
        print("🔍 Testing role assignment without proper permission...")

        # Authenticate as a regular user
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('userrole-list')
        data = {"user": self.regular_user.id, "role": self.admin_role.id}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        print("✅ Unauthorized role assignment test passed.")

    def test_assign_invalid_role(self):
        print("🔍 Testing assigning a non-existent role...")

        # Authenticate as Admin
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('userrole-list')
        invalid_data = {"user": self.regular_user.id, "role": 9999}  # Non-existent role ID

        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        print("✅ Invalid role assignment test passed.")

    def test_assign_role_to_nonexistent_user(self):
        print("🔍 Testing assigning a role to a non-existent user...")

        # Authenticate as Admin
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('userrole-list')
        invalid_data = {"user": 9999, "role": self.moderator_role.id}  # Non-existent user ID

        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        print("✅ Invalid user assignment test passed.")

    def test_remove_role_from_user(self):
        print("🔍 Testing removing a role from a user...")

        # Assign a role first
        UserRole.objects.create(user=self.regular_user, role=self.moderator_role)

        # Test role removal
        self.client.force_authenticate(user=self.admin_user)
        user_role = UserRole.objects.get(user=self.regular_user, role=self.moderator_role)
        url = reverse('userrole-detail', args=[user_role.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertFalse(UserRole.objects.filter(user=self.regular_user, role=self.moderator_role).exists())
        print("✅ Role removal test passed.")

    def test_create_role(self):
        print("🔍 Testing creating a new role...")

        # Authenticate as Admin
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('role-list')
        data = {"name": "Test Role", "description": "A role for testing."}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        print("✅ Role creation test passed.")

    def test_create_role_no_permission(self):
        print("🔍 Testing creating a role without permission...")

        # Authenticate as a regular user
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('role-list')
        data = {"name": "Unauthorized Role", "description": "Should not be created."}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        print("✅ Unauthorized role creation test passed.")

    def test_view_roles(self):
        print("🔍 Testing viewing roles...")

        # Authenticate as Admin
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('role-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertGreaterEqual(len(response.data), 1)  # At least one role should exist
        print("✅ Role view test passed.")

    def test_view_roles_no_permission(self):
        print("🔍 Testing viewing roles without permission...")

        # Authenticate as a regular user
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('role-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        print("✅ Unauthorized role view test passed.")
