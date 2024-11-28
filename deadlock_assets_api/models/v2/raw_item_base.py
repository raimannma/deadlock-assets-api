from functools import lru_cache

import css_parser
from css_parser.css import CSSRuleList, CSSStyleRule
from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator


class RawItemWeaponInfoBulletSpeedCurveSplineV2(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    slope_incoming: float = Field(..., validation_alias="m_flSlopeIncoming")
    slope_outgoing: float = Field(..., validation_alias="m_flSlopeOutgoing")
    x: float = Field(..., validation_alias="x")
    y: float = Field(..., validation_alias="y")


class RawItemWeaponInfoBulletSpeedCurveV2(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    spline: list[RawItemWeaponInfoBulletSpeedCurveSplineV2] = Field(
        None, validation_alias="m_spline"
    )
    domain_maxs: list[float] = Field(..., validation_alias="m_vDomainMaxs")
    domain_mins: list[float] = Field(..., validation_alias="m_vDomainMins")


class RawItemWeaponInfoV2(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    bullet_speed_curve: RawItemWeaponInfoBulletSpeedCurveV2 = Field(
        None, validation_alias="m_BulletSpeedCurve"
    )


class RawItemPropertyV2(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    value: str | float | None = Field(
        None, validation_alias=AliasChoices("m_strValue", "m_strVAlue")
    )
    can_set_token_override: bool | None = Field(
        None, validation_alias="m_bCanSetTokenOverride"
    )
    provided_property_type: str | None = Field(
        None, validation_alias="m_eProvidedPropertyType"
    )
    css_class: str | None = Field(None, validation_alias="m_strCSSClass")
    disable_value: str | None = Field(None, validation_alias="m_strDisableValue")
    loc_token_override: str | None = Field(
        None, validation_alias="m_strLocTokenOverride"
    )
    display_units: str | None = Field(None, validation_alias="m_eDisplayUnits")


@lru_cache
def parse_css_rules(filename: str) -> CSSRuleList:
    return css_parser.parseFile(filename).cssRules


def parse_css_ability_icon(class_name: str) -> str | None:
    for rule in parse_css_rules("res/ability_icons.css"):
        if not isinstance(rule, CSSStyleRule):
            continue
        css_class = next(
            (
                s
                for s in " ".join(rule.selectorText.split(".")).split(" ")
                if s == class_name
            ),
            None,
        )
        if css_class is None:
            continue
        rule: CSSStyleRule = rule
        background_image = rule.style.getProperty("background-image")
        if background_image is None:
            continue
        background_image = background_image.value[4:-1]
        background_image = background_image.replace("_psd.vtex", ".psd")
        background_image = background_image.split("images/")[-1]
        return 'panorama:"file://{images}/' + background_image + '"'
    return None


class RawItemBaseV2(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    class_name: str
    start_trained: bool | None = Field(None, validation_alias="m_bStartTrained")
    image: str | None = Field(None, validation_alias="m_strAbilityImage")
    update_time: int | None = Field(None, validation_alias="m_iUpdateTime")
    properties: dict[str, RawItemPropertyV2] | None = Field(
        None, validation_alias="m_mapAbilityProperties"
    )
    weapon_info: RawItemWeaponInfoV2 | None = Field(
        None, validation_alias="m_WeaponInfo"
    )
    css_class: str | None = Field(None, validation_alias="m_strCSSClass")

    @model_validator(mode="after")
    def check_image_path(self):
        if (
            self.image is not None
            and self.css_class is not None
            and self.css_class != ""
        ):
            try:
                css_image = parse_css_ability_icon(self.css_class)
                self.image = css_image or self.image
            except Exception as e:
                print(f"Failed to parse css for {self.css_class}: {e}")
        return self
