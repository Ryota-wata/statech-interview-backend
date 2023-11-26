from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from api.db import Base
from api.models.user import UserOrm

class UserAnswerOrm(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    choice_id = Column(Integer, ForeignKey("choices.id"))
    took_exam_num = Column(Integer)
