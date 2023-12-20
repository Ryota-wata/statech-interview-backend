from pydantic import BaseModel, Field

class QuizRequestModel(BaseModel):
  corporate_id: int
  question_text: str = Field(..., example="質問のテキスト")
  correct_choice: str = Field(..., example="正解選択肢のテキスト")
  wrong_choice: str = Field(..., example="不正解選択肢のテキスト")
  correct_answer: str = Field(..., example="正解のテキスト")

  class Config:
    orm_mode = True