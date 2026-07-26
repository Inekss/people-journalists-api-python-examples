"""Articles search endpoint (/v1/all) for entity ID filters."""

from __future__ import annotations

from .client import PerigonClient
from .queries import ArticleByEntityQuery, ArticleResults


class Endpoint:
    path: str = ""

    def __init__(self, client: PerigonClient) -> None:
        self.client = client


class ArticlesEndpoint(Endpoint):
    """GET article search scoped by personWikidataId and/or journalistId."""

    path = "/v1/all"

    def search(self, query: ArticleByEntityQuery) -> ArticleResults:
        data = self.client.get(self.path, params=query.to_params())
        return ArticleResults.from_response(data)
