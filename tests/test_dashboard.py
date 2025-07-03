import os
import sys
import uuid
from datetime import date, datetime, timedelta
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Role, AthleteProfile

@pytest.fixture
def app_instance():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        if not Role.query.filter_by(name='viewer').first():
            db.session.add(Role(name='viewer'))
            db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()


def _create_athlete(active=True, created_at=None):
    user = User(username=str(uuid.uuid4()), email=f'{uuid.uuid4()}@example.com', first_name='F', last_name='L')
    user.save()
    athlete = AthleteProfile(
        user_id=user.user_id,
        date_of_birth=date.fromisoformat('2000-01-01'),
        contract_active=active,
    )
    if created_at:
        athlete.created_at = created_at
    athlete.save()
    return athlete


def test_dashboard_active_contracts(client, app_instance):
    # create sample athletes
    _create_athlete(active=True)
    _create_athlete(active=True)
    _create_athlete(active=False)

    # create and login user
    with app_instance.app_context():
        user = User(username='dashuser', email='dash@example.com', first_name='Dash', last_name='User')
        user.set_password('secret')
        role = Role.query.filter_by(name='viewer').first()
        if role:
            user.roles.append(role)
        db.session.add(user)
        db.session.commit()

    client.post('/auth/login', data={'username_or_email': 'dashuser', 'password': 'secret'}, follow_redirects=True)
    with client.session_transaction() as sess:
        sess['auth_token'] = 'token'

    resp = client.get('/dashboard')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert 'Active Contracts' in html
    assert '>2<' in html


def test_dashboard_new_this_week(client, app_instance):
    with app_instance.app_context():
        _create_athlete(active=True, created_at=datetime.utcnow() - timedelta(days=8))
        _create_athlete(active=True, created_at=datetime.utcnow() - timedelta(days=1))
        _create_athlete(active=True, created_at=datetime.utcnow() - timedelta(days=2))

        user = User(username='newuser', email='new@example.com', first_name='New', last_name='User')
        user.set_password('secret')
        role = Role.query.filter_by(name='viewer').first()
        if role:
            user.roles.append(role)
        db.session.add(user)
        db.session.commit()

    client.post('/auth/login', data={'username_or_email': 'newuser', 'password': 'secret'}, follow_redirects=True)
    with client.session_transaction() as sess:
        sess['auth_token'] = 'token'

    resp = client.get('/dashboard')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert 'New This Week' in html
    assert '>2<' in html

