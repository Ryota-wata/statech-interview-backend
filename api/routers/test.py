from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}
