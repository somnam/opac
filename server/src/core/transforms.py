import re
from typing import List
from uuid import UUID

from src.core.entities import Catalog, Profile, ProfileSearchParams, Shelf, ShelfSearchParams


def payload_to_catalog(payload: dict) -> Catalog:
    result = re.search(r"^([^\(]+)\s\(([^\)]+)\)$", payload["name"])

    if result:
        name, city = result.groups()
    else:
        name, city = "", ""

    return Catalog(name=name, city=city, value=payload["value"])


def payload_to_profile(payload: dict) -> Profile:
    return Profile(
        name=payload["name"],
        value=payload["value"],
    )


def payload_to_shelf(payload: dict) -> Shelf:
    return Shelf(
        profile_uuid=UUID(payload["profile_uuid"]),
        name=payload["name"],
        value=payload["value"],
        pages=payload["pages"],
    )


def payload_to_shelves(payload: list) -> List[Shelf]:
    return [payload_to_shelf(item) for item in payload]


def payload_to_shelf_search_params(payload: dict) -> ShelfSearchParams:
    return ShelfSearchParams(
        profile_uuid=UUID(payload["profile_uuid"]),
        phrase=payload.get("phrase", None),
        page=payload.get("page", 1),
    )


def payload_to_profile_search_params(payload: dict) -> ProfileSearchParams:
    return ProfileSearchParams(
        phrase=payload["phrase"],
        page=payload.get("page", 1),
    )
