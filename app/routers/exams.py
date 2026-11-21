from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user
from .courses import owned_course


router = APIRouter(prefix="/exams", tags=["Exams"])


def owned_exam(exam_id: int, user_id: int, db: Session) -> models.Exam:
    exam = db.scalar(select(models.Exam).where(models.Exam.id == exam_id, models.Exam.owner_id == user_id))
    if not exam: raise HTTPException(status_code=404, detail="Sınav bulunamadı.")
    return exam


@router.post("", response_model=schemas.ExamOut, status_code=status.HTTP_201_CREATED)
def create_exam(data: schemas.ExamCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    owned_course(data.course_id, user.id, db)
    exam = models.Exam(**data.model_dump(), owner_id=user.id)
    db.add(exam); db.commit(); db.refresh(exam)
    return exam


@router.get("", response_model=list[schemas.ExamOut])
def list_exams(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.scalars(select(models.Exam).where(models.Exam.owner_id == user.id).order_by(models.Exam.exam_date)).all()


@router.get("/{exam_id}", response_model=schemas.ExamOut)
def get_exam(exam_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return owned_exam(exam_id, user.id, db)


@router.put("/{exam_id}", response_model=schemas.ExamOut)
def update_exam(exam_id: int, data: schemas.ExamUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    exam = owned_exam(exam_id, user.id, db); values = data.model_dump(exclude_unset=True)
    if "course_id" in values: owned_course(values["course_id"], user.id, db)
    for key, value in values.items(): setattr(exam, key, value)
    db.commit(); db.refresh(exam)
    return exam


@router.delete("/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exam(exam_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db.delete(owned_exam(exam_id, user.id, db)); db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

