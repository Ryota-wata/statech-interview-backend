from sqlalchemy import and_, delete, literal, select, update
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.choice import ChoiceOrm
from api.models.question import QuestionOrm
from api.schemas.request_model.quiz_crud import QuizRequestModel
from api.schemas.response_model.quiz_crud import QuizResponseModel
from api.db import get_db


router = APIRouter()

@router.get("/admin/quizzes/")
async def get_quizzes(db: AsyncSession = Depends(get_db)) -> list[QuizResponseModel]:
    """クイズ一覧を取得するエンドポイント
    
      【QuizResponseModel】
        question_id: 質問ID,
        question_text: 質問文,
        correct_choice: 正解選択肢,
        wrong_choice: 不正解選択肢,
        correct_answer: 正解,
    
    """
    stmt = select(
        QuestionOrm.id,
        QuestionOrm.text,
        ChoiceOrm.text.label("choice"),
        QuestionOrm.correct_answer
    ).join(ChoiceOrm, ChoiceOrm.question_id == QuestionOrm.id)
    result = await db.execute(stmt)
    quizzes = result.all()

    return [
        QuizResponseModel(
            question_id=quiz.id,
            question_text=quiz.text,
            correct_choice=quiz.choice,
            wrong_choice=quiz.choice,
            correct_answer=quiz.correct_answer
        )
        for quiz in quizzes
    ]


@router.post("/admin/create-quiz/")
async def create_quiz(create_quiz: QuizRequestModel, db: AsyncSession = Depends(get_db)):
    """クイズを作成するエンドポイント

      【Request】
        question_text: 質問文,
        correct_answer: 正解,
        choice_texts: 選択肢 = []

    """
    create_question = QuestionOrm(
        text=create_quiz.question_text,
        correct_answer=create_quiz.correct_answer,
    )
    db.add(create_question)
    await db.commit()

    # コミット後にcreate_questionのidが取得できる
    await db.refresh(create_question)

    for choice_text in create_quiz.choice_texts:
      create_choice = ChoiceOrm(
          text=choice_text,
          question_id=create_question.id
      )
      db.add(create_choice)
    await db.commit()


@router.put("/admin/update-quiz/{question_id}/")
async def update_quiz(question_id: int, update_quiz: QuizRequestModel, db: AsyncSession = Depends(get_db)):
    """クイズを編集するエンドポイント

      【Request】
        question_id: 質問ID,
        question_text: 質問文,
        correct_answer: 正解,
        choice_texts: 選択肢 = []

    """
    update_question = (
       update(QuestionOrm)
       .where(QuestionOrm.id == question_id)
       .values(
          text=update_quiz.question_text,
          correct_answer=update_quiz.correct_answer
        )
    )
    await db.execute(update_question)
    await db.commit()

    for choice_text in update_quiz.choice_texts:
      update_choice = (
          update(ChoiceOrm)
          .where(ChoiceOrm.question_id == question_id)
          .values(
            text=choice_text, 
          )
      )
      await db.execute(update_choice)
    await db.commit()


@router.delete("/admin/delete-quiz/{question_id}/")
async def update_quiz(question_id: int, db: AsyncSession = Depends(get_db)):
    """クイズを削除するエンドポイント"""
    delete_choice = (
        delete(ChoiceOrm)
        .where(ChoiceOrm.question_id == question_id)
    )
    await db.execute(delete_choice)
    await db.commit()

    delete_question = (
       delete(QuestionOrm)
       .where(QuestionOrm.id == question_id)
    )
    await db.execute(delete_question)
    await db.commit()