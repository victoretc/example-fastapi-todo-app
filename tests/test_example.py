from clients.http.todo.models.api_models import Todo, TodoCreate
from faker import Faker
from clients.http.todo import TodosApi


def test_get_todos(todo_client: TodosApi):
    got = todo_client.get_todos()
    assert len(got.model_dump()) == 0


def test_create_todo(
    todo_client: TodosApi,
    faker: Faker,
):
    expected_title = faker.name()
    expected_description = faker.text()

    response = todo_client.post_todos(
        TodoCreate(title=expected_title, description=expected_description)
    )
    assert response.title == expected_title
    assert response.description == expected_description
    assert response.id == 1
    assert response.completed is False


def test_get_todo_by_id(todo_client: TodosApi, task: Todo):
    got: Todo = todo_client.get_todos_todo_id(todo_id=task.id)
    assert got.id == task.id
    assert got.title == task.title
    assert got.description == task.description
    assert got.completed == task.completed


def test_update_todo(todo_client: TodosApi, task: Todo, faker: Faker):
    new_title = faker.name()
    new_description = faker.text()

    got = todo_client.put_todos_todo_id(
        todo_id=task.id,
        todo_create=TodoCreate(title=new_title, description=new_description),
    )

    assert got.title == new_title
    assert got.description == new_description
    assert got.id == task.id


def test_complete_todo(todo_client: TodosApi, task: Todo):
    got = todo_client.patch_todos_todo_id_complete(todo_id=task.id)
    assert got.completed is True


def test_delete_todo(todo_client: TodosApi, task: Todo):
    got = todo_client.delete_todos_todo_id_with_http_info(todo_id=task.id)
    assert got.json() == {"message": "Todo deleted successfully"}


def test_todo_not_found(todo_client: TodosApi):
    got = todo_client.get_todos_todo_id_with_http_info(todo_id=999)
    assert got.status_code == 404
    assert got.json() == {"detail": "Todo not found"}
