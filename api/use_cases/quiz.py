from sqlalchemy.orm.session import Session
from fastapi import HTTPException
import logging

# スキーマ
from api.schemas.response_model.question import QuestionResponseModel
from api.schemas.request_model.userAnswer import UserAnswerRequestModel

# use_case基底クラス
from api.use_cases.base import UseCaseBaseModel

# repositoryクラス
from api.repository.quiz import QuestionInfoRepository, UserAnswerRepository


class ConvertQuestionIdToQuestionInfo(UseCaseBaseModel):
    def __init__(self, session: Session):
        self.session = session

    async def convert_question_id_to_question_info(self, question_id: int) -> QuestionResponseModel:
        """質問を取得

          question_idを元に該当する質問と選択肢を取得する

        """

        question_info = await QuestionInfoRepository(session=self.session).fetch_question_info(question_id=question_id)

        logging.warning("クイズ%s", question_info)

        if question_info is None:
            raise HTTPException(status_code=404, detail="該当する質問情報が存在しません")

        return question_info
    

class UserAnswer(UseCaseBaseModel):
    def __init__(self, session: Session):
        self.session = session

    async def answer_question(self, users_answer: UserAnswerRequestModel):
        """質問に回答する

          質問に対する回答を保存する

        """

        answer_result = await UserAnswerRepository(session=self.session).save_answer(answer=users_answer)

        return answer_result