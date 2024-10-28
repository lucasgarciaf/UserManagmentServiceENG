import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:' # Use an in-memory database for testing


import pytest
from app import app
from database import SessionLocal, engine
from models import Base
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json



@pytest.fixture
def client():

    app.config['TESTING'] = True
    app.config['DEBUG'] = False

    # Setup
    with app.app_context():
        Base.metadata.create_all(bind=engine)

    test_client = app.test_client()

    yield test_client

    # Teardown
    with app.app_context():
        SessionLocal.close_all()
        Base.metadata.drop_all(engine)

def test_create_user(client):
    response = client.post('/api/users', json={
        'name': 'Test User',
        'birthdate': '2024-10-28'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Test User'
    assert data['active'] is True

def test_list_active_users(client):
    # Create a user
    client.post('/api/users', json={
        'name': 'Active User',
        'birthdate': '2020-05-15'
    })
    response = client.get('/api/users/active')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == 'Active User'

def test_update_user_state(client):
    # Create a user
    client.post('/api/users', json={
        'name': 'User to Deactivate',
        'birthdate': '1986-09-14'
    })
    # Update user state
    response = client.put('/api/users/1/state', json={'active': False})
    assert response.status_code == 204
    # Verify update
    response = client.get('/api/users/active')
    data = response.get_json()
    assert len(data) == 0

def test_delete_user(client):
    # Create a user
    client.post('/api/users', json={
        'name': 'User to Delete',
        'birthdate': '1944-10-02'
    })
    # Delete the user
    response = client.delete('/api/users/1')
    assert response.status_code == 204
    # Verify deletion
    response = client.get('/api/users/active')
    data = response.get_json()
    assert len(data) == 0
