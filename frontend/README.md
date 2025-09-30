# Technical Test - Fullstack React + Python

This project implements a fullstack application featuring a Next.js frontend with an integrated Python chatbot service. The application provides articles management with search capabilities and a finance FAQ chatbot widget.

## Project Overview

The application consists of two main parts:
- A Next.js frontend with articles management and chat integration
- Integration points for a Python FastAPI service providing chatbot functionality

### Key Features

- Articles management with full-text search and date sorting
- Real-time search through article titles and summaries
- Finance FAQ chatbot widget integrated into the articles page
- Comprehensive error handling and loading states
- Responsive design optimized for both desktop and mobile
- SQLite database with Prisma ORM for data persistence

## Architecture

The frontend application uses Next.js 15 with the App Router and React 19. The chat functionality is implemented as a client-side component that communicates with a Python service through a Next.js API proxy route.

```
Frontend (Next.js) → API Route → Python Service (FastAPI)
                 ↓
            SQLite Database
```

## Technology Stack

- **Frontend**: Next.js 15, React 19, TypeScript
- **Styling**: Tailwind CSS
- **Database**: SQLite with Prisma ORM
- **Validation**: Zod schemas
- **Code Quality**: Biome for linting and formatting
- **Testing**: Vitest for unit tests

## Prerequisites

- Node.js 18 or higher
- A package manager (npm, yarn, or pnpm)
- Python 3.8+ (for the chatbot service)

## Installation and Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Database Setup

Generate the Prisma client and set up the database:

```bash
npm run db:generate
npm run db:push
npm run db:seed
```

### 3. Environment Configuration

Copy the environment template:

```bash
cp .env.local.example .env.local
```

Update the `.env.local` file with your configuration:

```env
DATABASE_URL="file:./dev.db"
NEXT_PUBLIC_API_URL="http://localhost:3000"
PYTHON_SERVICE_URL="http://localhost:8001"
```

### 4. Start Development Server

```bash
npm run dev
```

The application will be available at http://localhost:3000.

## Python Service Integration

The frontend is designed to work with a Python FastAPI service running on port 8001. The expected API contract is:

**Endpoint**: `POST /chat`

**Request Format**:
```json
{
  "message": "What is EBITDA?"
}
```

**Response Format**:
```json
{
  "answer": "EBITDA is an indicator of operational performance...",
  "sources": ["faq#ebitda"]
}
```

When the Python service is unavailable, the chat widget displays a fallback message instead of failing completely.

## Available Scripts

### Development
- `npm run dev` - Start development server with Turbopack
- `npm run build` - Build application for production
- `npm run start` - Start production server

### Database Management
- `npm run db:generate` - Generate Prisma client
- `npm run db:push` - Apply schema changes to database
- `npm run db:seed` - Populate database with sample data
- `npm run db:studio` - Open Prisma Studio for database management

### Code Quality
- `npm run lint` - Run Biome linter
- `npm run format` - Format code with Biome

### Testing
- `npm run test` - Run tests in watch mode
- `npm run test:run` - Run tests once
- `npm run test:watch` - Run tests in watch mode

## API Endpoints

### Articles
- `GET /api/articles` - Retrieve articles with optional filtering
  - Query parameters:
    - `query`: Search term for title/summary filtering
    - `sort`: Sort order (`asc` or `desc`, defaults to `desc`)

### Chat
- `POST /api/chat` - Proxy chat requests to Python service
  - Request body: `{ "message": "string" }`
  - Response: `{ "answer": "string", "sources": ["string"] }`

## Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── api/               # API routes
│   │   ├── articles/      # Articles CRUD operations
│   │   └── chat/          # Chat proxy to Python service
│   ├── articles/          # Articles page with chat integration
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Homepage
├── components/            # Reusable components
│   ├── articles/          # Article-related components
│   └── chat/              # Chat widget components
├── lib/                   # Utility functions and server logic
├── types/                 # TypeScript type definitions
├── tests/                 # Test files
├── data/                  # Sample data files
└── prisma/                # Database schema and migrations
```

## Chat Integration Details

The chat widget is implemented as a React component that appears as a sidebar on the articles page. It maintains conversation history during the session and handles various error states gracefully.

### Features
- Message history with user/bot differentiation
- Loading indicators during API calls
- Error handling with retry functionality
- Source attribution for bot responses
- Input validation and character limits
- Responsive design for mobile devices

### Error Handling
The chat system implements multiple layers of error handling:
- Network connectivity issues
- Python service unavailability
- Invalid user input
- JavaScript runtime errors

## Testing

The project includes comprehensive tests for both API endpoints and utility functions. Tests cover:
- API request/response validation
- Error scenarios and edge cases
- Input validation and sanitization
- Python service integration scenarios

Run tests with:
```bash
npm run test
```

## Development Notes

### Code Conventions
- All components are functional (no class components except error boundaries)
- Use absolute imports with the `@/` prefix
- Prefer async/await over Promise chains
- Maintain strict TypeScript typing throughout
- Follow conventional commit message format

### Performance Considerations
- Server Components are used by default for better performance
- Client components are used only when necessary (state, effects, browser APIs)
- Streaming and Suspense are implemented for progressive loading
- Code splitting happens automatically at the route level

## Troubleshooting

### Common Issues

**Database connection errors**: Ensure the database file exists and Prisma client is generated
```bash
npm run db:push
npm run db:generate
```

**Chat widget not responding**: Check if the Python service is running on port 8001 and the environment variables are configured correctly

**Build errors**: Clear the build cache and regenerate Prisma client
```bash
rm -rf .next
npm run db:generate
npm run build
```

**Test failures**: Ensure all dependencies are installed and environment variables are set for testing

## Deployment Considerations

### Production Environment
- Configure environment variables for your deployment platform
- Consider using PostgreSQL instead of SQLite for production
- Set up proper logging and monitoring
- Configure CORS settings for your domain

### Security
- All user inputs are validated with Zod schemas
- Environment variables are properly scoped (client vs server)
- API routes include proper error handling without information leakage

## Contributing

When contributing to this project:
1. Follow the established code patterns and conventions
2. Write tests for new functionality
3. Update documentation for any API changes
4. Use conventional commit messages
5. Ensure TypeScript compilation passes without errors

## Documentation

Additional documentation is available in the `docs/` directory:
- `CHAT_INTEGRATION.md` - Detailed chat integration guide
- Sample data files in `data/` directory
- Development helper scripts in `scripts/` directory

This project serves as a foundation for integrating React frontends with Python backend services, demonstrating modern web development practices and clean architecture patterns.