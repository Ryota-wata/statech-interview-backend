from pydantic import BaseModel

class QuizResponseModel(BaseModel):
  question_id: int
  question_text: str
  correct_choice: str
  wrong_choice: str
  correct_answer: str

  class Config:
    orm_mode = True