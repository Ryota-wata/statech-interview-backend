from pydantic import BaseModel

class QuestionResponseModel(BaseModel):
  id: int
  text: str
  corporate_id: int
  correct_answer: str

  class Config:
    orm_mode = True