from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    user_answer = relationship("UserAnswer", backref="users", cascade="delete")
