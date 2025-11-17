from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src import schemas
from src import crud
from src.database import get_db
from src.auth import get_current_user, create_access_token, get_current_admin
from src import models

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован"
        )
    return crud.create_user(db=db, user=user)

@router.post("/login")
def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.UserResponse)
def update_user_me(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_user = crud.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return updated_user

@router.delete("/me")
def delete_user_me(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    crud.soft_delete_user(db, current_user.id)
    return {"message": "Аккаунт пользователя успешно деактивирован"}

@router.post("/logout")
def logout():
    return {"message": "Успешно вышел из системы"}

@router.get("/admin/users", response_model=list[schemas.UserResponse])
def get_all_users(current_admin: models.User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@router.delete("/admin/users/{user_id}")
def delete_user(user_id: int, current_admin: models.User = Depends(get_current_admin), db: Session = Depends(get_db)):
    user = crud.delete_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return {"message": f"Пользователь {user_id} успешно удален"}
