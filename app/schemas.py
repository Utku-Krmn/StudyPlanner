from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Harf, rakam ve alt çizgi kullanılabilir.",
    )
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    username: str
    email: EmailStr
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CourseBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    code: str | None = Field(default=None, max_length=30)
    description: str | None = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    code: str | None = Field(default=None, max_length=30)
    description: str | None = None


class CourseOut(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    due_date: date
    course_id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    due_date: date | None = None
    course_id: int | None = None
    is_completed: bool | None = None


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_completed: bool


class ExamBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    exam_date: datetime
    location: str | None = Field(default=None, max_length=200)
    notes: str | None = None
    course_id: int


class ExamCreate(ExamBase):
    pass


class ExamUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    exam_date: datetime | None = None
    location: str | None = Field(default=None, max_length=200)
    notes: str | None = None
    course_id: int | None = None


class ExamOut(ExamBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class DashboardOut(BaseModel):
    upcoming_tasks: list[TaskOut]
    upcoming_exams: list[ExamOut]
    completed_tasks: list[TaskOut]
    total_courses: int
