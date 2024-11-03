"""Module with schema for success response."""

from typing import Optional

from pydantic import BaseModel

class SuccessResponse(BaseModel):
    # TODO add documentaion

    result: list[Optional[dict]]
