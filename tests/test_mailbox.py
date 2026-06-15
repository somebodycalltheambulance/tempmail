from app.config import settings


async def test_create_mailbox(client):
    response = await client.post("/mailboxes")
    
    assert response.status_code == 201
    
    data = response.json()
    #проверка что в ответе есть нужные поля
    assert "id" in data
    assert "address" in data
    assert "token" in data
    assert "expires_at" in data
    assert "is_extended" in data
    
    assert data["address"].endswith("@"+settings.mail_domain)
    assert data["is_extended"] is False
    assert data["token"]
    

async def test_list_messages_requires_token(client):
    response = await client.post("/mailboxes")
    
    mailbox_id = response.json()["id"]
    #запросить письма без токена - 401
    response = await client.get(f"/mailboxes/{mailbox_id}/messages")
    assert response.status_code == 401
    
    
async def test_authorization(client):
    response = await client.post("/mailboxes")
    
    mailbox_id = response.json()["id"]
    headers = {"Authorization": "Bearer wrongtoken"}
    response = await client.get(f"/mailboxes/{mailbox_id}/messages", headers=headers)
    assert response.status_code == 401
    
    
async def test_list_messages_with_token(client):
    response = await client.post("/mailboxes")
    data = response.json()
    mailbox_id = data["id"]
    token = data["token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get(f"/mailboxes/{mailbox_id}/messages", headers=headers)
    assert response.status_code == 200
    assert response.json()["count"] == 0