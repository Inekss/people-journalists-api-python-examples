"""Public exports for the example package."""

from .articles import ArticlesEndpoint
from .client import PerigonClient
from .errors import AuthError, BadRequestError, PerigonError, RateLimitError
from .examples import ResolveJournalistExample, ResolvePersonExample
from .journalists import JournalistsEndpoint
from .people import PeopleEndpoint
from .queries import ArticleByEntityQuery, JournalistQuery, PeopleQuery

__all__ = [
    "ArticlesEndpoint",
    "ArticleByEntityQuery",
    "AuthError",
    "BadRequestError",
    "JournalistQuery",
    "JournalistsEndpoint",
    "PeopleEndpoint",
    "PeopleQuery",
    "PerigonClient",
    "PerigonError",
    "RateLimitError",
    "ResolveJournalistExample",
    "ResolvePersonExample",
]
