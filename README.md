# Social Media App API using FastAPI

## API endpoints/routes

- [Collection of API Testings in Insomnia json file](assets/api-test-insomnia-collection-v1.json)

![API Endpoints/Routes](assets/api-routes.png)

## Pydantic Schemas

![API Pydantic Schemas](assets/api-schemas.png)

## Tech stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic

## TO DO Features

- [x] CRUD Operations
- [ ] Authentication
- [ ] Validation
- [ ] Documentation
- [ ] Testing
- [ ] Deployment on Cloud VPS or Hosting
- [ ] Conteinerize with Docker
- [ ] Configure Nginx and Uvicorn ASGI
- [ ] GitHub action CI/CD

## How to run locally

- create venv and install dependencies in requirements.txt or use poetry
- run fastapi uvicorn server: `uvicorn app.main:app`
- run it in automatic reload mode when you change code with reload flag: `uvicorn app.main:app --reload`
- also you can specify port by: `--port 5000` by default: is `8000`

---

- How to stop background uvicorn server in windows (powershell) if any error or is still running in background:
- <kbd>CTRL + C</kbd> to quit.
- `netstat -ano | findstr :8080`
- `Stop-Process -id <PID>` or `kill <PID>`
