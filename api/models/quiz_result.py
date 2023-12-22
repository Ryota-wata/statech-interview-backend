from sqlalchemy import Column, ForeignKey, Boolean, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from api.db import Base

class QuizResultOrm(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"))
    corporate_id = Column(Integer, ForeignKey("corporates.id"))
    passed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
