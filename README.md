# Chat-Art - Technical Test Implementation
> Fullstack React + Python Finance FAQ Chatbot

A complete fullstack application featuring a Next.js frontend for articles management with an integrated Python FastAPI chatbot service for finance-related queries.

## Project Structure

```
taram/
├── artit/                    # Next.js Frontend Application
│   ├── app/                  # Next.js App Router (pages & API routes)
│   ├── components/           # React components (articles, chat)
│   ├── prisma/              # Database schema & seed data
│   └── README.md            # Detailed frontend documentation
└── python-service/          # Python FastAPI Chatbot Service
    ├── app/                 # FastAPI application modules
    ├── data/                # FAQ knowledge base
    └── README.md            # Detailed service documentation
```

## Quick Start

### Prerequisites
- **Node.js** 18+ and npm/yarn/pnpm
- **Python** 3.8+ and pip
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd taram
```

### 2. Setup Next.js Frontend
```bash
cd artit
npm install

# Database setup
npm run db:generate
npm run db:push
npm run db:seed

# Environment configuration
cp .env.local.example .env.local
# Edit .env.local with your configuration

# Start development server
npm run dev
```

The frontend will be available at: **http://localhost:3000**

### 3. Setup Python Service
```bash
cd ../python-service

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start the service
python main.py
# or: uvicorn main:app --reload --port 8001
```

The Python service will be available at: **http://localhost:8001**

### 4. Access the Application
1. Open http://localhost:3000 in your browser
2. Navigate to `/articles` to see the articles list with search and sort functionality
3. Use the chat widget on the articles page to interact with the finance FAQ bot

## Features Implemented

### Frontend (Next.js)
- **Articles Management**: Display, search, and sort articles by date
- **Full-text Search**: Real-time search through titles and summaries
- **Date Sorting**: Newest first (default), with option to reverse
- **State Management**: Loading states, empty states, error handling
- **API Routes**: RESTful `/api/articles` endpoint with query parameters
- **Database**: SQLite with Prisma ORM, seeded with 20 sample articles
- **Validation**: Zod schemas for input validation
- **Environment**: `.env.local` configuration

### Python Service
- **FastAPI Service**: RESTful `/chat` endpoint
- **Finance FAQ Bot**: 15 finance-related Q&A pairs
- **Smart Matching**: TF-IDF + cosine similarity algorithm
- **Knowledge Base**: JSON-based FAQ data structure
- **Logging**: Detailed interaction logs with timestamps
- **CORS**: Configured for frontend integration

### Integration
- **Chat Widget**: Integrated chat interface on articles page
- **Real-time Communication**: Frontend ↔ API Route ↔ Python Service
- **Error Handling**: Graceful fallbacks when services are unavailable
- **TypeScript**: Full type safety throughout the application

## Technical Choices

### Frontend Stack
- **Next.js 15** with App Router for modern React development
- **React 19** for latest features and improved performance
- **TypeScript** for type safety and better developer experience
- **Tailwind CSS** for utility-first styling
- **Prisma + SQLite** for simple, efficient data persistence
- **Zod** for runtime validation
- **Biome** for consistent code formatting and linting
- **Vitest** for fast, modern testing

### Backend Stack
- **FastAPI** for high-performance async API development
- **Pydantic** for data validation and serialization
- **scikit-learn** for TF-IDF vectorization and similarity matching
- **SQLite/JSON** for lightweight data storage
- **pytest** for comprehensive testing

### Architecture Decisions
- **Microservices**: Separate concerns between React app and Python service
- **API Gateway Pattern**: Next.js API routes proxy requests to Python service
- **Client-Server Components**: Optimal use of React Server Components
- **Error Boundaries**: Robust error handling with graceful degradation
- **Environment-based Configuration**: Flexible deployment options

## API Endpoints

### Frontend API Routes
```
GET /api/articles?query=<search>&sort=<asc|desc>
POST /api/chat
```

### Python Service
```
GET  /              # Service information
GET  /health        # Health check
POST /chat          # Finance FAQ chatbot
GET  /docs          # Interactive API documentation
```

## Testing

### Frontend Tests
```bash
cd artit
npm run test        # Run tests in watch mode
npm run test:run    # Run tests once
```

### Python Service Tests
```bash
cd python-service
pytest test_main.py -v
```

## Environment Variables

### Frontend (.env.local)
```env
DATABASE_URL="file:./prisma/dev.db"
NEXT_PUBLIC_API_URL="http://localhost:3000"
PYTHON_SERVICE_URL="http://localhost:8001"
```

### Python Service (.env)
```env
PORT=8001
DEBUG=true
```

## Sample Data

### Articles
The database is seeded with 20 sample articles covering various finance topics with realistic titles, dates, and summaries.

### FAQ Knowledge Base
15 finance Q&A pairs covering:
- Financial indicators (EBITDA, EBIT, ROE, ROI, PER)
- Margins and profitability metrics
- Cash flow and liquidity concepts
- Advanced financial analysis topics

## Usage Examples

### Search Articles
```bash
curl "http://localhost:3000/api/articles?query=EBITDA&sort=desc"
```

### Chat with Finance Bot
```bash
curl -X POST "http://localhost:8001/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is EBITDA?"}'
```

## Development Scripts

### Frontend
```bash
npm run dev         # Development server
npm run build       # Production build
npm run lint        # Code linting
npm run format      # Code formatting
npm run db:studio   # Database management UI
```

### Python Service
```bash
python main.py      # Start development server
pytest             # Run tests
```

## Known Limitations & Future Improvements

### Current Limitations
- **Chat History**: Messages are not persisted between sessions
- **Authentication**: No user authentication system implemented
- **Caching**: No response caching for frequently asked questions
- **Monitoring**: Basic logging without advanced monitoring/metrics

### Potential Improvements
- Add user authentication and personalized chat history
- Implement Redis caching for improved performance
- Add comprehensive monitoring and analytics
- Extend FAQ knowledge base with more financial topics
- Add multi-language support
- Implement real-time chat with WebSocket connections
- Add admin interface for FAQ management

## Detailed Documentation

For comprehensive documentation of each component:

- **[Frontend Documentation](./artit/README.md)** - Next.js app setup, components, and API details
- **[Python Service Documentation](./python-service/README.md)** - FastAPI service, FAQ matching, and deployment
- **[Implementation Summary](./artit/IMPLEMENTATION_SUMMARY.md)** - Technical implementation details
