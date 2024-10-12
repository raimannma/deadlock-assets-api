from murmurhash2 import murmurhash2
from pydantic import BaseModel, ConfigDict

from deadlock_assets_api.glob import IMAGE_BASE_URL
from deadlock_assets_api.models.v2.raw_hero import RawHero
from deadlock_assets_api.models.v2.raw_item_base import (
    RawItemBase,
    RawItemProperty,
    RawItemWeaponInfo,
)


def parse_img_path(v):
    if v is None:
        return None
    split_index = v.find("abilities/")
    if split_index == -1:
        split_index = v.find("upgrades/")
    if split_index == -1:
        split_index = v.find("hud/")
    v = f"{IMAGE_BASE_URL}/{v[split_index:]}"
    if v.endswith(".png") and not v.endswith("_psd.png"):
        v = v.replace(".png", "_psd.png")
    else:
        v = v.replace(".psd", "_psd.png")
    return v.replace('"', "")


class ItemBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    class_name: str
    name: str
    start_trained: bool | None
    image: str | None
    hero: int | None
    update_time: int | None
    properties: dict[str, RawItemProperty] | None
    weapon_info: RawItemWeaponInfo

    @classmethod
    def from_raw_item(
        cls,
        raw_model: RawItemBase,
        raw_heroes: list[RawHero],
        localization: dict[str, str],
    ) -> dict:
        raw_model = raw_model.model_dump()
        raw_model["id"] = murmurhash2(raw_model["class_name"].encode(), 0x31415926)
        raw_model["name"] = localization.get(
            raw_model["class_name"], raw_model["class_name"]
        )
        raw_model["hero"] = next(
            (h.id for h in raw_heroes if raw_model["class_name"] in h.items.values()),
            None,
        )
        raw_model["image"] = parse_img_path(raw_model["image"])
        return raw_model
