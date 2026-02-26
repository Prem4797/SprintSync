# SprintSync 
A production-ready internal task management tool with AI-powered planning, built for the CodeStratLabs hiring challenge.

## Live Deployment
- **API Base URL:** https://sprintsync-api-gu5l.onrender.com/
- **Interactive API Docs:** https://sprintsync-api-gu5l.onrender.com/docs
- **System Metrics:** https://sprintsync-api-gu5l.onrender.com/metrics

## Walkthrough Video
- **Loom Link:** [INSERT_YOUR_LOOM_LINK_HERE]

## Architecture & Reasoning
This project follows a layered architecture to ensure maintainability and production resilience:
- **FastAPI & SQLModel:** Chosen for high performance and seamless integration with PostgreSQL.

- **Role-Based Access Control:** Implemented logic in `tasks.py` where Admins oversee the entire organization, while standard Users have strict data privacy for their own tasks.

- **AI Assist Layer:** Integrated Gemini 3 Flash to assist engineers in drafting professional task descriptions. Includes a deterministic "stub" mode to ensure reliable CI/CD and testing.

- **Observability:** Custom middleware captures request latency and structured logs (Loguru), while the Prometheus Instrumentator exposes real-time health metrics.

## Testing & Quality
- **Unit & Integration Tests:** 3/3 passing tests covering User Registration, JWT Authentication, and AI Stub integration.

- **Clean Code:** Standardized error handling and modular configuration using Pydantic-based settings.

## Local Setup & Execution
1. Clone the repository.
2. Create a `.env` file with `DATABASE_URL`, `SECRET_KEY`, and `GEMINI_API_KEY`.
3. Run via Docker Compose:
   ```bash
   docker-compose up --build
4. Execute test suite:
    ```bash
    docker exec -it sprintsync-app-1 pytest