from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./chat_history.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    """
    Veritabanı oturumu oluşturur ve yönetir.
    
    Bu fonksiyon, veritabanı oturumu (Session) oluşturur ve 
    işlem sonunda oturumu kapatır. Kullanıcıların veritabanı ile 
    etkileşimde bulunmalarını sağlamak için bir jeneratör olarak 
    tasarlanmıştır.
    
    Returns:
        Generator[Session, None, None]: Veritabanı oturumu sağlayan bir jeneratör.
    """
    db = SessionLocal() 
    try:
        yield db  
    finally:
        db.close()  
