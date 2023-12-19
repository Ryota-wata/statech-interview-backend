from pydantic import BaseModel
from datetime import datetime

class ResultResponseModel(BaseModel):
  id: int
  user_id: str
  corporate_id: int
  passed: bool
  created_at: datetime

  class Config:
    orm_mode = True
