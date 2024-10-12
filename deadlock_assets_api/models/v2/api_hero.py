import json

from pydantic import BaseModel, ConfigDict

from deadlock_assets_api.glob import IMAGE_BASE_URL
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


def extract_image_url(image: str) -> str | None:
    if not image:
        return None
    relative_url = (
        image[image.find("/heroes/") :].replace(".psd", "_psd.png").replace('"', "")
    )
    return IMAGE_BASE_URL + relative_url


class HeroImages(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    icon_hero_card: str | None
    icon_image_small: str | None
    minimap_image: str | None
    selection_image: str | None
    top_bar_image: str | None
    top_bar_vertical: str | None

    @classmethod
    def from_raw_hero(cls, raw_hero: RawHero) -> "HeroImages":
        return cls(
            icon_hero_card=extract_image_url(raw_hero.icon_hero_card),
            icon_image_small=extract_image_url(raw_hero.icon_image_small),
            minimap_image=extract_image_url(raw_hero.minimap_image),
            selection_image=extract_image_url(raw_hero.selection_image),
            top_bar_image=extract_image_url(raw_hero.top_bar_image),
            top_bar_vertical=extract_image_url(raw_hero.top_bar_vertical_image),
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


class Hero(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    class_name: str
    name: str
    description: HeroDescription
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
    abilities: dict[str, str]
    starting_stats: RawHeroStartingStats
    item_slot_info: dict[ItemSlotType, RawHeroItemSlotInfoValue]
    physics: HeroPhysics
    colors: HeroColors
    shop_stat_display: HeroShopStatDisplay
    stats_display: RawHeroStatsDisplay
    hero_stats_ui: RawHeroStatsUI
    level_info: dict[str, RawHeroLevelInfo]
    scaling_stats: dict[str, RawHeroScalingStat]
    purchase_bonuses: dict[ItemSlotType, list[RawHeroPurchaseBonus]]
    standard_level_up_upgrades: dict[str, float]

    @classmethod
    def from_raw_hero(cls, raw_hero: RawHero, localization: dict[str, str]) -> "Hero":
        raw_model = raw_hero.model_dump()
        raw_model["name"] = localization.get(raw_hero.class_name, raw_hero.class_name)
        raw_model["description"] = HeroDescription.from_raw_hero(raw_hero, localization)
        raw_model["images"] = HeroImages.from_raw_hero(raw_hero)
        raw_model["physics"] = HeroPhysics.from_raw_hero(raw_hero)
        raw_model["colors"] = HeroColors.from_raw_hero(raw_hero)
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
