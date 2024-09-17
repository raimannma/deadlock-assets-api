import json
import os
from enum import StrEnum

from murmurhash2.murmurhash2 import murmurhash2
from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator

from deadlock_assets_api.models import utils
from deadlock_assets_api.models.languages import Language


class ItemInfoProperty(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    value: str | int | float | None = Field(None, validation_alias="m_strValue")
    disable_value: str | None = Field(None, validation_alias="m_strDisableValue")
    can_set_token_override: bool | None = Field(
        None, validation_alias="m_bCanSetTokenOverride"
    )


class ItemInfoWeaponInfoBulletSpeedCurveSpline(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    x: float
    y: float
    slope_incoming: float = Field(..., validation_alias="m_flSlopeIncoming")
    slope_outgoing: float = Field(..., validation_alias="m_flSlopeOutgoing")


class ItemInfoWeaponInfoBulletSpeedCurveTangents(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    incoming_tangent: str = Field(..., validation_alias="m_nIncomingTangent")
    outgoing_tangent: str = Field(..., validation_alias="m_nOutgoingTangent")


class ItemInfoWeaponInfoBulletSpeedCurve(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    spline: list[ItemInfoWeaponInfoBulletSpeedCurveSpline] = Field(
        ..., validation_alias="m_spline"
    )
    tangents: list[ItemInfoWeaponInfoBulletSpeedCurveTangents] = Field(
        ..., validation_alias="m_tangents"
    )
    domain_mins: list[float] = Field(..., validation_alias="m_vDomainMins")
    domain_maxs: list[float] = Field(..., validation_alias="m_vDomainMaxs")


class ItemInfoWeaponInfoRecoil(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    range: list[float] | float = Field(..., validation_alias="m_Range")
    burst_slope: float | None = Field(None, validation_alias="m_flBurstSlope")
    burst_exponent: float | None = Field(None, validation_alias="m_flBurstExponent")
    burst_constant: float | None = Field(None, validation_alias="m_flBurstConstant")


class ItemInfoWeaponInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    spread: float | None = Field(None, validation_alias="m_Spread")
    standing_spread: float | None = Field(None, validation_alias="m_StandingSpread")
    scatter_yaw_scale: float | None = Field(
        None, validation_alias="m_flScatterYawScale"
    )
    shooting_up_spread_penalty: float | None = Field(
        None, validation_alias="m_flShootingUpSpreadPenalty"
    )
    zoom_move_speed_percent: float | None = Field(
        None, validation_alias="m_flZoomMoveSpeedPercent"
    )
    shoot_move_speed_percent: float | None = Field(
        None, validation_alias="m_flShootMoveSpeedPercent"
    )
    horizontal_punch: float | None = Field(None, validation_alias="m_flHorizontalPunch")
    vertical_punch: float | None = Field(None, validation_alias="m_flVerticalPunch")
    recoil_recovery_speed: float | None = Field(
        None, validation_alias="m_flRecoilRecoverySpeed"
    )
    vertical_recoil: ItemInfoWeaponInfoRecoil | None = Field(
        None, validation_alias="m_VerticallRecoil"
    )
    horizontal_recoil: ItemInfoWeaponInfoRecoil | None = Field(
        None, validation_alias="m_HorizontalRecoil"
    )
    recoil_speed: float | None = Field(None, validation_alias="m_flRecoilSpeed")
    zoom_fov: float | None = Field(None, validation_alias="m_flZoomFOV")
    damage_falloff_start_range: float | None = Field(
        None, validation_alias="m_flDamageFalloffStartRange"
    )
    damage_falloff_end_range: float | None = Field(
        None, validation_alias="m_flDamageFalloffEndRange"
    )
    range: float | None = Field(None, validation_alias="m_flRange")
    bullet_lifetime: float | None = Field(None, validation_alias="m_flBulletLifetime")
    damage_falloff_start_scale: float | None = Field(
        None, validation_alias="m_flDamageFalloffStartScale"
    )
    damage_falloff_end_scale: float | None = Field(
        None, validation_alias="m_flDamageFalloffEndScale"
    )
    damage_falloff_bias: float | None = Field(
        None, validation_alias="m_flDamageFalloffBias"
    )
    bullets: int | None = Field(None, validation_alias="m_iBullets")
    cycle_time: float | None = Field(None, validation_alias="m_flCycleTime")
    reload_duration: float | None = Field(None, validation_alias="m_reloadDuration")
    clip_size: int | None = Field(None, validation_alias="m_iClipSize")
    burst_shot_count: int | None = Field(None, validation_alias="m_iBurstShotCount")
    burst_shot_cooldown: float | None = Field(
        None, validation_alias="m_flBurstShotCooldown"
    )
    bullet_gravity_scale: float | None = Field(
        None, validation_alias="m_flBulletGravityScale"
    )
    bullet_radius: float | None = Field(None, validation_alias="m_flBulletRadius")
    bullet_reflect_scale: float | None = Field(
        None, validation_alias="m_flBulletReflectScale"
    )
    bullet_reflect_amount: float | None = Field(
        None, validation_alias="m_flBulletReflectAmount"
    )
    bullet_inherit_shooter_velocity_scale: float | None = Field(
        None, validation_alias="m_flBulletInheritShooterVelocityScale"
    )
    bullet_whiz_distance: float | None = Field(
        None, validation_alias="m_flBulletWhizDistance"
    )
    crit_bonus_start: float | None = Field(None, validation_alias="m_flCritBonusStart")
    crit_bonus_end: float | None = Field(None, validation_alias="m_flCritBonusEnd")
    crit_bonus_start_range: float | None = Field(
        None, validation_alias="m_flCritBonusStartRange"
    )
    crit_bonus_end_range: float | None = Field(
        None, validation_alias="m_flCritBonusEndRange"
    )
    crit_bonus_against_npcs: float | None = Field(
        None, validation_alias="m_flCritBonusAgainstNPCs"
    )
    shoot_spread_penalty_per_shot: float | None = Field(
        None, validation_alias="m_flShootSpreadPenaltyPerShot"
    )
    shoot_spread_penalty_decay_delay: float | None = Field(
        None, validation_alias="m_flShootSpreadPenaltyDecayDelay"
    )
    shoot_spread_penalty_decay: float | None = Field(
        None, validation_alias="m_flShootSpreadPenaltyDecay"
    )
    recoil_shot_index_recovery_time_factor: float | None = Field(
        None, validation_alias="m_flRecoilShotIndexRecoveryTimeFactor"
    )
    can_zoom: bool | None = Field(None, validation_alias="m_bCanZoom")
    reload_move_speed: float | None = Field(None, validation_alias="ReloadMoveSpeed")
    auto_replenish_clip: float | None = Field(
        None, validation_alias="m_flAutoReplenishClip"
    )
    penetration_percent: float | None = Field(
        None, validation_alias="m_flPenetrationPercent"
    )
    npc_aiming_spread: float | list[float] | None = Field(
        None, validation_alias="m_NpcAimingSpread"
    )
    bullet_damage: float | None = Field(None, validation_alias="m_flBulletDamage")


class ItemDofWhileZoomed(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    dof_near_crisp: float = Field(..., validation_alias="m_flDofNearCrisp")
    dof_far_crisp: float = Field(..., validation_alias="m_flDofFarCrisp")
    dof_far_blurry: float = Field(..., validation_alias="m_flDofFarBlurry")


class ItemType(StrEnum):
    WEAPON = "weapon"
    ABILITY = "ability"
    UPGRADE = "upgrade"

    @classmethod
    def _missing_(cls, value: str):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None


class Item(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    class_name: str = Field()
    image: str | None = Field(None, validation_alias="m_strComponentImage")
    properties: dict[str, ItemInfoProperty | str | float] | None = Field(
        None, validation_alias="m_mapComponentProperties"
    )
    weapon_info: ItemInfoWeaponInfo | None = Field(
        None, validation_alias="m_WeaponInfo"
    )
    start_trained: bool | None = Field(None, validation_alias="m_bStartTrained")
    dof_while_zoomed: ItemDofWhileZoomed | None = Field(
        None, validation_alias="m_DOFWhileZoomed"
    )
    points_cost: int | None = Field(None, validation_alias="m_nComponentPointsCost")
    unlocks_cost: int | None = Field(
        None, validation_alias="m_nAbillityUnlocksCost"
    )  # typo in the original data
    max_level: int | None = Field(None, validation_alias="m_iMaxLevel")
    language: Language = Field(Language.English, exclude=True)

    @computed_field
    @property
    def id(self) -> int:
        return murmurhash2(self.class_name.encode(), 0x31415926)

    @computed_field
    @property
    def type(self) -> ItemType | None:
        name = utils.strip_prefix(self.class_name, "citadel_")
        first_word = name.split("_")[0]
        try:
            return ItemType(first_word.capitalize())
        except ValueError:
            return None

    @field_validator("properties")
    @classmethod
    def validate_properties(cls, value: dict[str, ItemInfoProperty], _):
        if value is None or len(value) == 0:
            return None
        properties = dict()
        for k, v in value.items():
            k = utils.camel_to_snake(k)
            if isinstance(v, ItemInfoProperty):
                properties[k] = float(v.value) if utils.is_float(v.value) else v.value
            else:
                properties[k] = v
        return properties

    def model_post_init(self, __context):
        if self.image:
            split_index = self.image.find("abilities/")
            if split_index == -1:
                split_index = self.image.find("upgrades/")
            self.image = (
                ("images/" + self.image[split_index:])
                .replace('"', "")
                .replace(".psd", "_psd.png")
            )

    def set_base_url(self, base_url: str):
        if self.image:
            self.image = f"{base_url}{self.image}"

    @computed_field
    @property
    def name(self) -> str:
        file = f"res/localization/citadel_gc_{self.language.value}.json"
        if not os.path.exists(file):
            file = f"res/localization/citadel_gc_english.json"
            if not os.path.exists(file):
                return self.class_name

        with open(file) as f:
            language_data = json.load(f)["lang"]["Tokens"]
        name = language_data.get(self.class_name, None)
        if name is not None:
            return name
        if self.language == Language.English:
            return self.class_name
        file = f"res/localization/citadel_gc_english.json"
        with open(file) as f:
            language_data = json.load(f)["lang"]["Tokens"]
        return language_data.get(self.class_name, None)
