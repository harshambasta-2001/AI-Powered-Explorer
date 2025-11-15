import uuid
 
from sqlalchemy import Column, String, DateTime, Integer, Text,Enum,and_
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.sql.schema import ForeignKey, Column
from app.utils.helper_functions import get_current_time
from app.utils.enum import ContentType
from sqlalchemy.orm import Session

from app.database import Base


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(
        String(36),
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="cascade"),nullable=False)
    type = Column(Enum(ContentType), nullable=False) # 'search' or 'image'
    # title = Column(String(255), nullable=False)
    content = Column(Text,nullable=False)
    prompt_or_query = Column(Text)
    notes = Column(Text,nullable=True)
    created_at = Column(DateTime, nullable=False, default=get_current_time)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = self.id or str(uuid.uuid4())

    @classmethod
    def get_all_tasks(cls, db:Session):
        return db.query(cls).all()

    @classmethod
    def get_tasks_by_user(cls, db: Session, user_id: str, task_type: ContentType = None):
        if task_type is None:
            tasks = db.query(cls).filter(cls.user_id == user_id).all()
        else:
            tasks = db.query(cls).filter(and_(cls.user_id == user_id,cls.type == task_type)).all()
        return tasks

    @classmethod
    def get_task_by_id(cls, db: Session, task_id: str):
        return db.query(cls).filter(cls.id == task_id).first()