from uuid import UUID
from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, ConfigDict


class ChatMessageCreate(BaseModel):
    message: str


class ChatMessageResponse(BaseModel):
    chat_id: UUID
    user_id: UUID
    sender: str  # "User" or "Assistant"
    message: str
    chat_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
