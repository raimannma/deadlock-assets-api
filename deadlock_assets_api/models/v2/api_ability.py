import re
from typing import Literal

from pydantic import BaseModel, ConfigDict

from deadlock_assets_api.glob import VIDEO_BASE_URL
from deadlock_assets_api.models.v2.api_item_base import ItemBaseV2
from deadlock_assets_api.models.v2.enums import AbilityTypeV2
from deadlock_assets_api.models.v2.raw_ability import RawAbilityUpgradeV2, RawAbilityV2
from deadlock_assets_api.models.v2.raw_hero import RawHeroV2


def extract_video_url(v: str) -> str | None:
    if not v:
        return None
    return f"{VIDEO_BASE_URL}/{v.split('videos/')[-1]}"


class AbilityDescriptionV2(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    desc: str | None
    quip: str | None
    t1_desc: str | None
    t2_desc: str | None
    t3_desc: str | None

    @classmethod
    def from_raw_ability(
        cls,
        raw_ability: RawAbilityV2,
        raw_heroes: list[RawHeroV2],
        localization: dict[str, str],
    ) -> "AbilityDescriptionV2":
        def replace_templates(input_str: str | None, tier: int | None) -> str | None:
            if not input_str:
                return None

            def replacer(match):
                variable = match.group(1)

                replaced = raw_ability.properties.get(variable)
                if replaced is None:
                    replaced = next(
                        (
                            v
                            for k, v in raw_ability.properties.items()
                            if v.loc_token_override and v.loc_token_override == variable
                        ),
                        None,
                    )
                if replaced is not None:
                    replaced = replaced.value
                if tier is not None and len(raw_ability.upgrades) >= tier:
                    replaced = next(
                        (
                            i.bonus.rstrip("m") if isinstance(i.bonus, str) else i.bonus
                            for i in raw_ability.upgrades[tier - 1].property_upgrades
                            if i.name.lower() == variable.lower()
                        ),
                        replaced,
                    )
                if replaced is None:
                    if variable == "iv_attack":
                        replaced = "LMC"
                    elif variable == "iv_attack2":
                        replaced = "RMC"
                    elif variable == "key_alt_cast":
                        replaced = "M3"
                    elif variable == "ability_key":
                        hero_items = next(
                            h.items
                            for h in raw_heroes
                            if raw_ability.class_name in h.items.values()
                        )
                        if hero_items is not None:
                            ability_key = next(
                                (
                                    k.ability_index()
                                    for k, v in hero_items.items()
                                    if v == raw_ability.class_name
                                ),
                                None,
                            )
                            replaced = ability_key
                    elif variable.startswith("in_ability"):
                        index = int(variable[-1])
                        replaced = localization.get(f"citadel_keybind_ability{index}")
                    elif variable == "hero_name":
                        replaced = next(
                            (
                                localization.get(h.class_name, h.class_name)
                                for h in raw_heroes
                                if raw_ability.class_name in h.items.values()
                            ),
                            None,
                        )
                        if replaced is None:
                            print(
                                f"Failed to find hero name for {raw_ability.class_name}"
                            )
                    else:
                        var_to_loc = {
                            "key_duck": "citadel_keybind_crouch",
                            "in_mantle": "citadel_keybind_mantle",
                            "key_innate_1": "citadel_keybind_roll",
                        }
                        replaced = localization.get(var_to_loc.get(variable, variable))
                if replaced is None:
                    print(f"Failed to replace {variable}")
                return str(replaced) if replaced else match.group(0)

            return re.sub(r"\{s:([^}]+)}", replacer, input_str)

        return cls(
            desc=replace_templates(
                localization.get(f"{raw_ability.class_name}_desc"), None
            ),
            quip=replace_templates(
                localization.get(f"{raw_ability.class_name}_quip"), None
            ),
            t1_desc=replace_templates(
                localization.get(f"{raw_ability.class_name}_t1_desc"), 1
            ),
            t2_desc=replace_templates(
                localization.get(f"{raw_ability.class_name}_t2_desc"), 2
            ),
            t3_desc=replace_templates(
                localization.get(f"{raw_ability.class_name}_t3_desc"), 3
            ),
        )


class AbilityVideosV2(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    webm: str | None
    mp4: str | None

    @classmethod
    def from_raw_video(cls, raw_video: str) -> "AbilityVideosV2":
        webm = extract_video_url(raw_video)
        return cls(
            webm=webm,
            mp4=webm.replace(".webm", "_h264.mp4") if webm else None,
        )


class AbilityV2(ItemBaseV2):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    type: Literal["ability"] = "ability"
    behaviours: list[str] | None
    description: AbilityDescriptionV2
    upgrades: list[RawAbilityUpgradeV2] | None
    ability_type: AbilityTypeV2 | None
    dependant_abilities: list[str] | None
    videos: AbilityVideosV2 | None

    @classmethod
    def from_raw_item(
        cls,
        raw_ability: RawAbilityV2,
        raw_heroes: list[RawHeroV2],
        localization: dict[str, str],
    ) -> "AbilityV2":
        raw_model = super().from_raw_item(raw_ability, raw_heroes, localization)
        raw_model["behaviours"] = (
            [b.strip() for b in raw_ability.behaviour_bits.split("|")]
            if raw_ability.behaviour_bits
            else None
        )
        raw_model["description"] = AbilityDescriptionV2.from_raw_ability(
            raw_ability, raw_heroes, localization
        )
        raw_model["videos"] = (
            AbilityVideosV2.from_raw_video(raw_ability.video)
            if raw_ability.video
            else None
        )
        del raw_model["video"]
        return cls(**raw_model)
