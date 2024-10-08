import os
from enum import StrEnum
from functools import lru_cache
from logging import warning

from murmurhash2.murmurhash2 import murmurhash2
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    TypeAdapter,
    computed_field,
    field_serializer,
    field_validator,
)

import deadlock_assets_api.models.generic_data
from deadlock_assets_api import utils
from deadlock_assets_api.glob import IMAGE_BASE_URL, VIDEO_BASE_URL
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


class ItemSlotType(StrEnum):
    EItemSlotType_WeaponMod = "weapon"
    EItemSlotType_Tech = "spirit"
    EItemSlotType_Armor = "vitality"

    @classmethod
    def _missing_(cls, new_value: str):
        new_value = new_value.lower()
        for member in cls:
            if member.name.lower() == new_value or member.value.lower() == new_value:
                return member
        warning(f"Unknown ItemSlotType: {new_value}")
        return None


class ItemType(StrEnum):
    WEAPON = "weapon"
    ABILITY = "ability"
    UPGRADE = "upgrade"
    TECH = "tech"
    ARMOR = "armor"

    @classmethod
    def _missing_(cls, value: str):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        hero_list = [
            "astro",
            "atlas",
            "bebop",
            "bomber",
            "cadence",
            "chrono",
            "dynamo",
            "forge",
            "ghost",
            "gigawatt",
            "gunslinger",
            "haze",
            "hornet",
            "inferno",
            "kali",
            "kelvin",
            "krill",
            "lash",
            "mirage",
            "nano",
            "orion",
            "rutger",
            "shiv",
            "slork",
            "synth",
            "tengu",
            "thumper",
            "tokamak",
            "viscous",
            "warden",
            "wraith",
            "wrecker",
            "yakuza",
            "yamato",
        ]
        if value.strip() in hero_list:
            return cls.ABILITY
        warning(f"Unknown ItemType: {value}")
        return None


