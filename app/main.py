from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect, text

from . import models
from .database import engine
from .routers import auth, courses, dashboard, exams, tasks


models.Base.metadata.create_all(bind=engine)


def migrate_old_database() -> None:
    """Eski veritabanlarına veri kaybetmeden username alanını ekler."""
    columns = {column["name"] for column in inspect(engine).get_columns("users")}
    if "username" not in columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE users ADD COLUMN username VARCHAR(50)"))
            old_users = connection.execute(text("SELECT id FROM users")).fetchall()
            for user in old_users:
                connection.execute(
                    text("UPDATE users SET username = :username WHERE id = :user_id"),
                    {"username": f"user_{user.id}", "user_id": user.id},
                )
            connection.execute(
                text("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_username ON users (username)")
            )


migrate_old_database()

app = FastAPI(
    title="Study Planner API",
    description="Ders, görev, ödev ve sınavlarınızı yönetebileceğiniz basit bir REST API.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(tasks.router)
app.include_router(exams.router)
app.include_router(dashboard.router)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def root():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api-info", tags=["General"])
def api_info():
    return {"message": "Study Planner API çalışıyor.", "docs": "/docs"}


@app.get("/health", tags=["General"])
def health():
    return {"status": "ok"}
