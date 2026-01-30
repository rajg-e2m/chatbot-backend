import requests
import uuid

base_url = "http://localhost:8000"

def test_chat():
    try:
        # 1. Health check
        resp = requests.get(f"{base_url}/health")
        print("Health Check:", resp.json())

        # 2. Init Chat
        thread_id = str(uuid.uuid4())
        print(f"Init Thread ID: {thread_id}")
        resp = requests.post(f"{base_url}/chat/init", json={"thread_id": thread_id})
        print("Chat Init:", resp.status_code, resp.text)
        
        # 3. Register (simulating the deterministic flow)
        resp = requests.post(f"{base_url}/chat/register", json={
            "name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890",
            "thread_id": thread_id
        })
        print("Register:", resp.status_code, resp.text)

        # 4. Chat Message
        resp = requests.post(f"{base_url}/chat", json={
            "message": "Hello, who are you?",
            "thread_id": thread_id
        })
        print("Chat Message:", resp.status_code, resp.text)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_chat()
