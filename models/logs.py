from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum
from database import Base
from sqlalchemy.sql import func

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)# не забыть сменить на uuid4!!!!!!
    created = Column(DateTime, default=func.now(), nullable=False)
    ip = Column(String)
    method = Column(String)
    uri = Column(String)
    status_code = Column(Integer)
