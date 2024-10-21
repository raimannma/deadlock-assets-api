from functools import lru_cache

import css_parser
import stringcase
from css_parser.css import ColorValue, CSSUnknownRule
from pydantic import BaseModel, ConfigDict, Field


class ColorV1(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    red: int = Field(..., description="The red value of the color.")
    green: int = Field(..., description="The green value of the color.")
    blue: int = Field(..., description="The blue value of the color.")
    alpha: int = Field(..., description="The alpha value of the color.")


def get_colors() -> dict[str, ColorV1]:
    return {
        k: ColorV1(red=v.red, green=v.green, blue=v.blue, alpha=v.alpha)
        for k, v in load_colors().items()
    }


@lru_cache
def load_colors() -> dict[str, ColorValue]:
    colors = {}
    css_colors = css_parser.parseFile("res/citadel_shared_colors.css")
    for rule in css_colors.cssRules:
        if not isinstance(rule, CSSUnknownRule):
            continue
        if not rule.cssText.startswith("@define"):
            continue

        # Split CSS Text into key and value
        css_parts = rule.cssText[8:].replace(";", "").strip().split(":")
        css_key, css_value = (v.strip() for v in css_parts)

        # Parse Color Value
        color_value = ColorValue(
            css_value[:7] if css_value.startswith("#") else css_value
        )
        color_value._alpha = (
            int(css_value[7:], 16)
            if css_value.startswith("#") and len(css_value) > 7
            else 255
        )

        css_key = stringcase.snakecase(css_key)
        colors[css_key] = color_value
    return colors
