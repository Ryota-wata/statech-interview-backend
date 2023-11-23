from pydantic import BaseModel

class ChoiceResponseModel(BaseModel):
  id: int
  question_id: int
  text: str
  
  class Config:
    orm_mode = True