"""Query dataclasses for People, Journalists, and Articles-by-entity search."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


def _omit_none(data: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}


def _join_list(value: str | list[str] | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, list):
        return ",".join(value)
    return value


@dataclass
class PeopleQuery:
    """People search (/v1/people/all) - resolve a public figure to a Wikidata ID."""

    name: str | None = None
    q: str | None = None
    size: int | None = None
    page: int | None = None
    show_num_results: bool | None = None

    def to_params(self) -> dict[str, Any]:
        raw = {
            "name": self.name,
            "q": self.q,
            "size": self.size,
            "page": self.page,
            "showNumResults": (
                str(self.show_num_results).lower()
                if self.show_num_results is not None
                else None
            ),
        }
        return _omit_none(raw)


@dataclass
class JournalistQuery:
    """Journalists search (/v1/journalists/all) - resolve a reporter to journalistId."""

    name: str | None = None
    q: str | None = None
    topic: str | list[str] | None = None
    category: str | list[str] | None = None
    source: str | list[str] | None = None
    country: str | list[str] | None = None
    label: str | list[str] | None = None
    min_monthly_posts: int | None = None
    max_monthly_posts: int | None = None
    size: int | None = None
    page: int | None = None
    show_num_results: bool | None = None

    def to_params(self) -> dict[str, Any]:
        raw = {
            "name": self.name,
            "q": self.q,
            "topic": _join_list(self.topic),
            "category": _join_list(self.category),
            "source": _join_list(self.source),
            "country": _join_list(self.country),
            "label": _join_list(self.label),
            "minMonthlyPosts": self.min_monthly_posts,
            "maxMonthlyPosts": self.max_monthly_posts,
            "size": self.size,
            "page": self.page,
            "showNumResults": (
                str(self.show_num_results).lower()
                if self.show_num_results is not None
                else None
            ),
        }
        return _omit_none(raw)


@dataclass
class ArticleByEntityQuery:
    """Articles (/v1/all) filtered by personWikidataId and/or journalistId."""

    person_wikidata_id: str | list[str] | None = None
    journalist_id: str | list[str] | None = None
    q: str | None = None
    from_: str | None = None  # maps to query param `from` (ISO date or datetime)
    to: str | None = None
    source: str | list[str] | None = None
    source_group: str | list[str] | None = None
    language: str | list[str] | None = None
    country: str | list[str] | None = None
    sort_by: str | None = None
    size: int | None = None
    page: int | None = None
    show_num_results: bool | None = None

    def to_params(self) -> dict[str, Any]:
        raw = {
            "personWikidataId": _join_list(self.person_wikidata_id),
            "journalistId": _join_list(self.journalist_id),
            "q": self.q,
            "from": self.from_,
            "to": self.to,
            "source": _join_list(self.source),
            "sourceGroup": _join_list(self.source_group),
            "language": _join_list(self.language),
            "country": _join_list(self.country),
            "sortBy": self.sort_by,
            "size": self.size,
            "page": self.page,
            "showNumResults": (
                str(self.show_num_results).lower()
                if self.show_num_results is not None
                else None
            ),
        }
        return _omit_none(raw)


@dataclass
class PersonHit:
    name: str | None = None
    wikidata_id: str | None = None
    description: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PersonHit:
        return cls(
            name=data.get("name"),
            wikidata_id=data.get("wikidataId"),
            description=data.get("description") or data.get("abstract"),
        )


@dataclass
class PeopleResults:
    num_results: int | None
    people: list[PersonHit]
    raw: dict[str, Any] = field(repr=False, default_factory=dict)

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> PeopleResults:
        rows = data.get("results") or data.get("people") or []
        return cls(
            num_results=data.get("numResults"),
            people=[PersonHit.from_dict(row) for row in rows],
            raw=data,
        )


@dataclass
class JournalistHit:
    name: str | None = None
    journalist_id: str | None = None
    title: str | None = None
    avg_monthly_posts: int | None = None
    top_sources: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> JournalistHit:
        sources = data.get("topSources") or []
        top: list[str] = []
        for item in sources[:3]:
            if isinstance(item, dict):
                name = item.get("name")
                if name:
                    top.append(str(name))
            elif item:
                top.append(str(item))
        return cls(
            name=data.get("name") or data.get("fullName"),
            journalist_id=data.get("id") or data.get("journalistId"),
            title=data.get("title") or data.get("headline"),
            avg_monthly_posts=data.get("avgMonthlyPosts"),
            top_sources=top,
        )


@dataclass
class JournalistResults:
    num_results: int | None
    journalists: list[JournalistHit]
    raw: dict[str, Any] = field(repr=False, default_factory=dict)

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> JournalistResults:
        rows = data.get("results") or data.get("journalists") or []
        return cls(
            num_results=data.get("numResults"),
            journalists=[JournalistHit.from_dict(row) for row in rows],
            raw=data,
        )


@dataclass
class ArticleHit:
    title: str | None = None
    url: str | None = None
    pub_date: str | None = None
    source: str | None = None
    authors_byline: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ArticleHit:
        source = data.get("source")
        if isinstance(source, dict):
            source_name = source.get("domain") or source.get("name")
        else:
            source_name = data.get("sourceByline") or data.get("publisherDomain")
        return cls(
            title=data.get("title"),
            url=data.get("url"),
            pub_date=data.get("pubDate") or data.get("addDate"),
            source=source_name,
            authors_byline=data.get("authorsByline"),
        )


@dataclass
class ArticleResults:
    num_results: int | None
    articles: list[ArticleHit]
    raw: dict[str, Any] = field(repr=False, default_factory=dict)

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> ArticleResults:
        rows = data.get("articles") or data.get("results") or []
        return cls(
            num_results=data.get("numResults"),
            articles=[ArticleHit.from_dict(row) for row in rows],
            raw=data,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "num_results": self.num_results,
            "articles": [asdict(a) for a in self.articles],
        }
