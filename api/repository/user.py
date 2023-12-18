import logging
import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

# モデル
from api.models.user import UserOrm

# スキーマ
from api.schemas.response_model.user import UserResponseModel

uuid = str(uuid.uuid4())

class UserRepository:
    """QuestionテーブルとChoiceテーブルへアクセス"""

    def __init__(self, session: Session) -> None:
        self.session = session

    async def auth_user(self, email: str, name: str) -> UserResponseModel:
        """ユーザー認証

        既存ユーザーでされば取得、新規であれば保存

        Args:
            auth_token(str): 認証トークン
        Returns:
            ユーザー情報

        """
        stmt = select(UserOrm).where(UserOrm.email == email)
        result = await self.session.execute(stmt)
        user = result.scalars().one_or_none()

        if user is None:
            user = UserOrm(
                id=uuid, 
                name=name,
                email=email,
                admin_flag=False,
            )
            self.session.add(user)
            await self.session.commit() 
        
        return user

