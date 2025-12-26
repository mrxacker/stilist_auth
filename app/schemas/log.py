from pydantic import BaseModel


class LogRequest(BaseModel):
    user_id: int
    access_token: str
    action: str
    timestamp: str

class LogResponse(BaseModel):
    status: str