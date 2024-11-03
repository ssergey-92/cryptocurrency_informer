"""Module with schema for success response."""

from typing import Optional

from pydantic import BaseModel

class SuccessResponse(BaseModel):
    """Class for success response msg."""

    result: list[Optional[dict]]
