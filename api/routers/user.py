import os
import logging
import firebase_admin
import uuid
from dotenv import load_dotenv
from sqlalchemy import select
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from firebase_admin import auth, credentials
from api.models.user import UserOrm
from api.schemas.response_model.user import UserResponseModel
from api.db import get_db


router = APIRouter()

# サービスアカウントキーの情報を環境変数から取得
load_dotenv()

type = os.environ.get("TYPE")
project_id = os.environ.get("PROJECT_ID")
private_key_id = os.environ.get("PRIVATE_KEY_ID")
private_key = os.environ.get("PRIVATE_KEY")
client_email = os.environ.get("CLIENT_EMAIL")
client_id = os.environ.get("CLIENT_ID")
auth_uri = os.environ.get("AUTH_URI")
token_uri = os.environ.get("TOKEN_URI")
auth_provider_x509_cert_url = os.environ.get("AUTH_PROVIDER_X509_CERT_URL")
client_x509_cert_url = os.environ.get("CLIENT_X509_CERT_URL")
universe_domain = os.environ.get("UNIVERSE_DOMAIN")

# サービスアカウントキーの情報を辞書として作成
service_account_info = {
    "type": type,
    "project_id": project_id,
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri": auth_uri,
    "token_uri": token_uri,
    "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
    "client_x509_cert_url": client_x509_cert_url,
    "universe_domain": universe_domain
}

# Firebase Admin SDKの初期化
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

uuid = str(uuid.uuid4())

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

    stmt = select(UserOrm).where(UserOrm.email == email)
    result = await db.execute(stmt)
    user = result.scalars().one_or_none()

    if user is None:
        user = UserOrm(
            id=uuid, 
            name=name,
            email=email,
            admin_flag=False,
        )
        db.add(user)
        await db.commit() 

    return user

