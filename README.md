# deti4devs

## Frontend

### .env file example

```bash
VITE_API_URL = http://localhost:8000/
```

### How to run

1. Install dependencies
```bash
npm install
```

2. Run the project
```bash
npm run dev
```

## Backend

### .env file example

```bash
SECRET_KEY=<SECRET_KEY> # Generate a secret key with the command: openssl rand -hex 32
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### How to run

1. Create a virtual environment
```bash
python3 -m venv venv
```

2. Activate the virtual environment
```bash
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the project
```bash
fastapi dev app/main.py
```

## Docker 

To run the application is necessary to have a PostgreSQL database running. You can use the following command to run a PostgreSQL container:

```bash
docker compose up database -d
```