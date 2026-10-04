def signup(client, email):
    r = client.post("/api/auth/signup", json={"name": "Test", "email": email, "password": "secret12"})
    assert r.status_code == 201
    return r.json()


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_signup_login_roles(client):
    assert signup(client, "user@test.com")["user"]["role"] == "User"
    assert signup(client, "admin@test.com")["user"]["role"] == "Admin"
    ok = client.post("/api/auth/login", json={"email": "user@test.com", "password": "secret12"})
    assert ok.status_code == 200
    bad = client.post("/api/auth/login", json={"email": "user@test.com", "password": "wrongpass"})
    assert bad.status_code == 401


def test_policies_require_auth(client):
    assert client.get("/api/policies").status_code == 401


def test_upload_is_admin_only(client):
    token = signup(client, "u2@test.com")["access_token"]
    r = client.post("/api/policies/upload", headers=auth(token),
                    files={"file": ("p.pdf", b"%PDF-1.4", "application/pdf")})
    assert r.status_code == 403


def test_chat_ask_and_history(client, monkeypatch):
    from app.services import chatbot_service
    monkeypatch.setattr(chatbot_service, "answer",
                        lambda q: {"found": False, "answer": chatbot_service.NOT_FOUND, "sources": []})
    token = signup(client, "u3@test.com")["access_token"]
    r = client.post("/api/chat/ask", headers=auth(token), json={"question": "How many leave days?"})
    assert r.status_code == 200
    assert [m["role"] for m in r.json()["messages"]] == ["user", "assistant"]
    assert len(client.get("/api/chat", headers=auth(token)).json()) == 1
