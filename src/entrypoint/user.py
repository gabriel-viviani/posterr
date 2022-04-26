from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.service import user as user_service
from src.repository.database import get_db
from src.dto.user import UserDto


router = APIRouter()

@router.get("/{user_id}", status.HTTP_200_OK, response_model=UserDto)
def get_user(db: Session = Depends(get_db)) -> UserDto:
    
