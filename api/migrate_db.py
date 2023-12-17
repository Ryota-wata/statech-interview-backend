from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models.choice import ChoiceOrm
from api.models.user import UserOrm
from api.models.corporate import CorporateOrm
from api.models.question import QuestionOrm
from api.models.userAnswer import UserAnswerOrm
from api.models.quiz_result import QuizResultOrm

DB_URL = "mysql+pymysql://root@db:3306/statech?charset=utf8"
engine = create_engine(DB_URL, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

def reset_database():
    UserOrm.metadata.drop_all(bind=engine)
    UserOrm.metadata.create_all(bind=engine)

    CorporateOrm.metadata.drop_all(bind=engine)
    CorporateOrm.metadata.create_all(bind=engine)

    QuestionOrm.metadata.drop_all(bind=engine)
    QuestionOrm.metadata.create_all(bind=engine)

    ChoiceOrm.metadata.drop_all(bind=engine)
    ChoiceOrm.metadata.create_all(bind=engine)

    UserAnswerOrm.metadata.drop_all(bind=engine)
    UserAnswerOrm.metadata.create_all(bind=engine)

    QuizResultOrm.metadata.drop_all(bind=engine)
    QuizResultOrm.metadata.create_all(bind=engine)

    #初期データ投入
    corporate = CorporateOrm(id=1, name="走る技術")

    question1 = QuestionOrm(id=1, corporate_id=1, text="「エンジニア転職チャンネル」を知っていますか？", correct_answer="いつも楽しみに見てます！")
    choice1_1 = ChoiceOrm(id=1, text="いつも楽しみに見てます！", question_id=1)
    choice1_2 = ChoiceOrm(id=2, text="なんですかそれ？", question_id=1)

    question2 = QuestionOrm(id=2, corporate_id=1, text="「スタートアップこそ最高のキャリアである」を知ってますか？", correct_answer="感銘を受けました！")
    choice2_1 = ChoiceOrm(id=3, text="知らないです。", question_id=2)
    choice2_2 = ChoiceOrm(id=4, text="感銘を受けました！", question_id=2)

    question3 = QuestionOrm(id=3, corporate_id=1, text="お酒は好きですか？", correct_answer="飲みニケーションが全てだと思ってます！")
    choice3_1 = ChoiceOrm(id=5, text="嫌いです。", question_id=3)
    choice3_2 = ChoiceOrm(id=6, text="飲みニケーションが全てだと思ってます！", question_id=3)

    question4 = QuestionOrm(id=4, corporate_id=1, text="最強のエディターはなんだと思いますか？", correct_answer="vim")
    choice4_1 = ChoiceOrm(id=7, text="vim", question_id=4)
    choice4_2 = ChoiceOrm(id=8, text="VScode", question_id=4)

    question5 = QuestionOrm(id=5, corporate_id=1, text="X（twitter）はしてますか？", correct_answer="仕事だと思ってます")
    choice5_1 = ChoiceOrm(id=9, text="興味ないです。", question_id=5)
    choice5_2 = ChoiceOrm(id=10, text="仕事だと思ってます", question_id=5)

    # データベースに追加
    session.add_all([corporate,
                    question1, choice1_1, choice1_2,
                    question2, choice2_1, choice2_2,
                    question3, choice3_1, choice3_2,
                    question4, choice4_1, choice4_2,
                    question5, choice5_1, choice5_2, ])

    # コミットして変更を保存
    session.commit()

    # セッションを閉じる
    session.close()


if __name__ == "__main__":
  reset_database()
