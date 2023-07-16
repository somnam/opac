from src.core.entities.profile import Profile
from src.dataproviders.db.model.profile import ProfileModel
from src.dataproviders.repositories.entity import EntityRepository


class ProfileRepository(EntityRepository[Profile, ProfileModel]):
    def __init__(self) -> None:
        super().__init__(entity=Profile, model=ProfileModel)

    def to_entity(self, model: ProfileModel) -> Profile:
        return Profile(name=model.name, value=model.value)
