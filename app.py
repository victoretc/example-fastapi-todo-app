from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, StrictStr, StrictBool, StrictInt
from fastapi.responses import RedirectResponse

app = FastAPI(title="Simple Todo")


#############
#  schemas  #
#############


class Todo(BaseModel):
    id: StrictInt
    title: StrictStr
    description: StrictStr | None = None
    completed: StrictBool = False


class TodoCreate(BaseModel):
    title: StrictStr
    description: StrictStr | None = None


todos: dict[int, Todo] = {}


###############
#  endpoints  #
###############


router = APIRouter(prefix="/todos", tags=["todos"])


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@router.get("/", response_model=list[Todo])
async def get_todos() -> list[Todo]:
    return list(todos.values())


@router.delete("/", status_code=204, summary="Delete all todos")
async def delete_all_todos():
    todos.clear()


@router.post("/", response_model=Todo)
async def create_todo(todo: TodoCreate) -> Todo:
    new_id = len(todos) + 1
    new_todo = Todo(id=new_id, **todo.model_dump())
    todos[new_id] = new_todo
    return new_todo


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int) -> Todo:
    if todo_id in todos:
        return todos[todo_id]
    raise HTTPException(status_code=404, detail="Todo not found")


@router.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, updated_todo: TodoCreate) -> Todo:
    if todo_id in todos:
        new_todo = Todo(
            id=todo_id, **updated_todo.model_dump(), completed=todos[todo_id].completed
        )
        todos[todo_id] = new_todo
        return new_todo
    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int) -> dict[str, str]:
    if todo_id in todos:
        del todos[todo_id]
        return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")


@router.patch("/{todo_id}/complete", response_model=Todo)
async def complete_todo(todo_id: int) -> Todo:
    if todo_id in todos:
        todos[todo_id].completed = True
        return todos[todo_id]
    raise HTTPException(status_code=404, detail="Todo not found")


app.include_router(router)
