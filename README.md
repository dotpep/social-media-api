# Social Media App API using FastAPI

## Documentation

- [Collection of API Testing Endpoints in Insomnia json file that can be imported any API test tool like Postman](/docs/README.md)

### FastAPI endpoints/routes

![API Endpoints/Routes](assets/api-routes.png)

### Pydantic Schemas

![API Pydantic Schemas](assets/api-schemas.png)

## Tech stack

- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy
- Alembic

## TO DO Features

- [x] CRUD Operations
- [x] Authentication
- [ ] Validation
- [ ] Documentation
- [ ] Testing
- [ ] Deployment on Cloud VPS or Hosting
- [ ] Conteinerize with Docker
- [ ] Configure Nginx and Uvicorn ASGI
- [ ] GitHub action CI/CD

## How to run locally

### Running uvicorn server

- Create venv and install dependencies in requirements.txt or use poetry
- Run fastapi uvicorn server: `uvicorn app.main:app`
- Run it in automatic reload mode when you change code with reload flag: `uvicorn app.main:app --reload`
- Also you can specify port by: `--port 5000` by default: is `8000`

---

- How to stop background uvicorn server in windows (powershell) if any error or is still running in background:
- <kbd>CTRL + C</kbd> to quit.
- `netstat -ano | findstr :8080`
- `Stop-Process -id <PID>` or `kill <PID>`

---

- Also, you need provide Postgres db data like db_name, user_name, password etc.
- In below instruction section:

### Setting up Environment variables files (In Development)

> In Production, you must set this environment variables in Your machine/server as Permanent System-wide Environment Variables, in Development you can just use `.env` file

- Change this file in base dir of project with your required config variables: `.env.example`
- After setting your env variables data rename this `.env.example` file to `.env.`
- Provide values to empty variable values (create postgres database)

---
Postgres Database env variables

```.env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_USERNAME=postgres
```

---
JWT Token env variables

- You can use just my setting for JWT token or use own
- to generate SECRET_KEY you can use this command `openssl rand -hex 32`

```.env
SECRET_KEY=9b68c9f53ff13f75b890b62af1d9435d65827796d21ceb16c5fe431f054dcde3
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

- If somthings doesn't work try to delete `# Comment` in `.env` file I think this may help
