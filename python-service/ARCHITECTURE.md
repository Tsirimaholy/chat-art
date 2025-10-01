# Architecture Overview - FAQ Finance Chatbot

## Overview

The FAQ Finance Chatbot is a Python microservice built with FastAPI that provides intelligent question-answering capabilities for finance-related queries. The service uses TF-IDF vectorization and cosine similarity to match user questions with a curated knowledge base.

## Project Structure

```
python-service/
├── app/                          # Main application package
│   ├── __init__.py              # Package metadata
│   ├── main.py                  # FastAPI application factory
│   ├── api/                     # API layer
│   │   ├── __init__.py
│   │   └── endpoints.py         # REST endpoint handlers
│   ├── core/                    # Core utilities
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration management
│   │   └── logging.py           # Logging utilities
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic request/response models
│   └── services/                # Business logic
│       ├── __init__.py
│       ├── faq_service.py       # FAQ matching engine
│       └── knowledge_base.py    # Knowledge base management
├── data/                        # Data files
│   └── faq.json                 # FAQ knowledge base
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_api.py             # API endpoint tests
│   └── test_services.py        # Service layer tests
├── main.py                      # Backward-compatible entry point
├── requirements.txt             # Python dependencies
├── start.sh                     # Startup script
├── example_usage.py             # Usage examples
├── README.md                    # Full documentation
├── QUICKSTART.md               # Quick setup guide
└── ARCHITECTURE.md             # This file
```

## Architecture Layers

### 1. API Layer (`app/api/`)

**Purpose**: HTTP request/response handling
- **endpoints.py**: REST API route handlers
- Handles request validation, response formatting
- Implements dependency injection for services
- Provides error handling and status codes

**Key Endpoints**:
- `POST /chat` - Main chatbot interaction
- `GET /health` - Service health check
- `GET /` - Service information
- `POST /search` - Multi-match search (advanced)
- `GET /stats` - Service statistics

### 2. Core Layer (`app/core/`)

**Purpose**: Cross-cutting concerns and utilities

**config.py**:
- Environment-based configuration management
- Pydantic settings with validation
- Default values and type safety
- Configuration for CORS, thresholds, file paths

**logging.py**:
- Structured logging setup
- Interaction logging for audit trail
- Debug logging for matching process
- Configurable log levels and formats

### 3. Models Layer (`app/models/`)

**Purpose**: Data validation and serialization

**schemas.py**:
- Pydantic models for request/response validation
- Type safety and automatic documentation
- Input sanitization and constraints
- JSON schema generation

**Key Models**:
- `ChatRequest` - User question input
- `ChatResponse` - Bot answer output
- `HealthResponse` - Health check response
- `ServiceInfoResponse` - Service metadata

### 4. Services Layer (`app/services/`)

**Purpose**: Business logic and core functionality

**knowledge_base.py**:
- FAQ data loading and validation
- File-based knowledge management
- Search and retrieval operations
- Data integrity checks
- Statistics and metadata

**faq_service.py**:
- TF-IDF vectorization engine
- Cosine similarity matching
- Threshold-based filtering
- Multi-match capabilities
- Performance optimization

## Data Flow

```
User Request → API Layer → Service Layer → Knowledge Base
     ↓              ↓            ↓              ↓
HTTP/JSON → Validation → TF-IDF → FAQ Data → Response
     ↑              ↑            ↑              ↑
User Response ← JSON Format ← Similarity ← Best Match
```

### Request Processing Flow

1. **HTTP Request**: User sends POST to `/chat` with question
2. **Validation**: Pydantic validates request format and content
3. **Service Injection**: FastAPI dependency system provides FAQ service
4. **Query Processing**: TF-IDF vectorization of user question
5. **Similarity Matching**: Cosine similarity against FAQ vectors
6. **Threshold Filtering**: Only matches above confidence threshold
7. **Response Generation**: Format answer with sources and metadata
8. **Logging**: Record interaction for audit and debugging
9. **HTTP Response**: JSON response back to user

## Machine Learning Components

### TF-IDF Vectorization

**Purpose**: Convert text questions into numerical vectors

**Configuration**:
- Lowercase normalization
- Unigram and bigram features (1-2 word phrases)
- No stop word removal (preserves financial terms)
- Max 5000 features for performance
- Vocabulary built from FAQ questions

### Cosine Similarity

