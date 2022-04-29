from fastapi import APIRouter

from src.entrypoint import post, user

api_router = APIRouter()
api_router.include_router(post.router, prefix="/posts", tags=["post"])
api_router.include_router(user.router, prefix="/users", tags=["user"])
