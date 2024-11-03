"""Module with schemas for validation cryptocurrency price period params."""

from datetime import datetime, date
from os import getenv
from re import match

from pydantic import BaseModel, field_validator, model_validator


class DatesPeriod(BaseModel):
    """Class validation cryptocurrency price period params."""

    start_date: str
    end_date: str


    @field_validator("start_date")
    @classmethod
    def validate_start_date(cls, start_date: str) -> str:
        """Check that start date has supported format and valid."""

        if not cls._is_supported_date_format(start_date):
            raise ValueError(
                f"Use start date format as following: 31-12-2023!"
            )
        elif not cls._is_valid_date(start_date):
            raise ValueError(
                f"Start date must be valid and less or equal to current date!"
            )

        return start_date

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, end_date: str) -> str:
        """Check that end date has supported format and valid."""

        if not cls._is_supported_date_format(end_date):
            raise ValueError(
                f"Use end date format as following: 31-12-2023!"
            )
        elif not cls._is_valid_date(end_date):
            raise ValueError(
                f"End date must be valid and less or equal to current date!"
            )

        return end_date

    @model_validator(mode="after")
    def validate(self) -> "DatesPeriod":
        """Check that start date is less or equal end date."""

        if (
                datetime.strptime(self.start_date, getenv("DATE_FORMAT")) <=
                datetime.strptime(self.end_date, getenv("DATE_FORMAT"))
        ):
            return self

        raise ValueError("Start date should be less or equal to end date!")

    @classmethod
    def _is_supported_date_format(cls, date: str) -> bool:
        """Check that date has supported format."""

        date_pattern = r'{}'.format(getenv("DATE_FORMAT_PATTERN"))
        if match(date_pattern, date):
            return True

        return False

    @classmethod
    def _is_valid_date(cls, check_date: str) -> bool:
        """Check if date is existed in calendar."""

        try:
            check_date = datetime.strptime(check_date, getenv("DATE_FORMAT"))
            if check_date.date() <= date.today():
                return True

            return False
        except ValueError as exc:
            return False
