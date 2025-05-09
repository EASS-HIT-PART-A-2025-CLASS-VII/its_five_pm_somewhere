from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error_code: int
    message: str
