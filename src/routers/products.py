from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from src.auth import get_current_user, get_current_admin
from src import models

router = APIRouter(prefix="/products", tags=["products"])

# Mock данные для товаров
mock_products = [
    {
        "id": 1,
        "name": "Ноутбук Lenovo ThinkPad",
        "description": "Бизнес-ноутбук для профессионалов",
        "price": 85000,
        "owner_id": 1,  # admin
        "category": "Электроника"
    },
    {
        "id": 2,
        "name": "Смартфон Samsung Galaxy",
        "description": "Флагманский смартфон с отличной камерой",
        "price": 45000,
        "owner_id": 2,  # user
        "category": "Электроника"
    },
    {
        "id": 3,
        "name": "Кофемашина DeLonghi",
        "description": "Автоматическая кофемашина для дома",
        "price": 25000,
        "owner_id": 1,  # admin
        "category": "Бытовая техника"
    },
    {
        "id": 4,
        "name": "Книга 'Python для начинающих'",
        "description": "Учебник по программированию",
        "price": 1200,
        "owner_id": 2,  # user
        "category": "Книги"
    }
]

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ProductResponse])
def get_products(
    category: Optional[str] = None,
    current_user: models.User = Depends(get_current_user)
):
    products = mock_products.copy()

    if current_user.role != "admin":
        products = [p for p in products if p["owner_id"] == current_user.id]

    if category:
        products = [p for p in products if p["category"].lower() == category.lower()]

    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    current_user: models.User = Depends(get_current_user)
):
    product = next((p for p in mock_products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )

    if current_user.role != "admin" and product["owner_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен"
        )

    return product

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    current_user: models.User = Depends(get_current_user)
):
    new_id = max(p["id"] for p in mock_products) + 1
    new_product = {
        "id": new_id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "owner_id": current_user.id
    }
    mock_products.append(new_product)
    return new_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductCreate,
    current_user: models.User = Depends(get_current_user)
):
    product = next((p for p in mock_products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )

    if current_user.role != "admin" and product["owner_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен"
        )

    product.update({
        "name": product_update.name,
        "description": product_update.description,
        "price": product_update.price,
        "category": product_update.category
    })

    return product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    current_user: models.User = Depends(get_current_user)
):
    global mock_products
    product = next((p for p in mock_products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )

    if current_user.role != "admin" and product["owner_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен"
        )

    mock_products = [p for p in mock_products if p["id"] != product_id]
    return {"message": "Товар успешно удален"}
