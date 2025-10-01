# FAQ Finance Chatbot - Python Service

A Python microservice using FastAPI to answer frequently asked questions about finance.

## Features

- REST API with FastAPI
- Intelligent question matching using TF-IDF and cosine similarity
- Knowledge base with 15 finance Q&A pairs
- Detailed interaction logging
- Automated testing with pytest
- CORS configured for frontend integration

## Prerequisites

- Python 3.8+
- pip

## Installation

1. **Navigate to the service directory**
```bash
cd python-service
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

3. **
Install dependencies**
```bash
pip install -r requirements.txt
```

## Quick Start

### Development mode
```bash
python main.py
```

### With uvicorn
```bash
uvicorn main:app --reload --port 8001
```

The service will be available at `http://localhost:8001`

## API Documentation

### Available endpoints

#### `GET /` - Service information
```json
{
  "service": "FAQ Finance Chatbot",
  "status": "running",
  "endpoints": ["/chat"]
}
```

#### `POST /chat` - Ask the chatbot
**Request:**
```json
{
  "message": "What is EBITDA?"
}
```

**Response:**
```json
{
  "answer": "EBITDA (Earnings Before Interest, Taxes, Depreciation and Amortization) is an operational performance indicator...",
  "sources": ["faq#ebitda"]
}
```

#### `GET /health` - Health check
```json
{
  "status": "healthy",
  "faq_entries": 15
}
```

### Interactive documentation
Once the service is running, access the documentation at:
- `http://localhost:8001/docs` (Swagger UI)
- `http://localhost:8001/redoc` (ReDoc)

## Testing

### Run all tests
```bash
pytest test_main.py -v
```

### Test a specific question
```bash
curl -X POST "http://localhost:8001/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is EBITDA?"}'
```

## Knowledge Base

The `faq.json` file contains
 15 question-answer pairs covering:
- **Financial indicators**: EBITDA, EBIT, ROE, ROI, PER
- **Margins**: gross margin, net margin
- **Cash flow**: cash flow, free cash flow, working capital
- **Financial analysis**: net debt, liquidity ratio, CAPEX
- **Advanced concepts**: goodwill, breakeven point

## Matching Algorithm

The service uses:
1. **TF-IDF** (Term Frequency-Inverse Document Frequency) to vectorize questions
2. **Cosine similarity** to find the best match
3. **Confidence threshold** of 0.3 to avoid inappropriate responses

## Logging

Each interaction is logged with:
- Request timestamp
- User question
- System response
- Sources used
- Matching score for debugging

Example log output:
```
============================================================
[2024-01-15T10:30:45.123456]
Question: What is EBITDA?
Answer: EBITDA (Earnings Before Interest, Taxes, Depreciation and Amortization)...
Sources: faq#ebitda
============================================================
```

## Security

- CORS configured for `http://localhost:3000` (React frontend)
- Input validation with Pydantic
- Proper error handling with HTTP status codes

## Project Structure

```
python-service/
├── main.py           # Main FastAPI application
├── faq.json          # Knowledge base
├── requirements.txt  # Python dependencies
├── test_main.py      # Automated tests
└── README.md         # Documentation
```

## Configuration

### Environment variables (optional)
```bash
# Service port (default: 8001)
export PORT=8001

# Debug mode
export DEBUG=true
```

### Customizing matching threshold
In `main.py`, modify the `threshold` parameter in the `find_best_match()` function:
```python
def find_best_match(query: str, threshold: float = 0.3):
    # Increase for more precise answers
    # Decrease for more possible matches
```

## Troubleshooting

### Service won't start
- Verify virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`

### No response to a question
- Similarity score might be too low (< 0.3)
- Try rephrasing with keywords from `faq.json`
- Check logs for matching score

### CORS errors
- Verify frontend runs on `http://localhost:3000`
- Update `allow_origins` in `main.py` if needed

## Production Deployment

```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --workers 4
```

## Potential Improvements

- Database persistence for logs
- API authentication
- Response caching
- Multi-language support
- Metrics and monitoring
- Admin API for FAQ management