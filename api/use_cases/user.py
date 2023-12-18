import os
import logging
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import auth, credentials
from fastapi import HTTPException

from sqlalchemy.orm.session import Session

# スキーマ
from api.schemas.response_model.user import UserResponseModel

# use_case基底クラス
from api.use_cases.base import UseCaseBaseModel

# repositoryクラス
from api.repository.user import UserRepository

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

class Login(UseCaseBaseModel):
    def __init__(self, session: Session):
        self.session = session

    async def login(self, auth_token: str) -> UserResponseModel:
        """ログイン処理

        既存ユーザーでされば取得、新規であれば保存

        """
        token = auth_token.split(" ")[-1].strip()
        try:
            claims = auth.verify_id_token(token)
        except Exception as e:
            logging.error(f"不正な認証トークンです: {e}")
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        email = claims["email"]
        name = claims["name"]

        auth_user = await UserRepository(session=self.session).auth_user(email=email, name=name)

        logging.warning("ユーザー%s", auth_user)
        
        return auth_user
