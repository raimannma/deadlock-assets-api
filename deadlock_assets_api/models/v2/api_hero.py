import json

from pydantic import BaseModel, ConfigDict

from deadlock_assets_api.glob import IMAGE_BASE_URL
from deadlock_assets_api.models.hero import HeroItemType
from deadlock_assets_api.models.item import ItemSlotType
from deadlock_assets_api.models.v2.raw_hero import (
    RawHero,
    RawHeroItemSlotInfoValue,
    RawHeroLevelInfo,
    RawHeroPurchaseBonus,
    RawHeroScalingStat,
    RawHeroShopStatDisplay,
    RawHeroShopWeaponStatsDisplay,
    RawHeroStartingStats,
    RawHeroStatsDisplay,
    RawHeroStatsUI,
)


def extract_image_url(v: str) -> str | None:
    if not v:
        return None
    split_index = v.find("abilities/")
    if split_index == -1:
        split_index = v.find("upgrades/")
    if split_index == -1:
        split_index = v.find("hud/")
    if split_index == -1:
        split_index = v.find("heroes/")
    v = f"{IMAGE_BASE_URL}/{v[split_index:]}"
    if v.endswith(".png") and not v.endswith("_psd.png"):
        v = v.replace(".png", "_psd.png")
    else:
        v = v.replace(".psd", "_psd.png")
    return v.replace('"', "")


