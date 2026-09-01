from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class DBTask(Base):
    __tablename__ = "tasks"  # Postgres mein table ka naam yeh hoga

    id = Column(Integer, primary_key=True, index=True) # Primary Key (1, 2, 3...)
    title = Column(String, index=True)
    description = Column(String, nullable=True)        # Yeh empty (null) ho sakta hai
    completed = Column(Boolean, default=False)