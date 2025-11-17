from fastapi import FastAPI
from src.database import engine, SessionLocal
import src.models
from src.routers import auth, products
from src.seed import seed_database

src.models.Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    seed_database(db)
finally:
    db.close()

app = FastAPI(title="User Management API")

app.include_router(auth.router)
app.include_router(products.router)
