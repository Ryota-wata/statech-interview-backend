from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ここに許可するオリジンを指定することができます。
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可します。安全な設定に合わせて制限を追加してください。
    allow_headers=["*"],  # すべてのヘッダーを許可します。必要に応じて制限を設定してください。
)