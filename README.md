## Local Development

1. Create and activate virtual environment:
```bash
python -m venv venv source venv/bin/activate
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

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment to GCP

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
