from pydantic import BaseModel

class UserAnswerRequestModel(BaseModel):
  user_id: str
  question_id: int
  choice_id: int
  
  class Config:
    orm_mode = True
