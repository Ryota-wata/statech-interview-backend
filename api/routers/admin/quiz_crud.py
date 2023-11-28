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
    # レスポンス用の空配列を用意
    all_quizzes = []

    # 質問一覧を取得
    stmt = select(QuestionOrm)
    result = await db.execute(stmt)
    questions = result.scalars().all()

    # 取得した各質問に対する選択肢を取得
    for question in questions:
      stmt = select(ChoiceOrm).where(ChoiceOrm.question_id == question.id)
      result = await db.execute(stmt)
      choices = result.scalars().all()

      # 取得した選択肢のうち1つ目を正解、2つ目を不正解とする。
      correct_choice = choices[0].text
      wrong_choice = choices[1].text

      quiz = QuizResponseModel(
            question_id=question.id,
            question_text=question.text,
            correct_choice=correct_choice,
            wrong_choice=wrong_choice,
            correct_answer=question.correct_answer
      )
      all_quizzes.append(quiz)
    
    return all_quizzes

@router.post("/admin/create-quiz/")
async def create_quiz(create_quiz: QuizRequestModel, db: AsyncSession = Depends(get_db)):
    """クイズを作成するエンドポイント

      【Request】
        question_text: 質問文,
        correct_choice: 正解選択肢,
        wrong_choice: 不正解選択肢,
        correct_answer: 正解

    """
    # 質問文を保存
    create_question = QuestionOrm(
        text=create_quiz.question_text,
        correct_answer=create_quiz.correct_answer,
    )
    db.add(create_question)

    # のちにcreate_question.idを取得するため
    await db.flush()

    # 正解選択肢を保存
    create_correct_choice = ChoiceOrm(
        text=create_quiz.correct_choice,
        question_id=create_question.id
    )
    db.add(create_correct_choice)

    # 不正解選択肢を保存
    create_wrong_choice = ChoiceOrm(
        text=create_quiz.wrong_choice,
        question_id=create_question.id
    )
    db.add(create_wrong_choice)
    await db.commit()


@router.put("/admin/update-quiz/{question_id}/")
async def update_quiz(question_id: int, update_quiz: QuizRequestModel, db: AsyncSession = Depends(get_db)):
    """クイズを編集するエンドポイント

      【Request】
        question_text: 質問文,
        correct_choice: 正解選択肢,
        wrong_choice: 不正解選択肢,
        correct_answer: 正解

    """
    # 質問文を更新
    update_question = (
       update(QuestionOrm)
       .where(QuestionOrm.id == question_id)
       .values(
          text=update_quiz.question_text,
          correct_answer=update_quiz.correct_answer
        )
    )
    await db.execute(update_question)

    # 指定の質問から2つの選択肢を取得
    stmt = select(ChoiceOrm).where(ChoiceOrm.question_id == question_id)
    result = await db.execute(stmt)
    update_choices = result.scalars().all()

    # 取得した2つの選択肢のうち1つ目を正解、2つ目を不正解の選択肢として更新
    update_choices[0].text = update_quiz.correct_choice
    update_choices[1].text = update_quiz.wrong_choice

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