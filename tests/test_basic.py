from flask import session

# tests/test_basic.py

# Dictionary with user data for testing
data_object = {
    "first_name": "testeur",
    "last_name": "testeur lastname",
    "email": "testeur@example.com",
    "username": "testuser",
    "password": "testpassword"
}

# Tests to check if the application is running and the main page is accessible.
def test_login_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<h1 class=\"h3 mb-1\">Ma To-do</h1>" in response.data


# Tests to check if the register page is accessible.
def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"<h1 class=\"h4 mb-1\">S'enregistrer</h1>" in response.data

# Tests to check if the connection page is accessible.
def test_connection_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"<h1 class=\"h4 mb-1\">Se connecter</h1>" in response.data

# Tests to check if the dashboard page is accessible without login 
# (should redirect to login).
def test_dashboard_page_get(client):
    response = client.get("/dashboard")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")

# Test to check if a new user can be added.
def test_add_user(client):
    response = client.post("/new-user", data=data_object, 
                           follow_redirects=True)

    assert response.status_code == 200
    assert b"<p class=\"mb-0 text-white-75\">Vous pouvez maintenant" 
    b" vous connecter.</p>" in response.data
    
# Test to check if a user can log in with valid credentials.
def test_login_user(client):
    # First, create a new user
    client.post("/new-user", data=data_object, follow_redirects=True)
    
    response_fail = client.post("/connection", data={
        "username": "testuser",
        "password": "wrongpassword"
    }, follow_redirects=True)

    # Then, try to log in
    response = client.post("/connection", data={
        "username": "testuser",
        "password": "testpassword"
    }, follow_redirects=True)

    assert b"<h1 class=\"h4 mb-1\">Se connecter</h1>" in response_fail.data
    assert response.status_code == 200
    assert b"<p class=\"mb-0 text-white-75\">Bienvenue" 
    b"testuser!</p>" in response.data
    
def test_modify_session(client):
    with client.session_transaction() as sess:
        sess['id_user'] = 1

    response = client.get("/dashboard")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")
    assert b"<p class=\"mb-0 text-white-75\">Bienvenue" 
    b"testuser!</p>" in response.data