from django.core.management.base import BaseCommand
from accounts.models import User, Role, Permission, UserRole

class Command(BaseCommand):
    help = 'Set up initial data for testing'

    def handle(self, *args, **kwargs):
        # Create permissions
        manage_users_perm, _ = Permission.objects.get_or_create(name='Manage Users', codename='manage_users')
        manage_roles_perm, _ = Permission.objects.get_or_create(name='Manage Roles', codename='manage_roles')
        manage_user_roles_perm, _ = Permission.objects.get_or_create(name='Manage User Roles', codename='manage_user_roles')
        manage_permissions_perm, _ = Permission.objects.get_or_create(name='Manage Permissions', codename='manage_permissions')
        view_roles_perm, _ = Permission.objects.get_or_create(name='View Roles', codename='view_roles')

        # Create roles and assign permissions
        super_admin_role, _ = Role.objects.get_or_create(name='Super Admin')
        super_admin_role.permissions.set([manage_users_perm, manage_roles_perm, manage_user_roles_perm, manage_permissions_perm])

        admin_role, _ = Role.objects.get_or_create(name='Admin')
        admin_role.permissions.set([manage_users_perm, view_roles_perm])

        moderator_role, _ = Role.objects.get_or_create(name='Moderator')
        moderator_role.permissions.set([view_roles_perm])

        # Create users
        super_admin_user, _ = User.objects.get_or_create(
            email='superadmin@example.com',
            defaults={
                'username': 'superadmin',
                'password': 'SuperAdmin123!',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user, _ = User.objects.get_or_create(
            email='admin@example.com',
            defaults={'username': 'admin', 'password': 'Admin123!'}
        )
        moderator_user, _ = User.objects.get_or_create(
            email='moderator@example.com',
            defaults={'username': 'moderator', 'password': 'Moderator123!'}
        )
        regular_user, _ = User.objects.get_or_create(
            email='user@example.com',
            defaults={'username': 'user', 'password': 'User123!'}
        )

        # Assign roles to users
        UserRole.objects.get_or_create(user=super_admin_user, role=super_admin_role)
        UserRole.objects.get_or_create(user=admin_user, role=admin_role)
        UserRole.objects.get_or_create(user=moderator_user, role=moderator_role)

        self.stdout.write(self.style.SUCCESS('Test data setup completed.'))
