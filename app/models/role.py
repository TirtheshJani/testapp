from app import db
from app.models.base import BaseModel
import uuid

class Role(BaseModel):
    __tablename__ = 'roles'
    
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_system_role = db.Column(db.Boolean, default=False)
    
    # Simple many-to-many relationship
    users = db.relationship('User', secondary='user_roles', back_populates='roles')
    
    def __repr__(self):
        return f'<Role {self.name}>'

class UserRole(BaseModel):
    __tablename__ = 'user_roles'
    
    user_role_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id', ondelete='CASCADE'), nullable=False)
    # Remove assigned_by for now to avoid complexity
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('user_id', 'role_id', name='uq_user_role'),
    )
