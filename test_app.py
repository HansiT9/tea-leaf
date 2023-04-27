import tempfile
import pytest
from flask import Response

from app import app, diceas_predict


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200


def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200


def test_chatbot_page(client):
    response = client.get('/chatbot')
    assert response.status_code == 200


def test_login_success(client):
    # send a POST request to the '/login-user' endpoint with valid username and password
    response = client.post('/login-user', data={'username': 'john', 'password': 'password'})

    # assert that the response status code is 200 (OK)
    assert response.status_code == 200


def test_login_sql_injection(client):
    # send a POST request to the '/login-user' endpoint with SQL injection attack
    response = client.post('/login-user', data={'username': "'; DROP TABLE user; --", 'password': 'password'})

    # assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # assert that the response does not contain the sensitive information (e.g. database table is dropped)
    assert b'Error occurred while login user' in response.data


def test_register_successful(client):
    response = client.post('/register-user', data={
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'testuser@example.com',
        'nic': '123456789V',
        'dob': '1990-01-01',
        'phonenumber': '0712345678',
        'address': '123 Main St'
    })
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data


def test_register_missing_field(client):
    response = client.post('/register-user', data={
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'testuser@example.com',
        'nic': '123456789V',
        'dob': '1990-01-01',
        'phonenumber': '0712345678'
        # 'address' field is missing
    })
    assert response.status_code == 200
    assert b"Error occurred while registering user" in response.data


def test_register_sql_injection(client):
    response = client.post('/register-user', data={
        'username': "'; DROP TABLE user; --",
        'password': 'testpassword',
        'email': 'testuser@example.com',
        'nic': '123456789V',
        'dob': '1990-01-01',
        'phonenumber': '0712345678',
        'address': '123 Main St'
    })
    assert response.status_code == 200
    assert b"Error occurred while registering user" in response.data


def test_successd_post(client):
    response = client.post('/contact', data=dict(firstname="John", email="john@example.com", subject="Hello"))
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data


def test_successd_empty_post(client):
    response = client.post('/contact', data=dict())
    assert b"Error occurred while saving contact information" in response.data


def test_successd_get(client):
    response = client.get('/contact')
    assert response.status_code == 500
    assert b"<!doctype html>" in response.data


def test_algal_spot():
    expected_output = ('gray_blight',
                         'result.html',
                         'Gray blight is a fungal disease that affects tea leaves and can cause '
                         'significant damage to tea plantations.',
                         'Fungicide Application: Fungicides can be used to control gray blight on tea '
                         'leaves. A copper-based fungicide or a fungicide containing mancozeb can be '
                         'effective in controlling the disease. Fungicides should be applied as per '
                         "the manufacturer's instructions, and the application should be timed to "
                         'coincide with the early stages of the disease. Repeat applications may be '
                         'necessary depending on the severity of the disease.',
                         'Pruning: Infected leaves and shoots should be pruned to prevent the spread '
                         'of the disease. Pruning should be done carefully, and the infected material '
                         'should be disposed of properly to avoid spreading the disease to other parts '
                         'of the plantation.',
                         'Cultural Practices: Good plant hygiene is essential to control gray blight '
                         'disease. It is important to maintain proper spacing between the tea bushes '
                         'and provide adequate air circulation to reduce humidity levels. Regular '
                         'removal of weeds and debris from the plantation can also help to control the '
                         'disease.',
                         'Soil Management: The fungus that causes gray blight can survive in the soil, '
                         'so soil management is important to prevent the disease from recurring. '
                         'Proper soil drainage, regular aeration, and soil amendment can help to keep '
                         'the soil healthy and prevent the disease from reoccurring.',
                         'Organic Control: Some organic methods can be used to control gray blight. '
                         'Garlic extract, neem oil, and baking soda are effective organic fungicides '
                         'that can be used to control the disease. Mix one tablespoon of garlic '
                         'extract or neem oil or baking soda in a gallon of water and spray it on the '
                         'tea bushes.\n',
                         'Gray blight is a fungal disease that affects tea plants, caused by the '
                         'fungus Pestalotiopsis theae. It typically appears as grayish spots on the '
                         'leaves and can cause defoliation, reducing the yield and quality of tea. ')

    result = diceas_predict('test_images/Algal_Leaf_Spot2205.jpg')
    assert result == expected_output
