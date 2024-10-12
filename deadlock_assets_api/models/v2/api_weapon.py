from typing import Literal

from pydantic import ConfigDict

from deadlock_assets_api.models.v2.api_item_base import ItemBase
from deadlock_assets_api.models.v2.raw_hero import RawHero
from deadlock_assets_api.models.v2.raw_weapon import RawWeapon, RawWeaponInfo


class Weapon(ItemBase):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["weapon"] = "weapon"

    weapon_info: RawWeaponInfo

    @classmethod
    def from_raw_item(
        cls,
        raw_weapon: RawWeapon,
        raw_heroes: list[RawHero],
        localization: dict[str, str],
    ) -> "Weapon":
        raw_model = super().from_raw_item(raw_weapon, raw_heroes, localization)
        return cls(**raw_model)
