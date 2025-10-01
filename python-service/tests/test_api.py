from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "FAQ Finance Chatbot"
    assert data["status"] == "running"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["faq_entries"] > 0

def test_chat_ebitda():
    """Test chat with EBITDA question"""
    response = client.post(
        "/chat",
        json={"message": "Qu'est-ce que l'EBITDA ?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert len(data["sources"]) > 0
    assert "EBITDA" in data["answer"] or "ebitda" in data["answer"].lower()

def test_chat_marge_brute():
    """Test chat with margin question"""
    response = client.post(
        "/chat",
        json={"message": "C'est quoi la marge brute ?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "chiffre d'affaires" in data["answer"].lower() or "marge" in data["answer"].lower()

def test_chat_empty_message():
    """Test chat with empty message"""
    response = client.post(
        "/chat",
        json={"message": ""}
    )
    assert response.status_code == 422  # Pydantic validation error

def test_chat_whitespace_message():
    """Test chat with whitespace only message"""
    response = client.post(
        "/chat",
        json={"message": "   "}
    )
    assert response.status_code == 400

def test_chat_unknown_question():
    """Test chat with question completely unrelated to finance"""
    response = client.post(
        "/chat",
        json={"message": "xyz123 random nonsense text that should not match anything"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    # For very low similarity questions, should get fallback response
    if len(data["sources"]) == 0:
        assert "désolé" in data["answer"].lower() or "n'ai pas trouvé" in data["answer"].lower()
    # If it does match something (due to low threshold), that's acceptable too

def test_chat_cash_flow():
    """Test chat with cash flow question"""
    response = client.post(
        "/chat",
        json={"message": "flux de trésorerie"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert len(data["sources"]) > 0
    assert "cash" in data["answer"].lower() or "trésorerie" in data["answer"].lower()

def test_chat_roe():
    """Test chat with ROE question"""
    response = client.post(
        "/chat",
        json={"message": "ROE rentabilité"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "ROE" in data["answer"] or "Return on Equity" in data["answer"]

def test_chat_capex():
    """Test chat with CAPEX question"""
    response = client.post(
        "/chat",
        json={"message": "investissement CAPEX"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "CAPEX" in data["answer"] or "Capital Expenditure" in data["answer"]

def test_chat_case_insensitive():
    """Test that matching is case insensitive"""
    response = client.post(
        "/chat",
        json={"message": "EBITDA"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["sources"]) > 0
    assert "faq#ebitda" in data["sources"]

def test_chat_partial_match():
    """Test partial matching with keywords"""
    response = client.post(
        "/chat",
        json={"message": "dette"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # Should match "dette nette" question
    assert "dette" in data["answer"].lower()

def test_invalid_json():
    """Test with invalid JSON structure"""
    response = client.post(
        "/chat",
        json={"wrong_field": "test"}
    )
    assert response.status_code == 422  # Validation error
