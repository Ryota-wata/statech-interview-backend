import os
import logging
import firebase_admin
import uuid
from dotenv import load_dotenv
from sqlalchemy import select,insert
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from firebase_admin import auth, credentials
from api.models.user import UserOrm
from api.models.question import QuestionOrm
from api.models.quiz_result import QuizResultOrm
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

# # Firebase Admin SDKの初期化
# cred = credentials.Certificate(service_account_info)
# firebase_admin.initialize_app(cred)

uuid = str(uuid.uuid4())

#TODO 返り値の型指定
@router.post("/result")
async def login_user(request: Request, db: AsyncSession = Depends(get_db)):
    # リクエストから質問IDと合否を取得
    data = await request.json()
    question_id = data.get("question_id")
    quiz_result = data.get("result")

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
        return "合否は保存しない"
    
    email = claims["email"]
    stmt = select(UserOrm).where(UserOrm.email == email)
    result = await db.execute(stmt)
    user = result.scalars().one_or_none()

    # 質問の corporate_id を取得
    stmt_question = (
        select(QuestionOrm.corporate_id)
        .where(QuestionOrm.id == question_id)
    )
    result_question = await db.execute(stmt_question)
    corporate_id = result_question.scalar()

    # QuizResultOrm にデータを挿入
    quiz_result_data = {
        "user_id": user.id,
        "corporate_id": corporate_id,
        "passed": quiz_result,
    }

    stmt_insert = insert(QuizResultOrm).values(quiz_result_data)
    await db.execute(stmt_insert)
    await db.commit()

    return "処理完了"

