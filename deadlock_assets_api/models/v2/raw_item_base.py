from pydantic import AliasChoices, BaseModel, ConfigDict, Field


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
