from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class FavoriteBase(BaseModel):
    post_id: int
    dir: bool = True

