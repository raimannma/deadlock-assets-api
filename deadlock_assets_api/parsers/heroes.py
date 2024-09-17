from deadlock_assets_api.models.hero import Hero, HeroImages


def parse_heroes(data: dict) -> list[Hero]:
    hero_dicts = {
        k.removeprefix("hero_"): v
        for k, v in data.items()
        if k.startswith("hero_") and k != "hero_base"
    }
    images = [
        ("portrait", ""),
        ("card", "_card"),
        ("vertical", "_vertical"),
        ("mm", "_mm"),
        ("sm", "_sm"),
        ("gun", "_gun"),
    ]
    return [
        Hero(
            name=name,
            images=HeroImages(
                **{
                    img_name: f"images/heroes/{name}{postfix}_psd.png"
                    for (img_name, postfix) in images
                }
            ),
            **v,
        )
        for name, v in hero_dicts.items()
    ]
