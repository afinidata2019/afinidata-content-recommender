from datetime import datetime

from pydantic import BaseModel


class Article(BaseModel):
    id: int
    name: str
    content: str
    text_content: str
    min: int
    max: int
    preview: str
    thumbnail: str
    created_at: datetime
    updated_at: datetime
    status: str
    is_opened: bool
    metric: float
