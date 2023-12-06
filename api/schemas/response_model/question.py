from pydantic import BaseModel

class QuestionResponseModel(BaseModel):
  id: int
  text: str
  correct_answer: str
  choices: list

  class Config:
    orm_mode = True
