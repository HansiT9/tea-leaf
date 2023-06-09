import pytest

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


def test_login_valid_credentials(client):
    response = client.post('/login-user', data=dict(username='testuser', password='testpassword'))
    assert response.status_code == 200
    assert response.data == b'Successful'


def test_login_invalid_credentials(client):
    response = client.post('/login-user', data=dict(username='user1', password='password2'))
    assert response.status_code == 400
    assert response.data == b'Failed'


def test_login_empty_credentials(client):
    response = client.post('/login-user', data=dict(username='', password=''))
    assert response.status_code == 400
    assert response.data == b'Failed'


def test_login_invalid_method(client):
    response = client.get('/login-user')
    assert response.status_code == 500


def test_login_sql_injection(client):
    # send a POST request to the '/login-user' endpoint with SQL injection attack
    response = client.post('/login-user', data={'username': "'; DROP TABLE user; --", 'password': 'password'})

    # assert that the response status code is 500
    assert response.status_code == 500

    # assert that the response does not contain the sensitive information (e.g. database table is dropped)
    assert b'Failed' in response.data


def test_register_valid_data(client):
    data = {
        'username': 'user1',
        'password': 'password1',
        'email': 'user1@example.com',
        'nic': '123456789V',
        'dob': '1990-01-01',
        'phonenumber': '1234567890',
        'address': '123 Main St, Anytown USA'
    }
    response = client.post('/register-user', data=data)
    assert response.status_code == 200
    assert response.data == b'Successful'


def test_register_invalid_method(client):
    response = client.get('/register-user')
    assert response.status_code == 405


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
