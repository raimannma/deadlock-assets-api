from typing import Literal

from pydantic import ConfigDict, computed_field

from deadlock_assets_api.models.item import ItemSlotType
from deadlock_assets_api.models.v2.api_item_base import ItemBase
from deadlock_assets_api.models.v2.enums import ItemTier
from deadlock_assets_api.models.v2.raw_hero import RawHero
from deadlock_assets_api.models.v2.raw_upgrade import RawUpgrade


class Upgrade(ItemBase):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["upgrade"] = "upgrade"

    item_slot_type: ItemSlotType
    item_tier: ItemTier
    disabled: bool | None

    @computed_field
    @property
    def shopable(self) -> bool:
        return (
            (self.disabled is None or self.disabled is False)
            and self.item_slot_type
            in [
                ItemSlotType.EItemSlotType_Armor,
                ItemSlotType.EItemSlotType_WeaponMod,
                ItemSlotType.EItemSlotType_Tech,
            ]
            and self.image is not None
        )

    @classmethod
    def from_raw_item(
        cls,
        raw_upgrade: RawUpgrade,
        raw_heroes: list[RawHero],
        localization: dict[str, str],
    ) -> "Upgrade":
        raw_model = super().from_raw_item(raw_upgrade, raw_heroes, localization)
        return cls(**raw_model)
