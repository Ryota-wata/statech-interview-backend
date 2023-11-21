from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db import Base


class QuestionOrm(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255))
    correct_answer = Column(String(255))
    choice = relationship("ChoiceOrm", backref="questions", cascade="delete")
    user_answer = relationship("UserAnswerOrm", backref="questions", cascade="delete")
