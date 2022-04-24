from fastapi import APIRouter

from src.entrypoint import post, user

api_router = APIRouter()
api_router.include_router(post.router, prefix="/post", tags=["post"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
