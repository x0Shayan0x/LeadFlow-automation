import re
from datetime import datetime
from typing import Literal
from urllib.parse import urlparse
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


LeadSource = Literal[
    "website",
    "form",
    "api",
    "facebook_ads",
    "extension",
    "playwright",
    "manual",
]


class LeadUpsert(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=3, max_length=254)
    company: str = Field(min_length=1, max_length=150)
    role: str | None = Field(default=None, max_length=150)
    website: str | None = Field(default=None, max_length=2048)
    source: LeadSource
    notes: str | None = Field(default=None, max_length=2000)
    workflow_execution_id: str | None = Field(default=None, max_length=64)

    @field_validator(
        "full_name",
        "email",
        "company",
        "role",
        "website",
        "notes",
        "workflow_execution_id",
        mode="before",
    )
    @classmethod
    def strip_strings(cls, value: object) -> object:
        if isinstance(value, str):
            stripped_value = value.strip()
            return stripped_value or None

        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        normalized_email = value.lower()

        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if re.fullmatch(email_pattern, normalized_email) is None:
            raise ValueError("Email must have a valid format.")

        return normalized_email

    @field_validator("source", mode="before")
    @classmethod
    def normalize_source(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().lower()

        return value

    @field_validator("website")
    @classmethod
    def validate_website(cls, value: str | None) -> str | None:
        if value is None:
            return None

        parsed_url = urlparse(value)

        if parsed_url.scheme not in {"http", "https"}:
            raise ValueError("Website must use HTTP or HTTPS.")

        if not parsed_url.netloc:
            raise ValueError("Website must be a valid URL.")

        return value


class LeadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    email: str
    company: str
    role: str | None
    website: str | None
    source: str
    notes: str | None
    status: str
    workflow_execution_id: str | None
    score: int | None
    temperature: str | None
    occurrence_count: int
    created_at: datetime
    updated_at: datetime
    last_received_at: datetime


class LeadUpsertResponse(BaseModel):
    operation: Literal["created", "updated"]
    lead: LeadRead