class HeroImages(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    icon_hero_card: str | None = None
    icon_hero_card_webp: str | None = None
    icon_image_small: str | None = None
    icon_image_small_webp: str | None = None
    minimap_image: str | None = None
    minimap_image_webp: str | None = None
    selection_image: str | None = None
    selection_image_webp: str | None = None
    top_bar_image: str | None = None
    top_bar_image_webp: str | None = None
    top_bar_vertical: str | None = None
    top_bar_vertical_webp: str | None = None
    weapon_image: str | None = None
    weapon_image_webp: str | None = None

    @classmethod
    def from_raw_hero(cls, raw_hero: RawHero) -> "HeroImages":
        keys = [
            "icon_hero_card",
            "icon_image_small",
            "minimap_image",
            "selection_image",
            "top_bar_image",
            "top_bar_vertical",
            "weapon_image",
        ]
        images = {
            k: extract_image_url(v)
            for k, v in raw_hero.model_dump().items()
            if k in keys
        }
        return cls(
            **images,
            **{
                f"{k}_webp": v.replace(".png", ".webp") if v is not None else None
                for k, v in images.items()
            },
        )


class HeroDescription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    lore: str | None
    role: str | None
    playstyle: str | None

    @classmethod
    def from_raw_hero(
        cls, raw_hero: RawHero, localization: dict[str, str]
    ) -> "HeroDescription":
        return cls(
            lore=localization.get(f"{raw_hero.class_name}_lore"),
            role=localization.get(f"{raw_hero.class_name}_role"),
            playstyle=localization.get(f"{raw_hero.class_name}_playstyle"),
        )


class HeroPhysics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    collision_height: float
    collision_radius: float
    footstep_sound_travel_distance_meters: float
    stealth_speed_meters_per_second: float
    step_height: float
    step_sound_time: float
    step_sound_time_sprinting: float | None

    @classmethod
    def from_raw_hero(cls, raw_hero: RawHero) -> "HeroPhysics":
        return cls(
            collision_height=raw_hero.collision_height,
            collision_radius=raw_hero.collision_radius,
            footstep_sound_travel_distance_meters=raw_hero.footstep_sound_travel_distance_meters,
            stealth_speed_meters_per_second=raw_hero.stealth_speed_meters_per_second,
            step_height=raw_hero.step_height,
            step_sound_time=raw_hero.step_sound_time,
            step_sound_time_sprinting=raw_hero.step_sound_time_sprinting,
        )


class HeroColors(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    glow_enemy: tuple[int, int, int]
    glow_friendly: tuple[int, int, int]
    glow_team1: tuple[int, int, int]
    glow_team2: tuple[int, int, int]
    ui: tuple[int, int, int]

    @classmethod
    def from_raw_hero(cls, raw_hero: RawHero) -> "HeroColors":
        return cls(
            glow_enemy=raw_hero.color_glow_enemy,
            glow_friendly=raw_hero.color_glow_friendly,
            glow_team1=raw_hero.color_glow_team1,
            glow_team2=raw_hero.color_glow_team2,
            ui=raw_hero.color_ui,
        )


class HeroShopWeaponStatsDisplay(RawHeroShopWeaponStatsDisplay):
    model_config = ConfigDict(populate_by_name=True)

    weapon_attributes: list[str] | None
    weapon_image_webp: str | None = None

    @classmethod
    def from_raw_hero_shop_weapon_stats_display(
        cls, raw_hero_shop_weapon_stats_display: RawHeroShopWeaponStatsDisplay
    ) -> "HeroShopWeaponStatsDisplay":
        raw_model = raw_hero_shop_weapon_stats_display.model_dump()
        raw_model["weapon_attributes"] = (
            [
                i.strip()
                for i in raw_hero_shop_weapon_stats_display.weapon_attributes.split("|")
            ]
            if raw_hero_shop_weapon_stats_display.weapon_attributes
            else []
        )
        raw_model["weapon_image"] = extract_image_url(
            raw_hero_shop_weapon_stats_display.weapon_image
        )
        if raw_model["weapon_image"] is not None:
            raw_model["weapon_image_webp"] = raw_model["weapon_image"].replace(
                ".png", ".webp"
            )
        return cls(**raw_model)


class HeroShopStatDisplay(RawHeroShopStatDisplay):
    model_config = ConfigDict(populate_by_name=True)

    weapon_stats_display: HeroShopWeaponStatsDisplay

    @classmethod
    def from_raw_hero(cls, raw_hero: RawHero) -> "HeroShopStatDisplay":
        raw_model = raw_hero.shop_stat_display.model_dump()
        raw_model["weapon_stats_display"] = (
            HeroShopWeaponStatsDisplay.from_raw_hero_shop_weapon_stats_display(
                raw_hero.shop_stat_display.weapon_stats_display
            )
        )
        return cls(**raw_model)


class HeroLevelInfo(RawHeroLevelInfo):
    model_config = ConfigDict(populate_by_name=True)

    bonus_currencies: list[str] | None

    @classmethod
    def from_raw_level_info(cls, raw_level_info: RawHeroLevelInfo) -> "HeroLevelInfo":
        raw_model = raw_level_info.model_dump()
        raw_model["bonus_currencies"] = (
            list(raw_level_info.bonus_currencies.keys())
            if raw_level_info.bonus_currencies
            else None
        )
        return cls(**raw_model)


class HeroStartingStat(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    value: int | float
    display_stat_name: str


class HeroStartingStats(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    max_move_speed: HeroStartingStat
    sprint_speed: HeroStartingStat
    crouch_speed: HeroStartingStat
    move_acceleration: HeroStartingStat
    light_melee_damage: HeroStartingStat
    heavy_melee_damage: HeroStartingStat
    max_health: HeroStartingStat
    weapon_power: HeroStartingStat
    reload_speed: HeroStartingStat
    weapon_power_scale: HeroStartingStat
    proc_build_up_rate_scale: HeroStartingStat
    stamina: HeroStartingStat
    base_health_regen: HeroStartingStat
    stamina_regen_per_second: HeroStartingStat
    ability_resource_max: HeroStartingStat
    ability_resource_regen_per_second: HeroStartingStat
    crit_damage_received_scale: HeroStartingStat
    tech_duration: HeroStartingStat
    tech_range: HeroStartingStat
    bullet_armor_damage_reduction: HeroStartingStat | None

    @classmethod
    def from_raw_starting_stats(
        cls, raw_hero_starting_stats: RawHeroStartingStats
    ) -> "HeroStartingStats":
        return cls(
            **{
                k: (
                    HeroStartingStat(
                        value=v,
                        display_stat_name=raw_hero_starting_stats.model_fields[
                            k
                        ].validation_alias,
                    )
                    if v is not None
                    else None
                )
                for k, v in raw_hero_starting_stats.model_dump().items()
            }
        )


class Hero(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    class_name: str
    name: str
    description: HeroDescription
    recommended_upgrades: list[str] | None
    player_selectable: bool
    bot_selectable: bool
    disabled: bool
    in_development: bool
    needs_testing: bool
    assigned_players_only: bool
    limited_testing: bool
    complexity: int
    skin: int
    readability: int
    images: HeroImages
    items: dict[HeroItemType, str]
    starting_stats: HeroStartingStats
    item_slot_info: dict[ItemSlotType, RawHeroItemSlotInfoValue]
    physics: HeroPhysics
    colors: HeroColors
    shop_stat_display: HeroShopStatDisplay
    stats_display: RawHeroStatsDisplay
    hero_stats_ui: RawHeroStatsUI
    level_info: dict[str, HeroLevelInfo]
    scaling_stats: dict[str, RawHeroScalingStat]
    purchase_bonuses: dict[ItemSlotType, list[RawHeroPurchaseBonus]]
    standard_level_up_upgrades: dict[str, float]

    @classmethod
    def from_raw_hero(cls, raw_hero: RawHero, localization: dict[str, str]) -> "Hero":
        raw_model = raw_hero.model_dump()
        raw_model["name"] = localization.get(raw_hero.class_name, raw_hero.class_name)
        raw_model["description"] = HeroDescription.from_raw_hero(raw_hero, localization)
        raw_model["starting_stats"] = HeroStartingStats.from_raw_starting_stats(
            raw_hero.starting_stats
        )
        raw_model["images"] = HeroImages.from_raw_hero(raw_hero)
        raw_model["physics"] = HeroPhysics.from_raw_hero(raw_hero)
        raw_model["colors"] = HeroColors.from_raw_hero(raw_hero)
        raw_model["level_info"] = {
            k: HeroLevelInfo.from_raw_level_info(v)
            for k, v in raw_hero.level_info.items()
        }
        raw_model["shop_stat_display"] = HeroShopStatDisplay.from_raw_hero(raw_hero)
        return cls(**raw_model)


def test_parse():
    def get_raw_heroes():
        with open("res/raw_heroes.json") as f:
            raw_heroes = json.load(f)
        return [
            RawHero(class_name=k, **v)
            for k, v in raw_heroes.items()
            if k.startswith("hero_")
            and "base" not in k
            and "generic" not in k
            and "dummy" not in k
        ]

    raw_heroes = get_raw_heroes()

    localization = {}
    with open("res/localization/citadel_gc_english.json") as f:
        localization.update(json.load(f)["lang"]["Tokens"])
    with open("res/localization/citadel_heroes_english.json") as f:
        localization.update(json.load(f)["lang"]["Tokens"])
    with open("res/localization/citadel_gc_german.json") as f:
        localization.update(json.load(f)["lang"]["Tokens"])
    with open("res/localization/citadel_heroes_german.json") as f:
        localization.update(json.load(f)["lang"]["Tokens"])

    heroes = [Hero.from_raw_hero(raw_hero, localization) for raw_hero in raw_heroes]

    with open("test.json", "w") as f:
        json.dump([hero.model_dump(exclude_none=True) for hero in heroes], f, indent=2)
    print(heroes)


if __name__ == "__main__":
    test_parse()
