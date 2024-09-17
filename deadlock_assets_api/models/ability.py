from pydantic import BaseModel, ConfigDict, Field


class AbilityInfoProperty(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    value: str | int | float | None = Field(None, validation_alias="m_strValue")
    disable_value: str | None = Field(None, validation_alias="m_strDisableValue")
    can_set_token_override: bool | None = Field(
        None, validation_alias="m_bCanSetTokenOverride"
    )


class AbilityInfoWeaponInfoBulletSpeedCurveSpline(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    x: float
    y: float
    slope_incoming: float = Field(..., validation_alias="m_flSlopeIncoming")
    slope_outgoing: float = Field(..., validation_alias="m_flSlopeOutgoing")


class AbilityInfoWeaponInfoBulletSpeedCurveTangents(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    incoming_tangent: str = Field(..., validation_alias="m_nIncomingTangent")
    outgoing_tangent: str = Field(..., validation_alias="m_nOutgoingTangent")


class AbilityInfoWeaponInfoBulletSpeedCurve(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    spline: list[AbilityInfoWeaponInfoBulletSpeedCurveSpline] = Field(
        ..., validation_alias="m_spline"
    )
    tangents: list[AbilityInfoWeaponInfoBulletSpeedCurveTangents] = Field(
        ..., validation_alias="m_tangents"
    )
    domain_mins: list[float] = Field(..., validation_alias="m_vDomainMins")
    domain_maxs: list[float] = Field(..., validation_alias="m_vDomainMaxs")


class AbilityInfoWeaponInfoRecoil(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    range: list[float] | float = Field(..., validation_alias="m_Range")
    burst_slope: float | None = Field(None, validation_alias="m_flBurstSlope")
    burst_exponent: float | None = Field(None, validation_alias="m_flBurstExponent")
    burst_constant: float | None = Field(None, validation_alias="m_flBurstConstant")


class AbilityInfoWeaponInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    bullet_speed_curve: AbilityInfoWeaponInfoBulletSpeedCurve = Field(
        ..., validation_alias="m_BulletSpeedCurve"
    )
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
    vertical_recoil: AbilityInfoWeaponInfoRecoil | None = Field(
        None, validation_alias="m_VerticallRecoil"
    )
    horizontal_recoil: AbilityInfoWeaponInfoRecoil | None = Field(
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


class AbilityDofWhileZoomed(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    m_fl_dof_near_crisp: float = Field(..., validation_alias="m_flDofNearCrisp")
    m_fl_dof_far_crisp: float = Field(..., validation_alias="m_flDofFarCrisp")
    m_fl_dof_far_blurry: float = Field(..., validation_alias="m_flDofFarBlurry")


class Ability(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field()
    ability_image: str | None = Field(None, validation_alias="m_strAbilityImage")
    properties: dict[str, AbilityInfoProperty] | None = Field(
        None, validation_alias="m_mapAbilityProperties"
    )
    weapon_info: AbilityInfoWeaponInfo | None = Field(
        None, validation_alias="m_WeaponInfo"
    )
    start_trained: bool | None = Field(None, validation_alias="m_bStartTrained")
    dof_while_zoomed: AbilityDofWhileZoomed | None = Field(
        None, validation_alias="m_DOFWhileZoomed"
    )
    ability_points_cost: int | None = Field(
        None, validation_alias="m_nAbilityPointsCost"
    )
    abillity_unlocks_cost: int | None = Field(
        None, validation_alias="m_nAbillityUnlocksCost"
    )  # typo in the original data
    max_level: int | None = Field(None, validation_alias="m_iMaxLevel")

    def model_post_init(self, __context):
        if self.ability_image:
            self.ability_image = (
                (
                    "images/"
                    + self.ability_image[self.ability_image.find("abilities/") :]
                )
                .replace('"', "")
                .replace(".psd", "_psd.png")
            )

    def set_base_url(self, base_url: str):
        if self.ability_image:
            self.ability_image = f"{base_url}{self.ability_image}"
