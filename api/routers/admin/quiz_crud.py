from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db

# スキーマ
from api.schemas.request_model.quiz_crud import QuizRequestModel
from api.schemas.response_model.quiz_crud import QuizResponseModel

# use_caseクラス
from api.use_cases.admin.quiz_crud import QuizCrud


router = APIRouter()

@router.get("/admin/quizzes/")
async def get_quizzes(session: AsyncSession = Depends(get_db)) -> list[QuizResponseModel]:
    """クイズ一覧を取得するエンドポイント
    
      【QuizResponseModel】
        question_id: 質問ID,
        question_text: 質問文,
        correct_choice: 正解選択肢,
        wrong_choice: 不正解選択肢,
        correct_answer: 正解,
    
    """
    # use_case層のメソッド呼び出し
    quizzes = await QuizCrud(session=session).get_quizzes_all()

    return quizzes


@router.post("/admin/create-quiz/")
async def create_quiz(create_quiz: QuizRequestModel, session: AsyncSession = Depends(get_db)):
    """クイズを作成するエンドポイント

      【Request】
        corporate_id: 会社ID,
        question_text: 質問文,
        correct_choice: 正解選択肢,
        wrong_choice: 不正解選択肢,
        correct_answer: 正解

    """
    # use_case層のメソッド呼び出し
    new_quiz = await QuizCrud(session=session).create_quiz(create_quiz=create_quiz)

    return new_quiz


@router.put("/admin/update-quiz/{question_id}/")
async def update_quiz(question_id: int, update_quiz: QuizRequestModel, session: AsyncSession = Depends(get_db)):
    """クイズを編集するエンドポイント

      【Request】
        corporate_id: 会社ID,
        question_text: 質問文,
        correct_choice: 正解選択肢,
        wrong_choice: 不正解選択肢,
        correct_answer: 正解

    """
    # use_case層のメソッド呼び出し
    update_quiz = await QuizCrud(session=session).update_quiz(question_id=question_id, update_quiz=update_quiz)

    return update_quiz


@router.delete("/admin/delete-quiz/{question_id}/")
async def delete_quiz(question_id: int, session: AsyncSession = Depends(get_db)):
    """クイズを削除するエンドポイント"""

    # use_case層のメソッド呼び出し
    await QuizCrud(session=session).delete_quiz(question_id=question_id)
