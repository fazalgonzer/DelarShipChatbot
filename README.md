# SuperCar Virtual Sales Assistant - Backend Engineer Test

## Overview

This repository contains a test for backend engineers who will be working on AI-related systems. The test focuses on building a FastAPI backend that streams AI responses using Server-Sent Events (SSE) and implements tool calling functionality with Groq API. Your API will integrate with the provided frontend, which is a chat interface for Lex, a virtual sales assistant for SuperCar dealerships.

The test evaluates your ability to:
1. Implement Server-Sent Events (SSE) with FastAPI
2. Use Groq API for LLM tool calling with Llama 3.3 70B Versatile
3. Structure a maintainable backend API
4. Work with the provided frontend implementation



## Getting Started

### Development with Docker Compose (Recommended)

The easiest way to get started is using Docker Compose, which will set up both the backend and frontend environments for you:

1. Create a free Groq API account at https://console.groq.com/ and get your API key

2. Navigate to the `backend` directory and create a `.env` file with your Groq API key:
```bash
cd backend
cp .env.sample .env
# Edit the .env file to add your Groq API key
```

3. Run the development environment using Docker Compose:
```bash
cd ../infrastructure
docker-compose up
```

This will:
- Start the backend FastAPI service on http://localhost:8000
- Start the frontend Next.js application on http://localhost:3000
- Set up volume mounts so your code changes are reflected immediately

4. Open http://localhost:3000 in your browser to see the frontend
5. The backend includes a basic "hello world" implementation that you can use as a starting point. You'll need to modify `backend/main.py` to implement the full functionality.

### Setting Up Your Development Environment Manually

If you prefer to run without Docker, you can set up your environment directly:

1. Install the required dependencies:
```bash
pip install fastapi uvicorn sse-starlette pydantic python-dotenv groq
```

2. Create a free Groq API account at https://console.groq.com/ and get your API key

3. Create a `.env` file with your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the FastAPI application:
```bash
uvicorn backend.main:app --reload
```

