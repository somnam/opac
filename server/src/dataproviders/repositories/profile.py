from typing import List, Optional

from src.core.entities import Profile
from src.core.repositories import ProfileRepositoryInterface
from src.dataproviders.repositories.base import BaseDbRepository
from src.dataproviders.db import ProfileModel


class ProfileRepository(ProfileRepositoryInterface, BaseDbRepository):
    def exists(self, profile_id: str) -> bool:
        exists = self._dbh.session.query(ProfileModel._pk).filter_by(profile_id=profile_id).exists()
        result: bool = self._dbh.session.query(exists).scalar()
        return result

    def create(self, profile: Profile) -> Profile:
        self._dbh.session.add(ProfileModel(**profile.to_dict()))
        return profile

    def create_all(self, profiles: List[Profile]) -> None:
        if not profiles:
            return

        self._dbh.session.bulk_save_objects([
            ProfileModel(**profile.to_dict())
            for profile in profiles
        ])

    def update_all(self, profiles: List[Profile]) -> None:
        ...

    def delete_all(self, profiles: List[Profile]) -> None:
        ...

    def read(self, profile_id: str) -> Optional[Profile]:
        model = self._dbh.session.query(*ProfileModel.columns())\
            .filter_by(profile_id=profile_id)\
            .one_or_none()

        return Profile(name=model.name, value=model.value) if model else None

    def read_all(self) -> List[Profile]:
        return [
            Profile(name=row.name, value=row.value)
            for row in self._dbh.session.query(*ProfileModel.columns())
        ]
