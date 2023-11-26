from pydantic import BaseModel, Field
from typing import List

class QuizRequestModel(BaseModel):
  question_text: str = Field(..., example="質問のテキスト")
  correct_answer: str = Field(..., example="正解のテキスト")
  choice_texts: List[str]
  
  class Config:
    orm_mode = True