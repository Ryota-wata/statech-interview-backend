from sqlalchemy import Boolean, Column, String, Integer
from sqlalchemy.orm import relationship
from api.db import Base


class CorporateOrm(Base):
    __tablename__ = "corporates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
