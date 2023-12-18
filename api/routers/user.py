import logging
from sqlalchemy import select
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.user import UserOrm
from api.schemas.response_model.user import UserResponseModel
from api.db import get_db

# use_caseクラス
from api.use_cases.user import Login


router = APIRouter()

@router.post("/login", response_model=UserResponseModel)
async def login(request: Request, session: AsyncSession = Depends(get_db)):
    """ログインするエンドポイント
    
    【Response】
        id: ユーザーid
        name: ユーザー名
        email: メールアドレス
        admin_flag: 管理者フラグ

    """
    auth_token = request.headers.get("Authorization")
    if auth_token is None:
        logging.error(f"認証トークンが存在しません: {e}")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # use_case層のメソッド呼び出し
    user = await Login(session=session).login(auth_token=auth_token)

    return user

