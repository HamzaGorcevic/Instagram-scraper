from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from routes import media,todo,proxy
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import httpx
# app object
app = FastAPI()

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(media.router,prefix="/api")
app.include_router(todo.router,prefix="/api",tags=["Media"])
app.include_router(proxy.router,prefix="")

    