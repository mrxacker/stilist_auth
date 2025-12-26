from pydantic import BaseModel


class LogRequest(BaseModel):
    user_id: int
    action: str
    timestamp: str

class LogResponse(BaseModel):
    status: str