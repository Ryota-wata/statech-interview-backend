from sqlalchemy import Column, Integer, String
from api.db import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255))
    correct_answer = Column(String(255))
