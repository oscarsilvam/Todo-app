def test_login_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<h1 class=\"h3 mb-1\">Ma To-do</h1>" in response.data