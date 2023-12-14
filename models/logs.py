from sqlalchemy import Boolean, Column, Integer, String, DateTime
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import INET
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Log(Base):
    __tablename__ = "logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = Column(DateTime, default=func.now(), nullable=False)
    ip = Column(INET)
    method = Column(String)
    uri = Column(String)
    status_code = Column(Integer)
