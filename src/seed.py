from sqlalchemy.orm import Session
from src import crud, schemas
from src.auth import get_password_hash

def seed_database(db: Session):
    # Создаем админа
    admin_user = crud.get_user_by_email(db, email="admin@example.com")
    if not admin_user:
        admin_data = {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "password": "admin123",
            "password_confirm": "admin123",
            "role": "admin"
        }
        admin_user = crud.create_user(db, schemas.UserCreate(**admin_data))
        admin_user.role = "admin"
        db.commit()

    # Создаем обычного пользователя
    regular_user = crud.get_user_by_email(db, email="user@example.com")
    if not regular_user:
        user_data = {
            "first_name": "Regular",
            "last_name": "User",
            "email": "user@example.com",
            "password": "user123",
            "password_confirm": "user123",
            "role": "user"
        }
        regular_user = crud.create_user(db, schemas.UserCreate(**user_data))
        regular_user.role = "user"
        db.commit()

    print("Database seeded with test users.")
