from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user
from .courses import owned_course


router = APIRouter(prefix="/tasks", tags=["Tasks"])


def owned_task(task_id: int, user_id: int, db: Session) -> models.Task:
    task = db.scalar(select(models.Task).where(models.Task.id == task_id, models.Task.owner_id == user_id))
    if not task: raise HTTPException(status_code=404, detail="Görev bulunamadı.")
    return task


@router.post("", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    owned_course(data.course_id, user.id, db)
    task = models.Task(**data.model_dump(), owner_id=user.id)
    db.add(task); db.commit(); db.refresh(task)
    return task


@router.get("", response_model=list[schemas.TaskOut])
def list_tasks(completed: bool | None = None, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    query = select(models.Task).where(models.Task.owner_id == user.id)
    if completed is not None: query = query.where(models.Task.is_completed == completed)
    return db.scalars(query.order_by(models.Task.due_date)).all()


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return owned_task(task_id, user.id, db)


@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    task = owned_task(task_id, user.id, db)
    values = data.model_dump(exclude_unset=True)
    if "course_id" in values: owned_course(values["course_id"], user.id, db)
    for key, value in values.items(): setattr(task, key, value)
    db.commit(); db.refresh(task)
    return task


@router.patch("/{task_id}/complete", response_model=schemas.TaskOut)
def complete_task(task_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    task = owned_task(task_id, user.id, db); task.is_completed = True
    db.commit(); db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db.delete(owned_task(task_id, user.id, db)); db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

