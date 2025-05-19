# User Management API

A RESTful API for user management built with FastAPI and deployed on Google Cloud Platform.

## Features

- Complete CRUD operations for user management
- Input validation and error handling
- Async database operations
- Comprehensive test suite
- GCP Cloud Run deployment ready

## Local Development

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

4. Run tests:
```bash
pytest tests/ -v
```

## API Documentation

Once the application is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment to GCP

### Prerequisites

1. Install and initialize [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Enable required APIs:
   - Cloud Run API
   - Cloud Build API
   - Container Registry API

### Deployment Steps

1. Set up Cloud Build trigger:
   - Go to Cloud Build > Triggers
   - Create new trigger
   - Connect to your repository
   - Select branch to build
   - Use the provided `cloudbuild.yaml`

2. Manual deployment:
```bash
gcloud builds submit --config cloudbuild.yaml
```

### Environment Variables

The following environment variables should be set in Cloud Run:
- `DATABASE_URL`: Your database connection string
- `ENVIRONMENT`: 'production'

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── database.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_users.py
├── requirements.txt
├── cloudbuild.yaml
├── pytest.ini
└── README.md
```
