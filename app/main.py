from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from . import models, schemas, database
from .database import engine

app = FastAPI(
    title="User Management API",
    description="""
    A RESTful API for user management with complete CRUD operations.
    
    ## Features
    * Create new users
    * Retrieve user information
    * Update user details
    * Delete users
    * List all users with pagination
    
    ## Authentication
    This API is currently unauthenticated. In production, you should implement proper authentication.
    
    ## Database
    The API uses SQLAlchemy with SQLite for local development and supports PostgreSQL for production.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations with users. The **users** tag allows you to manage user data.",
        }
    ]
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.post(
    "/users/",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
    summary="Create a new user",
    description="""
    Create a new user with the following information:
    
    * **username**: Unique username for the user
    * **email**: Valid email address
    * **first_name**: User's first name
    * **last_name**: User's last name
    * **role**: User role (admin, user, guest)
    * **active**: Whether the user is active (default: True)
    """,
    response_description="The created user information"
)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    """
    Create a new user with the following information:
    
    - **username**: Unique username
    - **email**: Valid email address
    - **first_name**: First name
    - **last_name**: Last name
    - **role**: User role
    - **active**: Active status
    """
    result = await db.execute(select(models.User).filter(models.User.email == user.email))
    db_user = result.scalar_one_or_none()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.get(
    "/users/",
    response_model=List[schemas.User],
    tags=["users"],
    summary="List all users",
    description="Retrieve a list of all users with pagination support."
)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(database.get_db)
):
    """
    Retrieve users with pagination.
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users

@app.get(
    "/users/{user_id}",
    response_model=schemas.User,
    tags=["users"],
    summary="Get user by ID",
    description="Retrieve a specific user by their ID.",
    responses={
        404: {"description": "User not found"},
        200: {
            "description": "User found",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "username": "johndoe",
                        "email": "john@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "role": "user",
                        "active": True,
                        "created_at": "2024-01-01T00:00:00",
                        "updated_at": None
                    }
                }
            }
        }
    }
)
async def read_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
    """
    Get a specific user by their ID.
    
    - **user_id**: The ID of the user to retrieve
    """
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return db_user

@app.put(
    "/users/{user_id}",
    response_model=schemas.User,
    tags=["users"],
    summary="Update user",
    description="Update an existing user's information.",
    responses={
        404: {"description": "User not found"},
        200: {"description": "User updated successfully"}
    }
)
async def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: AsyncSession = Depends(database.get_db)
):
    """
    Update a user's information.
    
    - **user_id**: The ID of the user to update
    - **user**: The updated user information
    """
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["users"],
    summary="Delete user",
    description="Delete a user by their ID.",
    responses={
        404: {"description": "User not found"},
        204: {"description": "User deleted successfully"}
    }
)
async def delete_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
    """
    Delete a user.
    
    - **user_id**: The ID of the user to delete
    """
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    await db.delete(db_user)
    await db.commit()
    return None 