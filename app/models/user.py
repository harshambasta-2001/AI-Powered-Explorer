import uuid
 
from sqlalchemy import Column, String, DateTime, Integer, Text
from app.utils.helper_functions import get_current_time
from sqlalchemy.orm import Session
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        String(36),
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    # id =Column(Integer,primary_key=True,nullable=False,unique=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(255) ,nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(255), default="USER",nullable=False)
    created_at = Column(DateTime, nullable=False, default=get_current_time)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = self.id or str(uuid.uuid4())

    @classmethod
    def get_all_users(cls, db:Session):
        return db.query(cls).all()
    
    @classmethod
    def create_user(cls,db:Session,**kwargs):
        new_response = cls(**kwargs)
        db.add(new_response)
        db.commit()
        db.refresh(new_response)
        return new_response
    