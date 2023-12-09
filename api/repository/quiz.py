from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# モデル
from api.models.question import QuestionOrm
from api.models.choice import ChoiceOrm
from api.models.userAnswer import UserAnswerOrm

# スキーマ
from api.schemas.response_model.question import QuestionResponseModel
from api.schemas.response_model.choice import ChoiceResponseModel
from api.schemas.request_model.userAnswer import UserAnswerRequestModel


class QuestionRepository:
    """Questionテーブルへアクセス"""

    def __init__(self, session: Session) -> None:
        self.session = session

    async def fetch_question(self, question_id: int) -> QuestionResponseModel | None:
        """質問IDから質問を取得する

        Questionテーブルのquestion_idとリクエストのquestion_idが完全一致した場合、そQuestionテーブルのレコードを返す

        Args:
            question_id(int): 質問ID
        Returns:
            QuestionResponseModel: 質問ID、質問文、正解

        """

        question = (
            await self.session.execute(
                select(QuestionOrm)
                .where(QuestionOrm.id == question_id)
            )
        ).scalars().one_or_none()

        self.session.commit()

        if not question:
            return None

        return question
    
class ChoiceRepository:
    """Choiceテーブルへアクセス"""

    def __init__(self, session: Session) -> None:
        self.session = session

    async def fetch_choices(self, question_id: int) -> list[ChoiceResponseModel] | None:
        """質問IDから選択肢を取得する

        テーブルのquestion_idとリクエストのquestion_idが完全一致した場合、そのChoiceテーブルのレコードを返す

        Args:
            question_id(int): 質問ID
        Returns:
            list[ChoiceResponseModel] : list[選択肢ID、質問ID、質問文]

        """

        choices = (
            await self.session.execute(
                select(ChoiceOrm)
                .where(ChoiceOrm.question_id == question_id)
            )
        ).scalars().all()

        self.session.commit()

        if not choices:
            return None

        return choices
    

class UserAnswerRepository:
    """UserAnswerテーブルにアクセス"""

    def __init__(self, session: Session) -> None:
        self.session = session

    async def save_answer(self, answer: UserAnswerRequestModel):
        """質問に対する回答を保存する

        Args:
            answer(UserAnswerRequestModel): ユーザーの回答

        """

        # ユーザーが特定の質問に対して既に回答した回数を取得
        stmt = select(UserAnswerOrm).where(UserAnswerOrm.user_id == answer.user_id, UserAnswerOrm.question_id == answer.question_id)
        result = await self.session.execute(stmt)
        last_took_exam_num = result.scalars().all()

        user_answer = UserAnswerOrm(
            user_id=answer.user_id,
            question_id=answer.question_id,
            choice_id=answer.choice_id,
            took_exam_num = len(last_took_exam_num) + 1
        )
        try:
            self.session.add(user_answer)
            await self.session.commit()
            return "success"

        except SQLAlchemyError as e:
            self.session.rollback()
            raise e