from app import db
from app.models.base import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from enum import Enum

class UserStatus(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    SUSPENDED = 'suspended'
    PENDING = 'pending'

class User(UserMixin, BaseModel):
    __tablename__ = 'users'
    
    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    password_hash = db.Column(db.String(255))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    
    # FIXED RELATIONSHIPS with explicit foreign_keys
    # roles = db.relationship(
    #     'Role',
    #     secondary='user_roles',
    #     primaryjoin='User.user_id == UserRole.user_id',
    #     secondaryjoin='Role.role_id == UserRole.role_id',
    #     back_populates='users'
    # )
    # In the User class, replace the complex relationship with:
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')
    
    oauth_accounts = db.relationship('UserOAuthAccount', back_populates='user', cascade='all, delete-orphan')
    athlete_profile = db.relationship('AthleteProfile', back_populates='user', uselist=False)
    
    # Indexes
    __table_args__ = (
        db.Index('idx_users_email_status', 'email', 'status'),
        db.Index('idx_users_username_status', 'username', 'status'),
    )
    
    def get_id(self):
        """Required by Flask-Login."""
        return self.user_id
    
    def set_password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role_name):
        """Check if user has a specific role."""
        return any(role.name == role_name for role in self.roles)
    
    def is_active(self):
        """Check if user account is active."""
        return self.status == UserStatus.ACTIVE
    
    @property
    def full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<User {self.username}>'