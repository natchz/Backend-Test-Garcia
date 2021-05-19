def user_has_permissions(user, required_permissions, user_permissions=None):
    """
    Confirm if the user has a list of required permissions
    """

    if user.is_superuser:
        return True

    """
    Check the user's permissions in case they have not been passed to
    the function
    """
    if user_permissions is None:
        user_permissions = user.get_all_permissions()

    for perm in required_permissions:
        if perm not in user_permissions:
            return False

    return True