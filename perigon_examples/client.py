"""HTTP client for the Perigon News API (raw requests, not the official SDK)."""

from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv

from .errors import AuthError, BadRequestError, PerigonError, RateLimitError

DEFAULT_BASE_URL = "https://api.perigon.io"


class PerigonClient:
    """Thin session wrapper: auth header, GET, status -> typed errors."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 60.0,
    ) -> None:
        load_dotenv()
        self.api_key = api_key or os.environ.get("PERIGON_API_KEY", "").strip()
        if not self.api_key:
            raise AuthError(
                "PERIGON_API_KEY is missing. Copy .env.example to .env and set your key."
            )
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "x-api-key": self.api_key,
                "Accept": "application/json",
                "User-Agent": "people-journalists-api-python-examples/1.0",
            }
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("GET", path, params=params)

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = self._session.request(
            method,
            url,
            params=params or {},
            timeout=self.timeout,
        )
        return self._parse(response)

    def _parse(self, response: requests.Response) -> dict[str, Any]:
        status = response.status_code
        text = response.text
        if status in (401, 403):
            raise AuthError(f"Authentication failed ({status})", status, text)
        if status == 429:
            raise RateLimitError("Rate limit exceeded (429)", status, text)
        if status == 400:
            raise BadRequestError(f"Bad request (400): {text[:300]}", status, text)
        if status >= 400:
            raise PerigonError(f"HTTP {status}: {text[:300]}", status, text)
        try:
            return response.json()
        except ValueError as exc:
            raise PerigonError(f"Non-JSON response: {text[:300]}", status, text) from exc

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> PerigonClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
