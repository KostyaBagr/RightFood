from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool


class CreateUserRequest(BaseModel):
    email: EmailStr
    hashed_password: str
    is_active: bool
    name: str
    lastname: str
    age: str
    weight: str
    height: str
