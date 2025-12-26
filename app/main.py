from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base
from app.routes.auth import router as auth_router
from app.routes.log import router as log_router

app = FastAPI(title="Auth Service")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(log_router)