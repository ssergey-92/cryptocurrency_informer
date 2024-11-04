"""Module with schema for response with error msg."""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Class to validate response body with error message."""

    error: str