class Item(BaseModel):
    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    name: str | None = Field(None)
    description: str | None = Field(None)
    class_name: str = Field()
    shopable: bool | None = Field(None)
    disabled: bool | None = Field(None, validation_alias="m_bDisabled")
    in_development: bool | None = Field(None, validation_alias="m_bInDevelopment")
    start_trained: bool | None = Field(None, validation_alias="m_bStartTrained")
    image: str | None = Field(None, validation_alias="m_strAbilityImage")
    video: str | None = Field(None, validation_alias="m_strMoviePreviewPath")
    properties: dict[str, ItemInfoProperty | str | float | None] | None = Field(
        None, validation_alias="m_mapAbilityProperties"
    )
    weapon_info: ItemInfoWeaponInfo | None = Field(
        None, validation_alias="m_WeaponInfo"
    )
    ability_upgrades: list[dict[str, str | float | list]] | None = Field(
        None, validation_alias="m_vecAbilityUpgrades"
    )
    dof_while_zoomed: ItemDofWhileZoomed | None = Field(
        None, validation_alias="m_DOFWhileZoomed"
    )
    points_cost: int | None = Field(None, validation_alias="m_nAbilityPointsCost")
    unlocks_cost: int | None = Field(
        None, validation_alias="m_nAbillityUnlocksCost"
    )  # typo in the original data
    max_level: int | None = Field(None, validation_alias="m_iMaxLevel")
    tier: str | int | None = Field(None, validation_alias="m_iItemTier")
    item_slot_type: ItemSlotType | None = Field(
        None, validation_alias="m_eItemSlotType"
    )
    child_items: list[str] | list[int] | None = Field(
        None, validation_alias="m_vecComponentItems"
    )

    @field_serializer("item_slot_type")
    def serialize_group(self, group: ItemSlotType | str, _info):
        if group is None or isinstance(group, str):
            return group
        return group.name

    @computed_field
    @property
    def id(self) -> int:
        return murmurhash2(self.class_name.encode(), 0x31415926)

    @computed_field
    @property
    def video_mp4_h264(self) -> str | None:
        if self.video is None:
            return None
        return self.video.replace(".webm", "_h264.mp4")

    @computed_field
    @property
    def type(self) -> ItemType | None:
        name = utils.strip_prefix(self.class_name, "citadel_")
        first_word = name.split("_")[0]
        try:
            return ItemType(first_word.capitalize())
        except ValueError:
            return None

    @field_validator("tier")
    @classmethod
    def validate_tier(cls, value: str | int | None, _):
        if value is None:
            return None
        if isinstance(value, int):
            return value
        return int(value[-1])

    @field_validator("disabled")
    @classmethod
    def validate_disabled(cls, value: str | int | None, _) -> bool | None:
        if value is None:
            return None
        if isinstance(value, int):
            return bool(value)
        if value.lower() in ["true", "1"]:
            return True
        if value.lower() in ["false", "0"]:
            return False
        return None

    @computed_field
    @property
    def cost(self) -> int | None:
        if self.tier is None:
            return None
        generic_data = deadlock_assets_api.models.generic_data.load_generic_data()
        return generic_data.item_price_per_tier[self.tier]

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

    @field_validator("ability_upgrades")
    @classmethod
    def validate_ability_upgrades(
        cls,
        value: (
            list[dict[str, str | float]] | list[dict[str, list[dict[str, str | float]]]]
        ),
        _,
    ) -> list[dict[str, str | float]] | None:
        if value is None or len(value) == 0:
            return None
        ability_upgrades = []
        for tier_upgrades in value:
            if any(isinstance(i, (str, float)) for i in tier_upgrades.values()):
                return value
            upgrades = [i for n in tier_upgrades.values() for i in n]
            ability_upgrades.extend(
                {
                    u["m_strPropertyName"]: (
                        float(u["m_strBonus"])
                        if utils.is_float(u["m_strBonus"])
                        else u["m_strBonus"]
                    )
                }
                for u in upgrades
            )
        return ability_upgrades

    def model_post_init(self, __context):
        self.name = self.get_name(Language.English)
        if self.image:
            split_index = self.image.find("abilities/")
            if split_index == -1:
                split_index = self.image.find("upgrades/")
            if split_index == -1:
                split_index = self.image.find("hud/")
            self.image = f"{IMAGE_BASE_URL}/{self.image[split_index:]}"
            if self.image.endswith(".png") and not self.image.endswith("_psd.png"):
                self.image = self.image.replace(".png", "_psd.png")
            else:
                self.image = self.image.replace(".psd", "_psd.png")
            self.image = self.image.replace('"', "")
        if self.video and "videos/" in self.video:
            self.video = f"{VIDEO_BASE_URL}/{self.video.split('videos/')[-1]}"

    def set_language(self, language: Language):
        self.name = self.get_name(language)
        self.description = self.get_description(language)

    def set_shopable(self, heroes: list):
        self.shopable = self.id in shopable_item_ids(heroes)

    def get_name(self, language: Language) -> str:
        return utils.get_translation(self.class_name, language)

    def get_description(self, language: Language) -> str:
        return utils.get_translation(f"{self.class_name}_desc", language, True)

    def postfix(self, items: list["Item"]):
        if self.child_items is None:
            return
        self.child_items = [
            s
            for s in (
                next((item.id for item in items if item.class_name == child_item), None)
                for child_item in self.child_items
                if self.class_name != child_item
            )
            if s is not None
        ]


@lru_cache
def load_items() -> list[Item] | None:
    if not os.path.exists("res/items.json"):
        return None
    with open("res/items.json") as f:
        content = f.read()
    ta = TypeAdapter(list[Item])
    return ta.validate_json(content)


@lru_cache
def shopable_item_ids(heroes: list) -> set[int]:
    hero_weapons = set()
    for h in heroes:
        hero_weapons.add(h.items["weapon_melee"])
        hero_weapons.add(h.items["weapon_primary"])
    return {
        i.id
        for i in load_items()
        if (i.disabled is None or i.disabled is False)
        and i.id not in hero_weapons
        and i.type != "ability"
        and i.item_slot_type in ["spirit", "vitality", "weapon"]
        and i.image is not None
    }
