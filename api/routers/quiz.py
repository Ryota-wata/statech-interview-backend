from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db

# スキーマ
from api.schemas.request_model.userAnswer import UserAnswerRequestModel
from api.schemas.response_model.choice import ChoiceResponseModel
from api.schemas.response_model.question import QuestionResponseModel

# use_caseメソッド
from api.use_cases.quiz import ConvertQuestionIdToChoices, ConvertQuestionIdToQuestion, UserAnswer


router = APIRouter()

@router.get("/question/{question_id}", response_model=QuestionResponseModel)
async def get_question(question_id: int, session: AsyncSession = Depends(get_db)):
    """質問を取得するエンドポイント

      【Request】
        question_id: 質問ID
      
      【Response】
        question_id: 質問ID,
        text: 質問文,
        correct_answer: 正解

    """
    # use_case層のメソッド呼び出し
    question = await ConvertQuestionIdToQuestion(session=session).convert_question_id_to_question(question_id=question_id)

    return question


@router.get("/questions/{question_id}/choices", response_model=list[ChoiceResponseModel])
async def get_choices(question_id: int, session: AsyncSession = Depends(get_db)):
    """質問の選択肢を取得するエンドポイント

      【Request】
        question_id: 質問ID

      【Response】
        choice_id: 選択肢ID,
        question_id: 質問ID,
        text: 選択肢

    """
    # use_case層のメソッド呼び出し
    choices = await ConvertQuestionIdToChoices(session=session).convert_question_id_to_choices(question_id=question_id)

    return choices


@router.post("/questions/{question_id}/answers")
async def answer_question(answer: UserAnswerRequestModel, session: AsyncSession = Depends(get_db)):
    """質問を回答するエンドポイント

      【Request】
        user_id: ユーザID,
        question_id: 質問ID,
        choice_id: 選択肢ID

    """
    # use_case層のメソッド呼び出し
    user_answer = await UserAnswer(session=session).answer_question(users_answer=answer)

    return user_answer

