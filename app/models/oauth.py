from app import db
from app.models.base import BaseModel
import uuid

class OAuthProvider(BaseModel):
    __tablename__ = 'oauth_providers'
    
    provider_id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(50), unique=True, nullable=False)
    client_id = db.Column(db.String(255), nullable=False)
    client_secret_encrypted = db.Column(db.Text, nullable=False)
    authorization_url = db.Column(db.Text, nullable=False)
    token_url = db.Column(db.Text, nullable=False)
    scopes = db.Column(db.JSON, default=list)
    is_active = db.Column(db.Boolean, default=True)
    
    # ADD RELATIONSHIPS
    user_accounts = db.relationship('UserOAuthAccount', back_populates='provider')
    
    def __repr__(self):
        return f'<OAuthProvider {self.provider_name}>'

class UserOAuthAccount(BaseModel):
    __tablename__ = 'user_oauth_accounts'
    
    account_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('oauth_providers.provider_id'), nullable=False)
    provider_user_id = db.Column(db.String(255), nullable=False)
    access_token_encrypted = db.Column(db.Text)
    refresh_token_encrypted = db.Column(db.Text)
    token_expires_at = db.Column(db.DateTime)
    provider_data = db.Column(db.JSON, default=dict)
    
    # ADD RELATIONSHIPS
    user = db.relationship('User', back_populates='oauth_accounts')
    provider = db.relationship('OAuthProvider', back_populates='user_accounts')
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('provider_id', 'provider_user_id', name='uq_provider_user'),
        db.Index('idx_oauth_user_provider', 'user_id', 'provider_id'),
    )
    
    def __repr__(self):
        return f'<UserOAuthAccount {self.user_id}>'