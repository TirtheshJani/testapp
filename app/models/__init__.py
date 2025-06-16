# Import order is important to avoid circular imports
from .base import BaseModel
from .role import Role, UserRole
from .oauth import OAuthProvider, UserOAuthAccount
from .sports import Sport, Position
from .user import User
from .athlete import AthleteProfile

__all__ = [
    'BaseModel',
    'User', 'Role', 'UserRole', 
    'OAuthProvider', 'UserOAuthAccount',
    'AthleteProfile', 'Sport', 'Position'
]