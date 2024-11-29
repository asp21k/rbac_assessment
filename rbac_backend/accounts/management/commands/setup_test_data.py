from django.core.management.base import BaseCommand
from accounts.models import User, Role, Permission, UserRole

class Command(BaseCommand):
    help = 'Set up test data for development and testing'

    def handle(self, *args, **kwargs):
        # Create an admin user
        admin_user, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'username': 'admin',
                'password': 'AdminPass123!',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Admin user created.'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))

        # Create a permission
        permission, created = Permission.objects.get_or_create(
            name='Test Permission',
            codename='test_permission'
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Permission created.'))
        else:
            self.stdout.write(self.style.WARNING('Permission already exists.'))

        # Create a role and assign the permission
        role, created = Role.objects.get_or_create(name='Test Role')
        if created:
            role.permissions.add(permission)
            self.stdout.write(self.style.SUCCESS('Role created and permission assigned.'))
        else:
            self.stdout.write(self.style.WARNING('Role already exists.'))

        # Create a regular user
        user, created = User.objects.get_or_create(
            email='user@example.com',
            defaults={
                'username': 'user',
                'password': 'UserPass123!',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Regular user created.'))
        else:
            self.stdout.write(self.style.WARNING('Regular user already exists.'))

        # Assign the role to the user
        user_role, created = UserRole.objects.get_or_create(user=user, role=role)
        if created:
            self.stdout.write(self.style.SUCCESS('Role assigned to user.'))
        else:
            self.stdout.write(self.style.WARNING('User already has the role assigned.'))
