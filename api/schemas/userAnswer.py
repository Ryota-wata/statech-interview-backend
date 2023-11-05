from pydantic import BaseModel

class UserAnswer(BaseModel):
  id: int
  user_id: int
  question_id: int
  choice_id: int