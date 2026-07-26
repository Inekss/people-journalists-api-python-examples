"""Runnable examples: resolve People / Journalists, then filter Articles by ID."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from .articles import ArticlesEndpoint
from .client import PerigonClient
from .journalists import JournalistsEndpoint
from .people import PeopleEndpoint
from .queries import ArticleByEntityQuery, JournalistQuery, PeopleQuery


def _window_days(days: int = 30) -> tuple[str, str]:
    end = date.today()
    start = end - timedelta(days=days)
    return start.isoformat(), end.isoformat()


class ResolvePersonExample:
    """People name lookup -> store wikidataId -> Articles with personWikidataId."""

    def __init__(self, client: PerigonClient) -> None:
        self.people = PeopleEndpoint(client)
        self.articles = ArticlesEndpoint(client)

    def run(self, name: str = "Satya Nadella") -> dict[str, Any]:
        people_query = PeopleQuery(name=name, size=5, show_num_results=True)
        people = self.people.search(people_query)
        if not people.people:
            return {
                "example": "resolve_person",
                "lookup_params": people_query.to_params(),
                "error": f"No people matched name={name!r}",
            }

        person = people.people[0]
        wikidata_id = person.wikidata_id
        if not wikidata_id:
            return {
                "example": "resolve_person",
                "lookup_params": people_query.to_params(),
                "error": "Top match had no wikidataId",
                "person": {"name": person.name},
            }

        start, end = _window_days(30)
        article_query = ArticleByEntityQuery(
            person_wikidata_id=wikidata_id,
            from_=start,
            to=end,
            size=3,
            sort_by="date",
            show_num_results=True,
        )
        articles = self.articles.search(article_query)
        return {
            "example": "resolve_person",
            "lookup_params": people_query.to_params(),
            "person": {
                "name": person.name,
                "wikidata_id": wikidata_id,
                "description": (person.description or "")[:160],
            },
            "article_params": article_query.to_params(),
            "num_results": articles.num_results,
            "articles": [
                {
                    "title": hit.title,
                    "source": hit.source,
                    "pub_date": hit.pub_date,
                    "url": hit.url,
                }
                for hit in articles.articles
            ],
        }


class ResolveJournalistExample:
    """Journalist name lookup -> store journalistId -> Articles with journalistId."""

    def __init__(self, client: PerigonClient) -> None:
        self.journalists = JournalistsEndpoint(client)
        self.articles = ArticlesEndpoint(client)

    def run(self, name: str = "Maggie Haberman") -> dict[str, Any]:
        journalist_query = JournalistQuery(name=name, size=5, show_num_results=True)
        journalists = self.journalists.search(journalist_query)
        if not journalists.journalists:
            return {
                "example": "resolve_journalist",
                "lookup_params": journalist_query.to_params(),
                "error": f"No journalists matched name={name!r}",
            }

        reporter = journalists.journalists[0]
        journalist_id = reporter.journalist_id
        if not journalist_id:
            return {
                "example": "resolve_journalist",
                "lookup_params": journalist_query.to_params(),
                "error": "Top match had no id",
                "journalist": {"name": reporter.name},
            }

        start, end = _window_days(30)
        article_query = ArticleByEntityQuery(
            journalist_id=journalist_id,
            from_=start,
            to=end,
            size=3,
            sort_by="date",
            show_num_results=True,
        )
        articles = self.articles.search(article_query)
        return {
            "example": "resolve_journalist",
            "lookup_params": journalist_query.to_params(),
            "journalist": {
                "name": reporter.name,
                "journalist_id": journalist_id,
                "title": reporter.title,
                "avg_monthly_posts": reporter.avg_monthly_posts,
                "top_sources": reporter.top_sources,
            },
            "article_params": article_query.to_params(),
            "num_results": articles.num_results,
            "articles": [
                {
                    "title": hit.title,
                    "source": hit.source,
                    "authors_byline": hit.authors_byline,
                    "pub_date": hit.pub_date,
                    "url": hit.url,
                }
                for hit in articles.articles
            ],
        }
