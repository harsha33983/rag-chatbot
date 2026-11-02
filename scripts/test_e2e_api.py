"""
End-to-End API Integration Test Suite for MindCare AI.
Tests live endpoints with FastAPI TestClient.
"""
import sys
import os
import uuid

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_e2e_flow():
    print("\n--- 1. Testing System Health & Root ---")
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["name"] == "MindCare AI"
    print("  [PASS] Root endpoint operational.")

    health_res = client.get("/api/health")
    assert health_res.status_code == 200
    assert health_res.json()["status"] == "healthy"
    print("  [PASS] Health check verified.")

    print("\n--- 2. Testing Authentication Endpoints ---")
    test_email = f"mindcare_test_{uuid.uuid4().hex[:6]}@example.com"
    reg_res = client.post("/api/auth/register", json={
        "name": "Maya Lin",
        "email": test_email,
        "password": "SecurePassword123!"
    })
    assert reg_res.status_code == 201, f"Registration failed: {reg_res.text}"
    token = reg_res.json()["access_token"]
    assert token is not None
    print("  [PASS] User registration succeeded.")

    login_res = client.post("/api/auth/login", json={
        "email": test_email,
        "password": "SecurePassword123!"
    })
    assert login_res.status_code == 200
    headers = {"Authorization": f"Bearer {token}"}
    print("  [PASS] User login succeeded.")

    me_res = client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == test_email
    print("  [PASS] GET /api/auth/me succeeded.")

    print("\n--- 3. Testing Sentiment Analysis Endpoint ---")
    sent_res = client.post("/api/sentiment/predict", headers=headers, json={
        "text": "My chest is tight and I can't catch my breath, I feel so panicked about the presentation tomorrow."
    })
    assert sent_res.status_code == 200, f"Sentiment endpoint failed: {sent_res.text}"
    sent_data = sent_res.json()
    assert sent_data["label"] in ["anxious", "fearful"]
    assert sent_data["confidence"] > 0.4
    assert "tone_strategy" in sent_data
    assert "tone_instruction" in sent_data
    print(f"  [PASS] 6-Class Sentiment classification: label='{sent_data['label']}' (conf={sent_data['confidence']:.2f}, tone='{sent_data['tone_strategy']}')")

    print("\n--- 4. Testing RAG Knowledge Status ---")
    status_res = client.get("/api/knowledge/status", headers=headers)
    assert status_res.status_code == 200
    assert status_res.json()["total_vectors"] >= 500
    print(f"  [PASS] Vector status verified: {status_res.json()['total_vectors']} chunks indexed across 500+ curated resources.")

    print("\n--- 5. Testing Chat & Grounded RAG Generation ---")
    chat_res = client.post("/api/chat", headers=headers, json={
        "message": "I feel anxious and overwhelmed. Can you guide me through a 5-4-3-2-1 grounding exercise?"
    })
    assert chat_res.status_code == 200, f"Chat failed: {chat_res.text}"
    chat_data = chat_res.json()
    assert chat_data["role"] == "assistant"
    assert chat_data["is_crisis"] is False
    assert chat_data["sources"] is not None
    assert len(chat_data["sources"]) > 0
    assert "sentiment" in chat_data and chat_data["sentiment"] is not None
    session_id = chat_data["session_id"]
    print(f"  [PASS] RAG response generated with {len(chat_data['sources'])} source citations.")
    print(f"  [PASS] Sentiment attached: {chat_data['sentiment']['label']} (Adapted Tone: {chat_data['sentiment']['tone_strategy']})")
    print(f"  [PASS] Top source: '{chat_data['sources'][0]['title']}' (Score: {chat_data['sources'][0]['score']})")

    print("\n--- 6. Testing Crisis Guardrail in Chat Endpoint ---")
    crisis_res = client.post("/api/chat", headers=headers, json={
        "session_id": session_id,
        "message": "I don't think I can go on living, I want to kill myself tonight"
    })
    assert crisis_res.status_code == 200
    crisis_data = crisis_res.json()
    assert crisis_data["is_crisis"] is True
    assert "112" in crisis_data["content"] or "14416" in crisis_data["content"]
    assert crisis_data["sources"] is None or len(crisis_data["sources"]) == 0
    print("  [PASS] Crisis guardrail triggered: LLM bypassed, emergency helplines returned directly.")

    print("\n--- 6. Testing Session History & Management ---")
    sessions_res = client.get("/api/chat/sessions", headers=headers)
    assert sessions_res.status_code == 200
    sessions = sessions_res.json()
    assert len(sessions) >= 1
    print(f"  [PASS] Listed {len(sessions)} active sessions.")

    # Get session details & messages
    session_detail = client.get(f"/api/chat/sessions/{session_id}", headers=headers)
    assert session_detail.status_code == 200
    messages = session_detail.json()["messages"]
    assert len(messages) >= 4  # 2 user messages + 2 assistant messages
    print(f"  [PASS] Retrieved session with {len(messages)} persistent SQL messages.")

    # Rename session
    patch_res = client.patch(f"/api/chat/sessions/{session_id}", headers=headers, json={
        "title": "Grounding & Safety Support"
    })
    assert patch_res.status_code == 200
    assert patch_res.json()["title"] == "Grounding & Safety Support"
    print("  [PASS] Session renamed successfully.")

    # Delete session
    del_res = client.delete(f"/api/chat/sessions/{session_id}", headers=headers)
    assert del_res.status_code == 200
    print("  [PASS] Session deleted successfully.")

    print("\n" + "=" * 60)
    print("ALL END-TO-END INTEGRATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_e2e_flow()

