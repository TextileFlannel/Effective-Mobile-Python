from fastapi import FastAPI
from src.database import engine
import src.models
from src.routers import auth

src.models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API")

app.include_router(auth.router)
