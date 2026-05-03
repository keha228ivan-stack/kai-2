from datetime import date
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    department: str


class CourseAssignmentCreate(BaseModel):
    user_id: int
    course_id: int


class CourseOut(BaseModel):
    id: int
    name: str
    description: str
    start_date: date | None = None
    end_date: date | None = None
    deadline: date | None = None

    class Config:
        from_attributes = True
