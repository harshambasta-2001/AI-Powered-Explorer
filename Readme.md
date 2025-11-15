# Welcome to the documentation

## Installation guide

Prerequisites: Python 3.12.3, MySQL server setup

1. Clone the repository

```
git clone <repository-url>
cd <repository-directory>
```

2. Make a virtual environment folder (named .venv or whatever preferred) and activate it using commands

For mac/linux:

```
python3 -m venv .venv
source .venv/bin/activate
```

For windows:

```
python -m venv .venv
.venv\Scripts\activate
```

2. Install Dependencies with pip:
   ```pip install -r requirements.txt```


3. Set up Alembic for database migrations

Initialize Alembic:
```
alembic init alembic
```

Generate a new migration automatically (based on your models):
```
alembic revision --autogenerate -m "initial migration"
```

Apply the migration to your database:
```
alembic upgrade head
```

4. Run your application

```
uvicorn main:app --reload
```

Api Document
```
http://127.0.0.1:8000/docs#/
```

5. Test your application
```
pytest
```