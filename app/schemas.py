from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CreateSessionResponse(BaseModel):
    session_id: int


class MessageRequest(BaseModel):
    session_id: int
    text: str = Field(min_length=1, max_length=2000)


class MessageResponse(BaseModel):
    sender: str
    text: str
    sent_at: datetime


class HistoryResponse(BaseModel):
    session_id: int
    messages: List[MessageResponse]


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
