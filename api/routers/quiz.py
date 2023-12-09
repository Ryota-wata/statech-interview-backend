from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db

# スキーマ
from api.schemas.request_model.userAnswer import UserAnswerRequestModel
from api.schemas.response_model.question import QuestionResponseModel

# use_caseクラス
from api.use_cases.quiz import ConvertQuestionIdToQuestionInfo, UserAnswer


router = APIRouter()

@router.get("/question/{question_id}", response_model=QuestionResponseModel)
async def get_question(question_id: int, session: AsyncSession = Depends(get_db)):
    """質問と選択肢を取得するエンドポイント

      【Request】
        question_id: 質問ID
      
      【Response】
        question_id: 質問ID,
        text: 質問文,
        corporate_id": 会社ID,
        correct_answer: 正解
        choices: 選択肢（リスト）

    """
    # use_case層のメソッド呼び出し
    question_info = await ConvertQuestionIdToQuestionInfo(session=session).convert_question_id_to_question_info(question_id=question_id)

    return question_info


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

