from pydantic import BaseModel
from typing import Optional



class CheckResponse(BaseModel):
    url: str
    is_safe: bool
    categories: dict[str, bool]
    # Categories include:
    # - porn (includes adult)
    # - social
    # - gambling
    # - admalware
