from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=schemas.DashboardOut)
def dashboard(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    today = date.today(); last_day = today + timedelta(days=7)
    upcoming_tasks = db.scalars(select(models.Task).where(models.Task.owner_id == user.id, models.Task.is_completed.is_(False), models.Task.due_date.between(today, last_day)).order_by(models.Task.due_date)).all()
    start = datetime.combine(today, time.min); end = datetime.combine(last_day, time.max)
    upcoming_exams = db.scalars(select(models.Exam).where(models.Exam.owner_id == user.id, models.Exam.exam_date.between(start, end)).order_by(models.Exam.exam_date)).all()
    completed_tasks = db.scalars(select(models.Task).where(models.Task.owner_id == user.id, models.Task.is_completed.is_(True)).order_by(models.Task.due_date.desc())).all()
    total_courses = db.scalar(select(func.count(models.Course.id)).where(models.Course.owner_id == user.id)) or 0
    return {"upcoming_tasks": upcoming_tasks, "upcoming_exams": upcoming_exams, "completed_tasks": completed_tasks, "total_courses": total_courses}

