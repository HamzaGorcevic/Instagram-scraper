# mongodb driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
database = client.TodoList
todoCollection = database.todo
mediaCollection = database.media

