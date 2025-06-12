from dataclasses import dataclass

from litestar import Litestar, get, post, put
from litestar.exceptions import HTTPException


@dataclass
class Todo:
    title: str
    done: bool


# TODO: move to databasee
TODO_LIST: list[Todo] = [
    Todo(title="Start writing TODO list", done=True),
    Todo(title="???", done=False),
    Todo(title="Profit", done=False),
]


@get("/")
async def get_list(done: bool | None = None) -> list[Todo]:
    if done is None:
        return TODO_LIST
    return [todo for todo in TODO_LIST if todo.done == done]


@post("/")
async def add_todo(data: Todo) -> list[Todo]:
    TODO_LIST.append(data)
    return TODO_LIST


@get("/{name:str}")
async def greeter(name: str) -> str:
    return f"Hello, {name}!"


@put("/{title:str}")
async def update_todo(title: str, data: Todo) -> list[Todo]:
    for todo in TODO_LIST:
        if todo.title == title:
            todo.title = data.title
            todo.done = data.done
            return TODO_LIST

    if title == "trycatch":
        return "CATCH!"

    raise HTTPException(status_code=404, detail=f"Todo '{title}' not found")


app = Litestar([get_list, add_todo, greeter, update_todo])
