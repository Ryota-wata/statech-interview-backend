from pydantic import BaseModel

class QuestionResponseModel(BaseModel):
  id: int
  text: str
  correct_answer: str

  class Config:
    orm_mode = True