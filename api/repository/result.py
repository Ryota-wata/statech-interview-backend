from sqlalchemy import select,insert,desc
from sqlalchemy.orm import Session
import logging
from typing import List

# スキーマ
from api.schemas.response_model.result import ResultResponseModel

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

        # 結果データ
        quiz_result_data = {
            "user_id": user_id,
            "corporate_id": corporate_id,
            "passed": quiz_result,
        }

        stmt_insert = insert(QuizResultOrm).values(quiz_result_data)
        await self.session.execute(stmt_insert)
        await self.session.commit()

        return None
    
    async def get_result(self, user_id: str) -> List[ResultResponseModel]:
        """クイズの合否の結果を保存

        保存処理のみをする

        Args:
            user_id(str): ユーザーID

        Returns:
            ResultResponseModel: ユーザーの合否結果を受験日降順で取得

        """

        # ユーザーの合否結果を受験日降順で取得
        result = (
            await self.session.execute(
                select(QuizResultOrm)
                .where(QuizResultOrm.user_id == user_id)
                .order_by(desc(QuizResultOrm.created_at)) 
            )
        ).all()

        self.session.commit()

        result_list = []

        for row in result:
            result_model = ResultResponseModel(
                id=row[0].id,
                user_id=row[0].user_id,
                corporate_id=row[0].corporate_id,
                passed=row[0].passed,
                created_at=row[0].created_at,
            )
            result_list.append(result_model)

        return result_list
