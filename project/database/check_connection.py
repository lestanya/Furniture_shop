# db/check_connection.py
from sqlalchemy import text
from connect_db import SessionLocal, init_db, logger  

def check_connection():
    init_db()  
    db = SessionLocal()
    try:
        logger.info("Проверка соединения с БД через SELECT 1...")
        result = db.execute(text("SELECT 1")).scalar()
        logger.info(f"Результат SELECT 1: {result}")
    finally:
        db.close()
        logger.info("Сессия закрыта.")


if __name__ == "__main__":
    check_connection()
