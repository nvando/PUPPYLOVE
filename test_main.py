import pytest
from main import app, valid_username

@pytest.fixture
def client():
    client = app.test_client()
    return client

def test_index(client):
    response = client.get('/')
    html = response.data.decode()

    assert response.status_code == 200
    assert "<h2>Who doesn't love puppies?</h2>" in html

def test_redirect(client):
    response = client.get("/home")
    assert response.status_code == 302
    assert response.location == '/'


def test_login(client):
    response = client.get('/login')
    html = response.data.decode()

    assert response.status_code == 200
    assert "<p>Please enter your email and password</p>" in html

def test_test_logout(client):
    pass


def test_signup(client):
    response = client.get('/signup')
    html = response.data.decode()

    assert response.status_code == 200
    assert "<p>Enter you email address, and create a username and password</p>" in html


def test_dashboard(client):
    response = client.get('/dashboard')

    assert response.status_code == 302
    assert response.location == '/'


def test_report(client):
    pass


def test_thankyou(client):
    pass
 
def valid_login(client):
    pass


def test_add_user(client):
    pass

def test_valid_username(client):
    
    pass


def test_valid_username():

    username1 = 'ThomasThank8'
    username2 = 'thomasthank8'
    username3 = 'THOMASTHANK8'
    username4 = 'ThomasThank'
    

    assert valid_username(username1) == (True, True, True)

    assert valid_username(username2) == (False, True, True)
    assert valid_username(username3) == (True, False, True)
    assert valid_username(username4) == (True, True, False)
    

    
