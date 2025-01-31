from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional

class Database:
    _instance: Optional['Database'] = None
    
    def __new__(cls, connection_string: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(connection_string)
        return cls._instance
    
    def _initialize(self, connection_string: str) -> None:
        self.engine = create_engine(connection_string)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self) -> Session:
        return self.SessionLocal()