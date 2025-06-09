from typing import Any, Dict, Optional
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend

from gallery.auth.bcrypt import hash_password, verify_password
from gallery.db import UserDataAccess

def basic_auth_user_loader(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    User loader for Basic Authentication.
    Verifies the username and password against a user data store.
    """
    user_data = UserDataAccess().get_user_by_username(username)

    if user_data:
        # In a real app, securely verify the password hash
        if verify_password(password, user_data["password_hash"]):
            # Return a dictionary representing the authenticated user
            # This dictionary will be available in req.context.auth['user']
            return {
                "username": username,
                "full_name": user_data["full_name"],
                "roles": user_data["roles"],
            }
    return None # Return None if user not found or password invalid

# authentication middleware
auth_backend = BasicAuthBackend(basic_auth_user_loader)
auth_middleware = FalconAuthMiddleware(auth_backend,
                    exempt_routes=['/exempt'], exempt_methods=['HEAD'])