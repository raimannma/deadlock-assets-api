from enum import Enum
from typing import Literal

from pydantic import ConfigDict, Field

from deadlock_assets_api.models.item import ItemSlotType
from deadlock_assets_api.models.v2.enums import ItemTier
from deadlock_assets_api.models.v2.raw_item_base import RawItemBase


class RawAbilityActivation(str, Enum):
    CITADEL_ABILITY_ACTIVATION_HOLD_TOGGLE = "hold_toggle"
    CITADEL_ABILITY_ACTIVATION_INSTANT_CAST = "instant_cast"
    CITADEL_ABILITY_ACTIVATION_ON_BUTTON_IS_DOWN = "on_button_is_down"
    CITADEL_ABILITY_ACTIVATION_PASSIVE = "passive"
    CITADEL_ABILITY_ACTIVATION_PRESS = "press"
    CITADEL_ABILITY_ACTIVATION_PRESS_TOGGLE = "press_toggle"

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if value in [member.value.lower(), member.name.lower()]:
                return member
        return None


class RawUpgrade(RawItemBase):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["upgrade"] = "upgrade"

    item_slot_type: ItemSlotType = Field(..., validation_alias="m_eItemSlotType")
    item_tier: ItemTier = Field(..., validation_alias="m_iItemTier")
    disabled: bool | None = Field(None, validation_alias="m_bDisabled")
    activation: RawAbilityActivation = Field(
        None, validation_alias="m_eAbilityActivation"
    )
