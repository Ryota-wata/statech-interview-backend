from sqlalchemy import select
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.choice import ChoiceOrm
from api.models.question import QuestionOrm
from api.models.userAnswer import UserAnswerOrm
from api.schemas.request_model.userAnswer import UserAnswerRequestModel
from api.schemas.response_model.choice import ChoiceResponseModel
from api.schemas.response_model.question import QuestionResponseModel
from api.db import get_db


router = APIRouter()

@router.get("/question/{question_id}", response_model=QuestionResponseModel)
async def get_question(question_id: int, db: AsyncSession = Depends(get_db)):
    """質問を取得するエンドポイント
      Request:
        question_id: 質問ID
      Response:
        quesiton_id: 質問ID
        text: 質問文
        correct_answer: 正解
    """

    stmt = select(QuestionOrm).where(QuestionOrm.id == question_id)
    result = await db.execute(stmt)
    question = result.scalars().one_or_none()
    return question


@router.get("/questions/{question_id}/choices", response_model=list[ChoiceResponseModel])
async def get_choices(question_id: int, db: AsyncSession = Depends(get_db)):
    """質問の選択肢を取得するエンドポイント
      Request:
        question_id: 質問ID
      Response:
        choice_id: 選択肢ID
        question_id: 質問ID
        text: 選択肢文

    """
    stmt = select(ChoiceOrm).where(ChoiceOrm.question_id == question_id)
    result = await db.execute(stmt)
    choices = result.scalars().all()
    return choices


@router.post("/questions/{question_id}/answers")
async def answer_question(answer: UserAnswerRequestModel, db: AsyncSession = Depends(get_db)):
    """質問を回答するエンドポイント
      Request:
        id: ユーザ回答ID
        user_id: ユーザID
        question_id: 質問ID
        choice_id: 選択肢ID
    """

    # ユーザーが特定の質問に対して既に回答した回数を取得
    stmt = select(UserAnswerOrm).where(UserAnswerOrm.user_id == answer.user_id, UserAnswerOrm.question_id == answer.question_id)
    result = await db.execute(stmt)
    last_took_exam_num = result.scalars().all()


    user_answer = UserAnswerOrm(
        user_id=answer.user_id,
        question_id=answer.question_id,
        choice_id=answer.choice_id,
        took_exam_num = len(last_took_exam_num) + 1
    )
    db.add(user_answer)
    await db.commit()
