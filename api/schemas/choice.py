from pydantic import BaseModel

class Choice(BaseModel):
  id: int
  text: str
  question_id: int