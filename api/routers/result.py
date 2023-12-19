import logging
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import get_db

# use_caseクラス
from api.use_cases.user import Login
from api.use_cases.quiz import ConvertQuestionIdToQuestionInfo
from api.use_cases.result import CrudReslut


router = APIRouter()

#TODO 返り値の型指定
@router.post("/result")
async def login_user(request: Request, session: AsyncSession = Depends(get_db)):
    # リクエストからトークン、質問ID、合否情報を取得
    auth_token = request.headers.get("Authorization")
    data = await request.json()
    question_id = data.get("question_id")
    quiz_result = data.get("result")

    # 認証ユーザー情報取得
    if auth_token is None:
        logging.error(f"認証トークンが存在しません: {e}")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # ユーザーid を取得
    user = await Login(session=session).login(auth_token=auth_token)
    user_id = user.id

    # 質問の会社を取得
    question_info = await ConvertQuestionIdToQuestionInfo(session=session).convert_question_id_to_question_info(question_id=question_id)
    corporate_id = question_info.corporate_id

    # クイズの結果 を保存
    await CrudReslut(session=session).register_reslut(user_id=user_id, corporate_id=corporate_id, quiz_result=quiz_result)

    return "処理完了"

