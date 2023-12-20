from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

# モデル
from api.models.question import QuestionOrm
from api.models.choice import ChoiceOrm

# スキーマ
from api.schemas.response_model.quiz_crud import QuizResponseModel


class QuizRepository:
    """QuestionテーブルとChoiceテーブルへアクセス"""

    def __init__(self, session: Session) -> None:
        self.session = session


    async def fetch_quizzes(self) -> list[QuizResponseModel]:
        """クイズを全て取得する"""

        # レスポンス用の空配列を用意
        all_quizzes = []

        # 質問一覧を取得
        stmt = select(QuestionOrm)
        result = await self.session.execute(stmt)
        questions = result.scalars().all()

        # 取得した各質問に対する選択肢を取得
        for question in questions:
          stmt = select(ChoiceOrm).where(ChoiceOrm.question_id == question.id)
          result = await self.session.execute(stmt)
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
    

    async def store_quiz(self, create_quiz):
        """クイズを作成する"""

        # 質問文を保存
        create_question = QuestionOrm(
            corporate_id=create_quiz.corporate_id,
            text=create_quiz.question_text,
            correct_answer=create_quiz.correct_answer,
        )
        self.session.add(create_question)

        # のちにcreate_question.idを取得するため
        await self.session.flush()

        # 正解選択肢を保存
        create_correct_choice = ChoiceOrm(
            text=create_quiz.correct_choice,
            question_id=create_question.id
        )
        self.session.add(create_correct_choice)

        # 不正解選択肢を保存
        create_wrong_choice = ChoiceOrm(
            text=create_quiz.wrong_choice,
            question_id=create_question.id
        )
        self.session.add(create_wrong_choice)
        await self.session.commit()

        return create_quiz
    

    async def update_quiz(self, question_id, update_quiz):
        """クイズを編集する"""

        # 質問文を更新
        update_question = (
          update(QuestionOrm)
          .where(QuestionOrm.id == question_id)
          .values(
              corporate_id=update_quiz.corporate_id,
              text=update_quiz.question_text,
              correct_answer=update_quiz.correct_answer
            )
        )
        await self.session.execute(update_question)

        # 指定の質問から2つの選択肢を取得
        stmt = select(ChoiceOrm).where(ChoiceOrm.question_id == question_id)
        result = await self.session.execute(stmt)
        update_choices = result.scalars().all()

        # 取得した2つの選択肢のうち1つ目を正解、2つ目を不正解の選択肢として更新
        update_choices[0].text = update_quiz.correct_choice
        update_choices[1].text = update_quiz.wrong_choice

        await self.session.commit()

        return update_quiz
    
    
    async def delete_quiz(self, question_id):
        """クイズを削除する"""

        delete_choice = (
            delete(ChoiceOrm)
            .where(ChoiceOrm.question_id == question_id)
        )
        await self.session.execute(delete_choice)
        await self.session.commit()

        delete_question = (
          delete(QuestionOrm)
          .where(QuestionOrm.id == question_id)
        )
        await self.session.execute(delete_question)
        await self.session.commit()
