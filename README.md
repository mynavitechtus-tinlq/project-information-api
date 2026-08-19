# SOURCE BASE FAST-API

## Source Structure

```bash
.
├── README.md                  # -> Here
├── app                        # Source root space
│   ├── api                    # Routes, API logic
│   ├── core                   # Shared config / depends / constants / db
│   ├── models                 # Model folder
│   ├── exceptions
│   ├── helpers
│   ├── main.py
│   ├── middlewares            # Middleware folder
│   ├── services               # Services folder
│   ├── repositories           # Repository folder
│   ├── schemas
├── docker
│   ├── nginx                  # Nginx config folder
│   ├── Dockerfile_fastapi     # Dockerfile for fastapi, using for local only
│   ├── Dockerfile_nginx       # Dockerfile for nginx, using for local only
├── docker-compose.yaml        # Running it for build local
├── Dockerfile                 # Dockerfile for dev/qa/stg/prod
├── requirements.txt           # library python
├── tests
│   └── unit                   # Unit tests (no database)
```

## Requirement

Python == 3.13
Postgres == 17.9 (Docker image)
MinIO (S3 compatible, local)
Mailpit (SMTP sandbox, local)
fastapi
Docker

## Build step

### Create virtual environments for python

```bash
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Install package

```bash
pip install -r requirements.txt
```

### Run source

```bash
cp .env.example .env

# Build compose
docker-compose build --no-cache

# Up compose
docker-compose up

# Up and build compose
docker-compose up --build
```

After startup:

- API: `http://localhost:8000`
- Nginx: `http://localhost:80`
- MinIO API: `http://localhost:9000`
- MinIO Console: `http://localhost:9001`
- Mailpit SMTP: `localhost:1025`
- Mailpit UI: `http://localhost:8025`

### Init database

```bash

docker exec -it {compose_name}-api-1 bash

alembic upgrade head

```

### Create user by CLI

```bash
# Run from project root
python3 manage.py create-user --username "admin" --email "admin@example.com" --password "password"

# Create inactive user
python3 manage.py create-user --username "admin2" --email "admin2@example.com" --password "password" --inactive
```

### Auth APIs (basic)

Base path: `/api/v1/auth`

- `POST /login`
- `POST /refresh`
- `DELETE /logout`

Login request body (sign in with **email**):

```json
{
  "email": "admin@example.com",
  "password": "password"
}
```

Refresh request body:

```json
{
  "refresh_token": "<refresh_token>"
}
```

Logout:

- Use `Authorization: Bearer <access_token>` header.

Login/Refresh success payload includes:

- `access_token`
- `refresh_token`
- `token_type`
- `expires_at`
- `refresh_expires_at`

### How run unit test and make report

```bash

docker exec -it {compose_name}-api-1 bash

pytest --cov --cov-report=html:coverage_report tests/unit/ -vv

```

### Update model

Create or update model files in `app/models`.
When adding a new model, import it in `alembic/env.py` so Alembic can detect metadata.

```python
from app.models import Base, UserSessions, Users  # noqa: F401 — register models on Base.metadata
```

```bash

docker exec -it {compose_name}-api-1 bash

alembic revision --autogenerate -m "{message}"

```

Apply to the database

```bash

alembic upgrade head

```

If get error about `function uuid_generate_v4()`
Please add this to the version file in folder `alembic/versions/`

```python
# Above code

def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Initial database script

```

Revert to the latest version

```bash

## alembic downgrade {version}
## Example

alembic downgrade 78a44f91de69

```
# project-information-api
