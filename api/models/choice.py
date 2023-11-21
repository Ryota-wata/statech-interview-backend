from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from api.db import Base

class ChoiceOrm(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255))
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_answer = relationship("UserAnswerOrm", backref="choices", cascade="delete")
