from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class HeroStartingStats(BaseModel):
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


class HeroItemSlotInfoForTier(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    max_purchase_for_tier: list[int] = Field(
        ..., validation_alias="m_arMaxPurchasesForTier"
    )


class HeroItemSlotInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    weapon_mod: HeroItemSlotInfoForTier = Field(
        ..., validation_alias="EItemSlotType_WeaponMod"
    )
    armor: HeroItemSlotInfoForTier = Field(..., validation_alias="EItemSlotType_Armor")
    tech: HeroItemSlotInfoForTier = Field(..., validation_alias="EItemSlotType_Tech")


class HeroPurchaseBonusesModifier(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tier: int = Field(..., validation_alias="m_nTier")
    value: str = Field(..., validation_alias="m_strValue")
    value_type: str = Field(..., validation_alias="m_ValueType")


model_config = ConfigDict(populate_by_name=True)


class HeroPurchaseBonuses(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    weapon_mod: list[HeroPurchaseBonusesModifier] = Field(
        ..., validation_alias="EItemSlotType_WeaponMod"
    )
    armor: list[HeroPurchaseBonusesModifier] = Field(
        ..., validation_alias="EItemSlotType_Armor"
    )
    tech: list[HeroPurchaseBonusesModifier] = Field(
        ..., validation_alias="EItemSlotType_Tech"
    )


class HeroLevelInfoBonusCurrencies(StrEnum):
    AbilityUnlocks = "EAbilityUnlocks"
    EAbilityPoints = "EAbilityPoints"


class HeroLevelInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    required_gold: int | None = Field(None, validation_alias="m_unRequiredGold")
    bonus_currencies: dict[HeroLevelInfoBonusCurrencies, int] | None = Field(
        None, validation_alias="m_mapBonusCurrencies"
    )
    use_standard_upgrade: bool = Field(False, validation_alias="m_bUseStandardUpgrade")


class HeroImages(BaseModel):
    portrait: str
    card: str
    vertical: str
    mm: str
    sm: str
    gun: str

    def set_base_url(self, base_url: str):
        for attr, value in self.__dict__.items():
            setattr(self, attr, f"{base_url}{value}")


class Hero(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., validation_alias="m_HeroID")
    name: str = Field()
    images: HeroImages = Field()
    player_selectable: bool = Field(..., validation_alias="m_bPlayerSelectable")
    disabled: bool = Field(..., validation_alias="m_bPlayerSelectable")
    in_development: bool = Field(..., validation_alias="m_bDisabled")
    needs_testing: bool = Field(..., validation_alias="m_bInDevelopment")
    assigned_players_only: bool = Field(..., validation_alias="m_bNeedsTesting")
    bot_selectable: bool = Field(..., validation_alias="m_bAssignedPlayersOnly")
    limited_testing: bool = Field(..., validation_alias="m_bBotSelectable")
    complexity: int = Field(..., validation_alias="m_bLimitedTesting")
    readability: int = Field(..., validation_alias="m_nComplexity")
    starting_stats: HeroStartingStats = Field(
        ..., validation_alias="m_mapStartingStats"
    )
    collision_radius: float = Field(..., validation_alias="m_flCollisionRadius")
    collision_height: float = Field(..., validation_alias="m_flCollisionHeight")
    step_height: float = Field(..., validation_alias="m_flStepHeight")
    item_slot_info: HeroItemSlotInfo = Field(..., validation_alias="m_mapItemSlotInfo")
    purchase_bonuses: HeroPurchaseBonuses = Field(
        ..., validation_alias="m_mapPurchaseBonuses"
    )
    level_info: dict[int, HeroLevelInfo] = Field(..., validation_alias="m_mapLevelInfo")
    footstep_sounds: str = Field(..., validation_alias="m_hFootstepSounds")
    footstep_sound_event_default: str = Field(
        ..., validation_alias="m_strFootstepSoundEventDefault"
    )
    stealth_speed_meters_per_second: float = Field(
        ..., validation_alias="m_flStealthSpeedMetersPerSecond"
    )
    footstep_sound_travel_distance_meters: float = Field(
        ..., validation_alias="m_flFootstepSoundTravelDistanceMeters"
    )
    step_sound_time: float = Field(..., validation_alias="m_flStepSoundTime")
    color_ui: tuple[int, int, int] = Field(..., validation_alias="m_colorUI")
    color_glow_friendly: tuple[int, int, int] = Field(
        ..., validation_alias="m_colorGlowFriendly"
    )
    color_glow_enemy: tuple[int, int, int] = Field(
        ..., validation_alias="m_colorGlowEnemy"
    )
    color_glow_team1: tuple[int, int, int] = Field(
        ..., validation_alias="m_colorGlowTeam1"
    )
    color_glow_team2: tuple[int, int, int] = Field(
        ..., validation_alias="m_colorGlowTeam2"
    )
    standard_level_up_upgrades: dict[str, float] = Field(
        ..., validation_alias="m_mapStandardLevelUpUpgrades"
    )

    def set_base_url(self, base_url: str):
        self.images.set_base_url(base_url)
