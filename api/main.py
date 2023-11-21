from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from api.routers import quiz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ここに許可するオリジンを指定することができます。
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可します。安全な設定に合わせて制限を追加してください。
    allow_headers=["*"],  # すべてのヘッダーを許可します。必要に応じて制限を設定してください。
)

router = APIRouter()
app.include_router(quiz.router)
