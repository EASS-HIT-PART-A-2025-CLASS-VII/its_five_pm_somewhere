from pydantic import BaseModel


class ImageSearchRequest(BaseModel):
    name: str
    count: int  # Number of images per page
    page: int  # Page number for pagination
