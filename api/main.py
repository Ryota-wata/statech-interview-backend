from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from api.routers.admin import quiz_crud
from api.routers import quiz, user, result

load_dotenv()

app = FastAPI()

api_base_url = os.getenv("API_PRODUCTION_URL", default="http://localhost:8000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ここに許可するオリジンを指定することができます。
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可します。安全な設定に合わせて制限を追加してください。
    allow_headers=["*"],  # すべてのヘッダーを許可します。必要に応じて制限を設定してください。
)

router = APIRouter()
app.include_router(quiz.router)
app.include_router(quiz_crud.router)
app.include_router(user.router)
app.include_router(result.router)
