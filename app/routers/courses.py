from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user


router = APIRouter(prefix="/courses", tags=["Courses"])


def owned_course(course_id: int, user_id: int, db: Session) -> models.Course:
    course = db.scalar(select(models.Course).where(models.Course.id == course_id, models.Course.owner_id == user_id))
    if not course:
        raise HTTPException(status_code=404, detail="Ders bulunamadı.")
    return course


@router.post("", response_model=schemas.CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(data: schemas.CourseCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    course = models.Course(**data.model_dump(), owner_id=user.id)
    db.add(course); db.commit(); db.refresh(course)
    return course


@router.get("", response_model=list[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.scalars(select(models.Course).where(models.Course.owner_id == user.id).order_by(models.Course.name)).all()


@router.get("/{course_id}", response_model=schemas.CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return owned_course(course_id, user.id, db)


@router.put("/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: int, data: schemas.CourseUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    course = owned_course(course_id, user.id, db)
    for key, value in data.model_dump(exclude_unset=True).items(): setattr(course, key, value)
    db.commit(); db.refresh(course)
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db.delete(owned_course(course_id, user.id, db)); db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

