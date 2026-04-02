from flask import session;
import pytest

data_object_1 = {
    "first_name": "testeur1",
    "last_name": "testeur1 lastname",
    "email": "testeur@example.com",
    "username": "testuser1",
    "password": "testpassword1"
}

data_object_2 = {
    "first_name": "testeur2",
    "last_name": "testeur2 lastname",
    "email": "testeur2@example.com",
    "username": "testuser2",
    "password": "testpassword2"
}


# Test to check if a user can log in with valid credentials, 
# and cannot log in with invalid credentials.
@pytest.mark.parametrize("username, password,status_code, expected_message", [
    ("testuser1", "testpassword1", 200, b"Bienvenue testuser1!"),
    ("wronguser", "testpassword", 200, b"Se connecter"),
    ("testuser", "wrongpassword", 200, b"Se connecter"), 
])
def test_login_param(client, username, password, status_code,
                     expected_message):
    client.post("/new-user", data=data_object_1, follow_redirects=True)
    
    response = client.post("/connection", data={
        "username": username,
        "password": password
    }, follow_redirects=True)
    assert response.status_code == status_code
    assert expected_message in response.data
    
# Test to check if multiple users can be created and log in successfully.
@pytest.mark.parametrize(
    "user_data, login_data, expected_message",
    [
        (data_object_1, {"username": "testuser1", 
                         "password": "testpassword1"}, 
         b"Bienvenue testuser1!"),
        (data_object_2, {"username": "testuser2", 
                         "password": "testpassword2"}, 
         b"Bienvenue testuser2!"),
    ]
)
def test_multiple_users(client, user_data, login_data, expected_message):
    client.post("/new-user", data=user_data, follow_redirects=True)
    response = client.post("/connection", data=login_data, follow_redirects=True)

    assert expected_message in response.data
    

# Test to check if the session is created when a user logs in with 
# valid credentials.
@pytest.mark.parametrize(
    "username,password,expected_messages,session",
    [
        ("wronguser", "testpassword", b"Se connecter", False),
        ("testuser1", "testpassword1", b"Bienvenue testuser1!", True),
        ("testuser1", "wrongpassword", b"Se connecter", False)
        
    ])
def test_session_param(client, username, password, expected_messages,
                     session):
    client.post("/new-user", data=data_object_1, follow_redirects=True)
    
    response = client.post("/connection", data={
        "username": username,
        "password": password
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert expected_messages in response.data
    
    with client.session_transaction() as sess:
        if session:
            assert 'user_id' in sess
        else:
            assert 'user_id' not in sess
                         