# example-fastapi-todo-app

## Setup

```bash
poetry install
```

## Run the app

```bash
poetry run uvicorn app:app --port=8081 --reload
```

Open http://127.0.0.1:8000/docs in your browser and ```curl -s http://127.0.0.1:8000/proxy/todos/```
