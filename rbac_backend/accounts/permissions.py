from rest_framework import permissions

class HasRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Get required permissions from the view
        required_permissions = getattr(view, 'required_permissions', [])
        
        # If no required permissions are set, allow access (you can change this behavior if needed)
        if not required_permissions:
            return True

        # Get all roles assigned to the user
        user_roles = request.user.userrole_set.all().select_related('role')
        user_permissions = set()

        # Collect all permissions for the user based on their roles
        for user_role in user_roles:
            role_permissions = user_role.role.permissions.all()
            user_permissions.update(perm.codename for perm in role_permissions)

        # Check if any of the required permissions exist in the user's permissions
        return bool(user_permissions.intersection(required_permissions))
