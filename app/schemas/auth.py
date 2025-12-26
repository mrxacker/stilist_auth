from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str
    admin_code: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    user_id: int
    token_type: str = "bearer"
