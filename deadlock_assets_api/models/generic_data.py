import os
from functools import lru_cache

from pydantic import BaseModel, ConfigDict, Field


class FlashData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    duration: float = Field(..., validation_alias="m_flDuration")
    coverage: float = Field(..., validation_alias="m_flCoverage")
    hardness: float = Field(..., validation_alias="m_flHardness")
    brightness: float = Field(..., validation_alias="m_flBrightness")
    color: list[int] = Field(..., validation_alias="m_Color")
    brightness_in_light_sensitivity_mode: float | None = Field(
        None, validation_alias="m_flBrightnessInLightSensitivityMode"
    )


class DamageFlash(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    bullet_damage: FlashData = Field(..., validation_alias="EFlashType_BulletDamage")
    tech_damage: FlashData = Field(..., validation_alias="EFlashType_TechDamage")
    healing_damage: FlashData = Field(..., validation_alias="EFlashType_Healing")
    crit_damage: FlashData = Field(..., validation_alias="EFlashType_CritDamage")
    melee_damage: FlashData = Field(..., validation_alias="EFlashType_MeleeActivate")


class GlitchSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    strength: float = Field(..., validation_alias="m_flStrength")
    uantize_type: float = Field(..., validation_alias="m_nQuantizeType")
    quantize_scale: float = Field(..., validation_alias="m_flQuantizeScale")
    quantize_strength: float = Field(..., validation_alias="m_flQuantizeStrength")
    frame_rate: float = Field(..., validation_alias="m_flFrameRate")
    speed: float = Field(..., validation_alias="m_flSpeed")
    jump_strength: float = Field(..., validation_alias="m_flJumpStrength")
    distort_strength: float = Field(..., validation_alias="m_flDistortStrength")
    white_noise_strength: float = Field(..., validation_alias="m_flWhiteNoiseStrength")
    scanline_strength: float = Field(..., validation_alias="m_flScanlineStrength")
    breakup_strength: float = Field(..., validation_alias="m_flBreakupStrength")


class NewPlayerMetrics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    skill_tier_name: str = Field(..., validation_alias="m_strSkillTierName")
    net_worth: int = Field(..., validation_alias="m_NetWorth")
    damage_taken: int = Field(..., validation_alias="m_DamageTaken")
    boss_damage: int = Field(..., validation_alias="m_BossDamage")
    player_damage: int = Field(..., validation_alias="m_PlayerDamage")
    last_hits: int = Field(..., validation_alias="m_LastHits")
    orbs_secured: int = Field(..., validation_alias="m_OrbsSecured")
    orbs_denied: int = Field(..., validation_alias="m_OrbsDenied")
    abilities_upgraded: int = Field(..., validation_alias="m_AbilitiesUpgraded")
    mods_purchased: int = Field(..., validation_alias="m_ModsPurchased")


class GenericData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    damage_flash: DamageFlash = Field(..., validation_alias="m_mapDamageFlash")
    glitch_settings: GlitchSettings = Field(..., validation_alias="m_GlitchSettings")
    new_player_metrics: list[NewPlayerMetrics] = Field(
        ..., validation_alias="m_NewPlayerMetrics"
    )
    item_price_per_tier: list[int] = Field(..., validation_alias="m_nItemPricePerTier")


@lru_cache
def load_generic_data() -> GenericData | None:
    if not os.path.exists("res/generic_data.json"):
        return None
    with open("res/generic_data.json") as f:
        return GenericData.model_validate_json(f.read())
