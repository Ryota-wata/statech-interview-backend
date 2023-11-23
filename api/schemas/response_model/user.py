from pydantic import BaseModel

class UserResponseModel(BaseModel):
  id: int
  name: str
  email: str
  admin_flag: bool

  class Config:
    orm_mode = True
