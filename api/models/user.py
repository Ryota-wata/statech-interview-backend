from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from api.db import Base


class UserOrm(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    admin_flag = Column(Boolean, default=False)
    user_answer = relationship("UserAnswerOrm", backref="users", cascade="delete")
