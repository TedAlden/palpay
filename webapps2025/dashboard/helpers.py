def user_is_admin(user):
    """
    Check if the user is an admin.
    """
    return user.is_authenticated and user.is_superuser
