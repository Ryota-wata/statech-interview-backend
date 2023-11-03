from sqlalchemy import create_engine
from api.models.user import Base as User
from api.models.question import Base as Quesion

DB_URL = "mysql+pymysql://root@db:3306/statech?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
  User.metadata.drop_all(bind=engine)
  User.metadata.create_all(bind=engine)

  Quesion.metadata.drop_all(bind=engine)
  Quesion.metadata.create_all(bind=engine)


if __name__ == "__main__":
  reset_database()
