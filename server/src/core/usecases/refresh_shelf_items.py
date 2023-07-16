import logging
from typing import Optional

from src.core.entities import Profile, Shelf, ShelfItem
from src.core.exceptions import ProfileNotFoundError
from src.core.gateways import IDataGateway
from src.core.repositories import IDataRepository

logger = logging.getLogger(__name__)


class RefreshShelfItemsUseCase:
    def __init__(self, gateway: IDataGateway, repository: IDataRepository) -> None:
        self._repository = repository
        self._gateway = gateway

    async def execute(self, shelf: Shelf) -> None:
        logger.info(f"Refreshing items on shelf {shelf.name}")

        async with self._repository.context():
            profile: Optional[Profile] = await self._repository.profile.read(
                uuid=shelf.profile_uuid
            )

            if not profile:
                raise ProfileNotFoundError(f"Profile {shelf.profile_uuid} not found.")

        async with self._gateway.context():
            remote_shelf_items: list[ShelfItem] = []
            fetch_results = self._gateway.shelf_item.fetch_for_profile_and_shelf(
                profile=profile,
                shelf=shelf,
            )
            async for shelf_item in fetch_results:
                if not shelf_item.book_editions:
                    book_editions = await self._gateway.book_edition.fetch_for_shelf_item(
                        shelf_item=shelf_item
                    )
                    if book_editions:
                        shelf_item.book_editions = book_editions

                if shelf_item.book_editions:
                    logger.info(
                        f"Found {len(shelf_item.book_editions)} editions"
                        f" for '{shelf_item.title}' by {shelf_item.author}"
                    )

                remote_shelf_items.append(shelf_item)

        if not remote_shelf_items:
            logger.info(f"No shelf items found on shelf {shelf.name}")
            return

        remote_shelf_items_len = len(remote_shelf_items)
        logger.info(f"Found {remote_shelf_items_len} shelf items on shelf {shelf.name}")

        remote_book_editions_len = sum(
            len(shelf_item.book_editions) for shelf_item in remote_shelf_items
        )
        logger.info(f"Found {remote_book_editions_len} book editions on shelf {shelf.name}")

        async with self._repository.context():
            await self._repository.shelf_item.sync_on_shelf(
                shelf=shelf,
                shelf_items=remote_shelf_items,
            )

            remote_book_editions = [
                book_edition
                for shelf_item in remote_shelf_items
                for book_edition in shelf_item.book_editions
            ]
            await self._repository.book_edition.sync_on_shelf(
                shelf=shelf,
                book_editions=remote_book_editions,
            )

        logger.info(f"Synchronized items on shelf {shelf.name}")
