from fastapi import FastAPI
from src.users.router import router as users_router
from src.diary.router import router as diary_router
app = FastAPI()

@app.get('/')
def hello():
    return {'hello':'world'}

app.include_router(users_router, prefix='/users')

app.include_router(diary_router, prefix='/diary')