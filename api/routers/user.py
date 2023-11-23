import logging
from sqlalchemy import select
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from firebase_admin import auth
from api.models.user import UserOrm
from api.schemas.response_model.user import UserResponseModel
from api.db import get_db


router = APIRouter()

@router.post("/login", response_model=UserResponseModel)
async def login_user(request: Request, db: AsyncSession = Depends(get_db)):
    """ログインするエンドポイント
    
    【Response】
        id: ユーザーid
        name: ユーザー名
        email: メールアドレス
        admin_flag: 管理者フラグ

    """

    #TODO リファクタ必須です
    # Firebase Admin SDKによりIDトークンを確認
    authorization = request.headers.get("Authorization")
    if authorization is None:
        logging.error(f"認証トークンが存在しません: {e}")
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split(" ")[-1].strip()
    try:
        claims = auth.verify_id_token(token)
    except Exception as e:
        logging.error(f"不正な認証トークンです: {e}")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    email = claims["email"]
    name = claims["name"]
    
    user = db.scalars(
        (select(UserOrm).with_for_update().where(UserOrm.email == email))
    ).one_or_none()

    if user is None:
        user = UserOrm(
            name=name,
            email=email,
        )
        db.add(user)
        db.flush()

    return user

