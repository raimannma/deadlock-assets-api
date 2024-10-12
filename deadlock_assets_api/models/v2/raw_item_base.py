from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class RawItemWeaponInfoBulletSpeedCurveSpline(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    slope_incoming: float = Field(..., validation_alias="m_flSlopeIncoming")
    slope_outgoing: float = Field(..., validation_alias="m_flSlopeOutgoing")
    x: float = Field(..., validation_alias="x")
    y: float = Field(..., validation_alias="y")


class RawItemWeaponInfoBulletSpeedCurve(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    spline: list[RawItemWeaponInfoBulletSpeedCurveSpline] = Field(
        None, validation_alias="m_spline"
    )
    domain_maxs: list[float] = Field(..., validation_alias="m_vDomainMaxs")
    domain_mins: list[float] = Field(..., validation_alias="m_vDomainMins")


class RawItemWeaponInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    bullet_speed_curve: RawItemWeaponInfoBulletSpeedCurve = Field(
        None, validation_alias="m_BulletSpeedCurve"
    )


class RawItemProperty(BaseModel):
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
    display_units: str | None = Field(None, validation_alias="m_eDisplayUnits")


class RawItemBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    class_name: str
    start_trained: bool | None = Field(None, validation_alias="m_bStartTrained")
    image: str | None = Field(None, validation_alias="m_strAbilityImage")
    update_time: int | None = Field(None, validation_alias="m_iUpdateTime")
    properties: dict[str, RawItemProperty] | None = Field(
        None, validation_alias="m_mapAbilityProperties"
    )
    weapon_info: RawItemWeaponInfo = Field(..., validation_alias="m_WeaponInfo")
