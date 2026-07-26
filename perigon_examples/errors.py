"""Typed exceptions for Perigon HTTP responses."""

from __future__ import annotations


class PerigonError(Exception):
    """Base error for any non-success Perigon response."""

    def __init__(self, message: str, status_code: int | None = None, body: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class AuthError(PerigonError):
    """401 / 403 - missing, invalid, or insufficient API key."""


class RateLimitError(PerigonError):
    """429 - too many requests; back off and retry."""


class BadRequestError(PerigonError):
    """400 - invalid parameters or malformed body."""
