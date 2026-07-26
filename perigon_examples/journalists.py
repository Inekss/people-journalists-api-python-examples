"""Journalists search endpoint (/v1/journalists/all)."""

from __future__ import annotations

from .client import PerigonClient
from .queries import JournalistQuery, JournalistResults


class Endpoint:
    path: str = ""

    def __init__(self, client: PerigonClient) -> None:
        self.client = client


class JournalistsEndpoint(Endpoint):
    """GET journalist profiles; keep id for Articles journalistId filters."""

    path = "/v1/journalists/all"

    def search(self, query: JournalistQuery) -> JournalistResults:
        data = self.client.get(self.path, params=query.to_params())
        return JournalistResults.from_response(data)
