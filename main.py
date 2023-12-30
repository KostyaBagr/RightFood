from fastapi import FastAPI
from src.users.views import router as users_router

app = FastAPI()

@app.get('/')
def hello():
    return {'hello':'world'}

app.include_router(users_router, prefix='/users')