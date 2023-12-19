from sqlalchemy import select,insert
from sqlalchemy.orm import Session
import logging

# モデル
from api.models.quiz_result import QuizResultOrm


class ResultCrudRepository:
    """QuestionテーブルとChoiceテーブルへアクセス"""

    def __init__(self, session: Session) -> None:
        self.session = session

    async def register_result(self, user_id: str, corporate_id: int, quiz_result:bool) -> None:
        """クイズの合否の結果を保存

        保存処理のみをする

        Args:
            user_id(str): ユーザーID
            corporate_id(int): 会社ID
            quiz_result(bool): 合格か不合格かの真為値d

        """

        # 質問を取得
        quiz_result_data = {
            "user_id": user_id,
            "corporate_id": corporate_id,
            "passed": quiz_result,
        }

        stmt_insert = insert(QuizResultOrm).values(quiz_result_data)
        await self.session.execute(stmt_insert)
        await self.session.commit()

        return None
