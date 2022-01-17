from src.core.entities import Profile, Shelf, ShelfItem, Book
from src.dataproviders.db import ProfileModel, ShelfItemModel, ShelfModel, LatestBookModel


def profile_from_model(model: ProfileModel) -> Profile:
    return Profile(name=model.name, value=model.value)


def shelf_from_model(model: ShelfModel) -> Shelf:
    return Shelf(
        profile_uuid=model.profile_uuid,
        name=model.name,
        value=model.value,
        pages=model.pages,
        refreshed_at=model.refreshed_at,
    )


def shelf_item_from_model(model: ShelfItemModel) -> ShelfItem:
    return ShelfItem(
        book_uuid=model.book_uuid,
        shelf_uuid=model.shelf_uuid,
        title=model.title,
        author=model.author,
        isbn=model.isbn,
        subtitle=model.subtitle,
        original_title=model.original_title,
        category=model.category,
        pages=model.pages,
        release=model.release,
    )


def latest_book_from_model(model: LatestBookModel) -> Book:
    return Book(
        title=model.title,
        author=model.author,
        isbn=model.isbn,
    )
