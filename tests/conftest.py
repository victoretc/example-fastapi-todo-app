from clients.http.todo import TodosApi
from clients.http.todo.models.api_models import TodoCreate
from utils.httpx_client import Client, Configuration
import pytest
from faker import Faker
from httpx import Response
from typing import Generator


@pytest.fixture(scope="session")
def client() -> Client:
    return Client(Configuration(base_url="http://127.0.0.1:8000/proxy"))


@pytest.fixture(scope="session")
def todo_client(client) -> TodosApi:
    return TodosApi(client)


@pytest.fixture(scope="function", autouse=True)
def delete_all_todos(todo_client: TodosApi):
    todo_client.delete_todos()
    yield


@pytest.fixture
def task(todo_client: TodosApi, faker: Faker) -> Generator[Response, None, None]:
    got = todo_client.post_todos(
        TodoCreate(title=faker.name(), description=faker.text())
    )
    yield got
