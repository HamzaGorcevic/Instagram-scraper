from models.todo import Todo
from database import todoCollection

async def fetch_one_todo(title):
    document=await todoCollection.find_one({"title":title})
    return document

async def fetch_all_todos():
    todos =[]
    cursor = todoCollection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos

async def create_todo(todo):
    document = todo.dict()
    result = await todoCollection.insert_one(document)
    return result
async def update_todo(title,desc):
    await todoCollection.update_one({"title":title},{"$set":{"description":desc}})
    document = await todoCollection.find_one({"title":title})
    return document
async def delete_todo(title):
    await todoCollection.delete_one({"title":title})
    return True
