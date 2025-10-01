# FAQ Finance Chatbot - Quick Start Guide

## Overview

This Python microservice provides a REST API for answering finance-related questions using FastAPI. It implements intelligent question matching with TF-IDF vectorization and cosine similarity, backed by a curated knowledge base of 15 financial Q&A pairs.

## Quick Setup

```bash
# Navigate to service directory
cd python-service

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Start the service
python main.py
```

Service will be available at **http://localhost:8001**

## Testing

```bash
# Basic test
curl -X POST "http://localhost:8001/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is EBITDA?"}'

# Run automated tests
pytest test_main.py -v

# Use demo script
python example_usage.py
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service information |
| `/chat` | POST | Submit question to chatbot |
| `/health` | GET | Health check |
| `/docs` | GET | Swagger documentation |

## Request/Response Format

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

## Knowledge Base Coverage

The service can answer questions about:
- Financial indicators: EBITDA, EBIT, ROE, ROI, PER
- Margins: gross margin, net margin
- Cash flow: free cash flow, working capital
- Financial analysis: net debt, liquidity ratios, CAPEX
- Advanced concepts: goodwill, breakeven analysis

## Architecture

- **Matching Engine**: TF-IDF vectorization with cosine similarity
- **Confidence Threshold**: 0.3 minimum score for responses
- **Logging**: Complete interaction tracking with timestamps
- **Validation**: Pydantic models for request/response validation
- **Testing**: Comprehensive test suite with 13+ test cases

## Example Supported Queries

- "What is EBITDA?"
- "How to calculate ROE?"
- "Net debt definition"
- "Free cash flow explanation"
- "Gross vs net margin"
- "Working capital meaning"

## Development Status

- REST API implementation: Complete
- Intelligent matching: Implemented with TF-IDF + cosine similarity
- Knowledge base: 15 finance Q&A pairs loaded
- Interaction logging: Detailed timestamp and response tracking
- Test coverage: 13 automated tests covering edge cases
- Frontend integration: CORS configured for localhost:3000
- Documentation: Auto-generated Swagger UI available
- Input validation: Robust error handling with Pydantic
- Production ready: Error handling and health checks implemented
