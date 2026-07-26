"""People search endpoint (/v1/people/all)."""

from __future__ import annotations

from .client import PerigonClient
from .queries import PeopleQuery, PeopleResults


class Endpoint:
    path: str = ""

    def __init__(self, client: PerigonClient) -> None:
        self.client = client


class PeopleEndpoint(Endpoint):
    """GET people profiles; keep wikidataId for Articles personWikidataId filters."""

    path = "/v1/people/all"

    def search(self, query: PeopleQuery) -> PeopleResults:
        data = self.client.get(self.path, params=query.to_params())
        return PeopleResults.from_response(data)
