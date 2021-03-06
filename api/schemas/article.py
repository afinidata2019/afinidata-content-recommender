from datetime import datetime
from typing import Optional

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
    type: Optional[str]
    is_opened: bool
    metric: Optional[float]
    in_weeks: bool
