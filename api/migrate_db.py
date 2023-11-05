from sqlalchemy import create_engine
from api.models.choice import Base as Choice
from api.models.user import Base as User
from api.models.question import Base as Question
from api.models.userAnswer import Base as UserAnswer

DB_URL = "mysql+pymysql://root@db:3306/statech?charset=utf8"
engine = create_engine(DB_URL, echo=True)

def reset_database():
    User.metadata.drop_all(bind=engine)
    User.metadata.create_all(bind=engine)

    Question.metadata.drop_all(bind=engine)
    Question.metadata.create_all(bind=engine)

    Choice.metadata.drop_all(bind=engine)
    Choice.metadata.create_all(bind=engine)

    UserAnswer.metadata.drop_all(bind=engine)
    UserAnswer.metadata.create_all(bind=engine)


if __name__ == "__main__":
  reset_database()
