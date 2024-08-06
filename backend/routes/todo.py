
from fastapi import APIRouter,HTTPException
from models.todo import Todo
from crud.todo import (fetch_all_todos,fetch_one_todo,create_todo,update_todo,delete_todo)
router = APIRouter()


@router.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@router.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_title(title: str):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with title {title}")

@router.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo)
    if response:
        return response
    raise HTTPException(400, "Bad request")

@router.put("/api/todo/{title}", response_model=Todo)
async def update_todo_endpoint(title: str, description: str):
    response = await update_todo(title, description)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with title {title}")

@router.delete("/api/todo/{title}")
async def delete_todo_endpoint(title: str):
    response = await delete_todo(title)
    if response:
        return {"message": "Todo deleted successfully"}
    raise HTTPException(404, f"There is no todo with title {title}")
