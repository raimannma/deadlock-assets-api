from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from deadlock_assets_api.models.v2.enums import AbilityType
from deadlock_assets_api.models.v2.raw_item_base import RawItemBase


class RawAbilityUpgradePropertyUpgrade(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., validation_alias="m_strPropertyName")
    bonus: str | float = Field(..., validation_alias="m_strBonus")
    scale_stat_filter: str | None = Field(None, validation_alias="m_eScaleStatFilter")
    upgrade_type: str | None = Field(None, validation_alias="m_eUpgradeType")


class RawAbilityUpgrade(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    property_upgrades: list[RawAbilityUpgradePropertyUpgrade] = Field(
        ..., validation_alias="m_vecPropertyUpgrades"
    )


class RawAbility(RawItemBase):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["ability"] = "ability"
    behaviour_bits: str | None = Field(None, validation_alias="m_AbilityBehaviorsBits")
    upgrades: list[RawAbilityUpgrade] | None = Field(
        None, validation_alias="m_vecAbilityUpgrades"
    )
    ability_type: AbilityType | None = Field(None, validation_alias="m_eAbilityType")
    dependant_abilities: list[str] | None = Field(
        None, validation_alias="m_vecDependentAbilities"
    )
