from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.chat import ChatHistory
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse
from app.api.v1.endpoints.auth import get_current_user
from app.core.logging import logger

router = APIRouter()

DISCLAIMER_TEXT = "\n\n*Educational Disclaimer: This AI response is provided strictly for educational purposes and general wellness information. It is not medical advice, diagnosis, or prescription. Please consult a qualified healthcare professional for medical concerns.*"


@router.post("/message", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
def send_chat_message(
    message_in: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sends a user health assistant query and receives an educational response with disclaimers."""
    logger.info(f"Chat query from user {current_user.user_id}: {message_in.message}")
    
    # Store user query
    user_chat = ChatHistory(
        user_id=current_user.user_id,
        sender="User",
        message=message_in.message
    )
    db.add(user_chat)
    db.commit()

    # Formulate assistant answer (Placeholder engine for Phase 4)
    assistant_reply = (
        f"Thank you for your question regarding: '{message_in.message}'. "
        f"I can help explain medical terms, laboratory reference ranges, and general health guidelines."
        f"{DISCLAIMER_TEXT}"
    )

    assistant_chat = ChatHistory(
        user_id=current_user.user_id,
        sender="Assistant",
        message=assistant_reply,
        chat_metadata={"disclaimer_included": True}
    )
    db.add(assistant_chat)
    db.commit()
    db.refresh(assistant_chat)

    return assistant_chat


@router.get("/history", response_model=List[ChatMessageResponse])
def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves conversation history for the authenticated user."""
    return db.query(ChatHistory).filter(ChatHistory.user_id == current_user.user_id).order_by(ChatHistory.created_at.asc()).all()
