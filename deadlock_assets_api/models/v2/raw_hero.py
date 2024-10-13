import json

from pydantic import BaseModel, ConfigDict, Field

from deadlock_assets_api.models.hero import HeroItemType
from deadlock_assets_api.models.item import ItemSlotType


class RawHeroStartingStats(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    max_move_speed: float = Field(..., validation_alias="EMaxMoveSpeed")
    sprint_speed: float = Field(..., validation_alias="ESprintSpeed")
    crouch_speed: float = Field(..., validation_alias="ECrouchSpeed")
    move_acceleration: float = Field(..., validation_alias="EMoveAcceleration")
    light_melee_damage: int = Field(..., validation_alias="ELightMeleeDamage")
    heavy_melee_damage: int = Field(..., validation_alias="EHeavyMeleeDamage")
    max_health: int = Field(..., validation_alias="EMaxHealth")
    weapon_power: int = Field(..., validation_alias="EWeaponPower")
    reload_speed: int = Field(..., validation_alias="EReloadSpeed")
    weapon_power_scale: int = Field(..., validation_alias="EWeaponPowerScale")
    proc_build_up_rate_scale: int = Field(..., validation_alias="EProcBuildUpRateScale")
    stamina: int = Field(..., validation_alias="EStamina")
    base_health_regen: float = Field(..., validation_alias="EBaseHealthRegen")
    stamina_regen_per_second: float = Field(
        ..., validation_alias="EStaminaRegenPerSecond"
    )
    ability_resource_max: int = Field(..., validation_alias="EAbilityResourceMax")
    ability_resource_regen_per_second: int = Field(
        ..., validation_alias="EAbilityResourceRegenPerSecond"
    )
    crit_damage_received_scale: float = Field(
        ..., validation_alias="ECritDamageReceivedScale"
    )
    tech_duration: int = Field(..., validation_alias="ETechDuration")
    tech_range: int = Field(..., validation_alias="ETechRange")
    bullet_armor_damage_reduction: float | None = Field(
        None, validation_alias="EBulletArmorDamageReduction"
    )


class RawHeroShopSpiritStatsDisplay(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    display_stats: list[str] = Field(..., validation_alias="m_vecDisplayStats")


class RawHeroShopVitalityStatsDisplay(RawHeroShopSpiritStatsDisplay):
    model_config = ConfigDict(populate_by_name=True)

    other_display_stats: list[str] = Field(
        ..., validation_alias="m_vecOtherDisplayStats"
    )


class RawHeroShopWeaponStatsDisplay(RawHeroShopVitalityStatsDisplay):
    model_config = ConfigDict(populate_by_name=True)

    weapon_attributes: str | None = Field(None, validation_alias="m_eWeaponAttributes")
    weapon_image: str | None = Field(None, validation_alias="m_strWeaponImage")


class RawHeroShopStatDisplay(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    spirit_stats_display: RawHeroShopSpiritStatsDisplay = Field(
        ..., validation_alias="m_eSpiritStatsDisplay"
    )
    vitality_stats_display: RawHeroShopVitalityStatsDisplay = Field(
        ..., validation_alias="m_eVitalityStatsDisplay"
    )
    weapon_stats_display: RawHeroShopWeaponStatsDisplay = Field(
        ..., validation_alias="m_eWeaponStatsDisplay"
    )


class RawHeroStatsDisplay(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    health_header_stats: list[str] = Field(
        ..., validation_alias="m_vecHealthHeaderStats"
    )
    health_stats: list[str] = Field(..., validation_alias="m_vecHealthHeaderStats")
    magic_header_stats: list[str] = Field(..., validation_alias="m_vecMagicHeaderStats")
    magic_stats: list[str] = Field(..., validation_alias="m_vecMagicStats")
    weapon_header_stats: list[str] = Field(
        ..., validation_alias="m_vecWeaponHeaderStats"
    )
    weapon_stats: list[str] = Field(..., validation_alias="m_vecWeaponStats")


class RawHeroStatsUIDisplay(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    category: str = Field(..., validation_alias="m_eStatCategory")
    stat_type: str = Field(..., validation_alias="m_eStatType")


class RawHeroStatsUI(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    weapon_stat_display: str = Field(..., validation_alias="m_eWeaponStatDisplay")
    display_stats: list[RawHeroStatsUIDisplay] = Field(
        ..., validation_alias="m_vecDisplayStats"
    )


class RawHeroItemSlotInfoValue(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    max_purchases_for_tier: list[int] = Field(
        ..., validation_alias="m_arMaxPurchasesForTier"
    )


class RawHeroLevelInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    use_standard_upgrade: bool | None = Field(
        None, validation_alias="m_bUseStandardUpgrade"
    )
    bonus_currencies: dict[str, int] | None = Field(
        None, validation_alias="m_mapBonusCurrencies"
    )
    required_gold: int = Field(..., validation_alias="m_unRequiredGold")


class RawHeroPurchaseBonus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    value_type: str = Field(..., validation_alias="m_ValueType")
    tier: int = Field(..., validation_alias="m_nTier")
    value: str = Field(..., validation_alias="m_strValue")


class RawHeroScalingStat(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    scaling_stat: str = Field(..., validation_alias="eScalingStat")
    scale: float = Field(..., validation_alias="flScale")


class RawHero(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., validation_alias="m_HeroID")
    class_name: str
    recommended_upgrades: list[str] | None = Field(
        None, validation_alias="m_RecommendedUpgrades"
    )
    player_selectable: bool = Field(..., validation_alias="m_bPlayerSelectable")
    bot_selectable: bool = Field(..., validation_alias="m_bBotSelectable")
    disabled: bool = Field(..., validation_alias="m_bDisabled")
    in_development: bool = Field(..., validation_alias="m_bInDevelopment")
    needs_testing: bool = Field(..., validation_alias="m_bNeedsTesting")
    assigned_players_only: bool = Field(..., validation_alias="m_bAssignedPlayersOnly")
    limited_testing: bool = Field(..., validation_alias="m_bLimitedTesting")
    complexity: int = Field(..., validation_alias="m_nComplexity")
    skin: int = Field(..., validation_alias="m_nModelSkin")
    readability: int = Field(..., validation_alias="m_nReadability")
    starting_stats: RawHeroStartingStats = Field(
        ..., validation_alias="m_mapStartingStats"
    )
    icon_hero_card: str | None = Field(None, validation_alias="m_strIconHeroCard")
    icon_image_small: str | None = Field(None, validation_alias="m_strIconImageSmall")
    minimap_image: str | None = Field(None, validation_alias="m_strMinimapImage")
    selection_image: str | None = Field(None, validation_alias="m_strSelectionImage")
    top_bar_image: str | None = Field(None, validation_alias="m_strTopBarImage")
    top_bar_vertical_image: str | None = Field(
        None, validation_alias="m_strTopBarVertical"
    )
    shop_stat_display: RawHeroShopStatDisplay = Field(
        ..., validation_alias="m_ShopStatDisplay"
    )
    color_glow_enemy: tuple[int, int, int] = Field(
        ..., validation_alias="m_colorGlowEnemy"
    )
    color_glow_friendly: tuple[int, int, int] = Field(
        ..., validation_alias="m_colorGlowFriendly"
    )
    color_glow_team1: tuple[int, int, int] = Field(
        ..., validation_alias="m_colorGlowTeam1"
    )
    color_glow_team2: tuple[int, int, int] = Field(
        ..., validation_alias="m_colorGlowTeam2"
    )
    color_ui: tuple[int, int, int] = Field(..., validation_alias="m_colorUI")
    collision_height: float = Field(..., validation_alias="m_flCollisionHeight")
    collision_radius: float = Field(..., validation_alias="m_flCollisionRadius")
    footstep_sound_travel_distance_meters: float = Field(
        ..., validation_alias="m_flFootstepSoundTravelDistanceMeters"
    )
    stealth_speed_meters_per_second: float = Field(
        ..., validation_alias="m_flStealthSpeedMetersPerSecond"
    )
    step_height: float = Field(..., validation_alias="m_flStepHeight")
    step_sound_time: float = Field(..., validation_alias="m_flStepSoundTime")
    step_sound_time_sprinting: float | None = Field(
        None, validation_alias="m_flStepSoundTimeSprinting"
    )
    stats_display: RawHeroStatsDisplay = Field(
        ..., validation_alias="m_heroStatsDisplay"
    )
    hero_stats_ui: RawHeroStatsUI = Field(..., validation_alias="m_heroStatsUI")
    items: dict[HeroItemType, str] = Field(..., validation_alias="m_mapBoundAbilities")
    item_slot_info: dict[ItemSlotType, RawHeroItemSlotInfoValue] = Field(
        ..., validation_alias="m_mapItemSlotInfo"
    )
    level_info: dict[str, RawHeroLevelInfo] = Field(
        ..., validation_alias="m_mapLevelInfo"
    )
    purchase_bonuses: dict[ItemSlotType, list[RawHeroPurchaseBonus]] = Field(
        ..., validation_alias="m_mapPurchaseBonuses"
    )
    scaling_stats: dict[str, RawHeroScalingStat] = Field(
        ..., validation_alias="m_mapScalingStats"
    )
    standard_level_up_upgrades: dict[str, float] = Field(
        ..., validation_alias="m_mapStandardLevelUpUpgrades"
    )


def test_parse():
    with open("res/raw_heroes.json") as f:
        raw_heroes = json.load(f)
    raw_heroes = [
        RawHero(class_name=k, **v)
        for k, v in raw_heroes.items()
        if k.startswith("hero_")
        and "base" not in k
        and "generic" not in k
        and "dummy" not in k
    ]
    print(raw_heroes)


if __name__ == "__main__":
    test_parse()
