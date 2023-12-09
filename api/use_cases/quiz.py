from sqlalchemy.orm.session import Session
from fastapi import HTTPException

# スキーマ
from api.schemas.response_model.question import QuestionResponseModel
from api.schemas.response_model.choice import ChoiceResponseModel
from api.schemas.request_model.userAnswer import UserAnswerRequestModel

# use_caseメソッド
from api.use_cases.base import UseCaseBaseModel

# repositoryメソッド
from api.repository.quiz import ChoiceRepository, QuestionRepository, UserAnswerRepository



class ConvertQuestionIdToQuestion(UseCaseBaseModel):
    def __init__(self, session: Session):
        self.session = session

    """質問ID(question_id)から質問を取得する"""

    async def convert_question_id_to_question(self, question_id: int) -> QuestionResponseModel:
        """質問を取得

          question_idを元に該当する質問を取得する

        """

        question = await QuestionRepository(session=self.session).fetch_question(question_id=question_id)

        if question is None:
            raise HTTPException(status_code=404, detail="該当する質問が存在しません")

        return question
    
    
class ConvertQuestionIdToChoices(UseCaseBaseModel):
    def __init__(self, session: Session):
        self.session = session

    """質問ID(question_id)から選択肢を取得する"""

    async def convert_question_id_to_choices(self, question_id: int) -> list[ChoiceResponseModel]:
        """選択肢を取得

          question_idを元に該当する選択肢を取得する

        """

        choices =  await ChoiceRepository(session=self.session).fetch_choices(question_id=question_id)

        if choices is None:
            raise HTTPException(status_code=404, detail="該当する選択肢が存在しません")

        return choices
    

class UserAnswer(UseCaseBaseModel):
    def __init__(self, session: Session):
        self.session = session

    """質問に対し回答し、その回答を保存する"""

    async def answer_question(self, users_answer: UserAnswerRequestModel):
        """質問に回答する

          質問に対する回答を保存する

        """

        answer = await UserAnswerRepository(session=self.session).save_answer(answer=users_answer)

        return answer