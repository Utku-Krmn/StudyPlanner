from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    courses: Mapped[list["Course"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    tasks: Mapped[list["Task"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    exams: Mapped[list["Exam"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    code: Mapped[str | None] = mapped_column(String(30), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    owner: Mapped[User] = relationship(back_populates="courses")
    tasks: Mapped[list["Task"]] = relationship(back_populates="course", cascade="all, delete-orphan")
    exams: Mapped[list["Exam"]] = relationship(back_populates="course", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    due_date: Mapped[date] = mapped_column(Date)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    course: Mapped[Course] = relationship(back_populates="tasks")
    owner: Mapped[User] = relationship(back_populates="tasks")


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    exam_date: Mapped[datetime] = mapped_column(DateTime)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    course: Mapped[Course] = relationship(back_populates="exams")
    owner: Mapped[User] = relationship(back_populates="exams")
