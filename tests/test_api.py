import json
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
from app import create_app, db
from app.models import User, AthleteProfile

@pytest.fixture
def app_instance():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()


def test_get_athlete(client):
    user = User(username='u1', email='u1@example.com', first_name='U', last_name='One')
    user.save()
    athlete = AthleteProfile(user_id=user.user_id, date_of_birth=date.fromisoformat('2000-01-01'))
    athlete.save()

    resp = client.get(f'/api/athletes/{athlete.athlete_id}')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['athlete_id'] == athlete.athlete_id
    assert data['user']['full_name'] == user.full_name


def test_create_athlete_missing_field(client):
    resp = client.post('/api/athletes', json={})
    assert resp.status_code == 400
    data = json.loads(resp.data)
    assert 'error' in data or 'message' in data


def test_404_returns_json(client):
    resp = client.get('/api/athletes/nonexistent')
    assert resp.status_code == 404
    data = json.loads(resp.data)
    assert 'error' in data or 'message' in data
