import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_expense(client):
    response = client.post('/expenses', json={
        'title': 'Coffee',
        'amount': 50,
        'category': 'Food'
    })
    assert response.status_code == 201

def test_get_expenses(client):
    response = client.get('/expenses')
    assert response.status_code == 200

def test_fail_demo():
    assert 1 == 2