**Purpose**: Measure similarity between user query and FAQ questions

**Process**:
1. Transform user query using fitted TF-IDF vectorizer
2. Calculate cosine similarity with all FAQ vectors
3. Find maximum similarity score and corresponding FAQ
4. Apply confidence threshold (default: 0.3)
5. Return best match or fallback response

## Configuration Management

### Environment Variables

All settings support environment variable overrides with `FAQ_` prefix:

- `FAQ_DEBUG=true` - Enable debug mode
- `FAQ_SIMILARITY_THRESHOLD=0.5` - Adjust matching sensitivity
- `FAQ_CORS_ORIGINS=["http://localhost:3000"]` - CORS settings
- `FAQ_FAQ_FILE=custom_faq.json` - Custom FAQ file

### Default Configuration

```python
# Core settings
service_name: "FAQ Finance Chatbot"
debug: False
similarity_threshold: 0.3

# Server settings
host: "0.0.0.0"
port: 8001

# File paths
data_dir: "data"
faq_file: "faq.json"
```

## Error Handling Strategy

### Validation Errors (422)
- Pydantic model validation failures
- Invalid request format or missing fields
- Automatic error details in response

### Business Logic Errors (400)
- Empty or whitespace-only messages
- Service-specific validation failures
- Custom error messages for user guidance

### Service Errors (500)
- Knowledge base loading failures
- TF-IDF initialization problems
- Unexpected processing errors
- Graceful degradation with fallback responses

### Health Check Errors (503)
- Service initialization failures
- Dependency unavailability
- System resource issues

## Performance Considerations

### Initialization Optimization
- FAQ data loaded once at startup
- TF-IDF vectors pre-computed
- Vocabulary cached in memory
- Service warm-up during application start

### Runtime Optimization
- Vectorized similarity calculations using NumPy
- Single-pass through FAQ vectors
- Minimal memory allocation per request
- Efficient numpy operations for large datasets

### Scalability Features
- Stateless design for horizontal scaling
- Configuration externalization
- Health checks for load balancer integration
- Structured logging for monitoring

## Security Considerations

### Input Validation
- Pydantic model validation for all inputs
- String length limits on messages
- UTF-8 encoding handling
- HTML/script injection prevention

### CORS Configuration
- Restricted to specific origins
- Configurable for different environments
- Credential handling options
- Method and header restrictions

### Error Information
- No sensitive data in error responses
- Generic error messages for production
- Detailed logging for debugging
- Stack trace filtering

## Testing Strategy

### Unit Tests
- Service layer components isolated
- Mock dependencies for focused testing
- Edge cases and error conditions
- Performance characteristics validation

### Integration Tests
- End-to-end API functionality
- Service interaction validation
- Real data processing verification
- Error handling workflows

### Test Coverage
- API endpoints: Full coverage of success/error paths
- Services: Business logic and edge cases
- Models: Validation scenarios
- Configuration: Environment variable handling

## Monitoring and Observability

### Logging Levels
- **INFO**: Service lifecycle events, successful operations
- **DEBUG**: Detailed matching scores, internal processing
- **WARNING**: Non-critical issues, fallback responses
- **ERROR**: Service failures, initialization problems

### Metrics Collection
- Request/response times
- Similarity score distributions
- FAQ match/no-match ratios
- Error rates by endpoint
- Service health status

### Health Checks
- Knowledge base loading status
- TF-IDF vectorizer initialization
- FAQ entry count validation
- Service response time checks

## Deployment Considerations

### Environment Requirements
- Python 3.8+
- FastAPI and dependencies
- Sufficient memory for TF-IDF vectors
- File system access for FAQ data

### Container Compatibility
- Stateless design suitable for containers
- Environment-based configuration
- Health check endpoint for orchestration
- Graceful shutdown handling

### Horizontal Scaling
- No shared state between instances
- Read-only data files
- Stateless request processing
- Load balancer compatible

## Future Enhancements

### Potential Improvements
- Database backend for FAQ management
- Machine learning model upgrades (BERT, embeddings)
- Caching layer for frequent queries
- Admin API for FAQ management
- Multi-language support
- Advanced analytics and reporting
- Authentication and rate limiting
- Automated FAQ updates from external sources

### Architectural Evolution
- Microservice decomposition
- Event-driven updates
- Real-time FAQ synchronization
- Advanced NLP preprocessing
- Feedback loop integration
- A/B testing framework