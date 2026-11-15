from uuid import UUID, uuid4
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="User Management CRUD API",
    description="Task 01 - REST API with In-Memory Storage",
    version="1.0.0"
)

# In-memory database using a Python hash map (dict)
# Key: UUID, Value: User data dictionary
users_db: Dict[UUID, dict] = {}


# --- Pydantic Schemas ---
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Jane Doe")
    email: EmailStr = Field(..., example="jane.doe@example.com")
    age: int = Field(..., ge=0, le=130, example=24)


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, example="Jane Smith")
    email: Optional[EmailStr] = Field(None, example="jane.smith@example.com")
    age: Optional[int] = Field(None, ge=0, le=130, example=25)


class UserResponse(UserBase):
    id: UUID


# --- API Endpoints ---

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    """Create a new user with an auto-generated UUID."""
    user_id = uuid4()
    user_data = payload.model_dump()
    user_record = {"id": user_id, **user_data}
    
    users_db[user_id] = user_record
    return user_record


@app.get("/users", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users():
    """Retrieve all users."""
    return list(users_db.values())


@app.get("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: UUID):
    """Retrieve a single user by their UUID."""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' not found."
        )
    return users_db[user_id]


@app.put("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: UUID, payload: UserUpdate):
    """Update user fields. Returns 404 if not found, 400 if body is empty."""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' not found."
        )
    
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields provided to update."
        )
        
    users_db[user_id].update(update_data)
    return users_db[user_id]


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID):
    """Delete a user by their UUID."""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' not found."
        )
    del users_db[user_id]
    return None