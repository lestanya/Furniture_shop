import os
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv, find_dotenv

from .models import Base

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


load_dotenv(find_dotenv())
DATABASE_URL = os.getenv("URL")

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
    echo=True,  
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def init_db() -> None:
    logger.info("Создание таблиц (если их ещё нет)...")
    Base.metadata.create_all(bind=engine)
    logger.info("Инициализация БД завершена.")


def get_db():
    db: Session = SessionLocal()
    try:
        logger.debug("Открытие новой сессии БД")
        yield db
    finally:
        logger.debug("Закрытие сессии БД")
        db.close()
