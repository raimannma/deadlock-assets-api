from typing import Literal

from pydantic import ConfigDict, Field

from deadlock_assets_api.models.item import ItemSlotType
from deadlock_assets_api.models.v2.enums import ItemTier
from deadlock_assets_api.models.v2.raw_item_base import RawItemBase


class RawUpgrade(RawItemBase):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["upgrade"] = "upgrade"

    item_slot_type: ItemSlotType = Field(..., validation_alias="m_eItemSlotType")
    item_tier: ItemTier = Field(..., validation_alias="m_iItemTier")
    disabled: bool | None = Field(None, validation_alias="m_bDisabled")
