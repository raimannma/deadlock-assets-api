from functools import lru_cache

import css_parser
from css_parser.css import CSSStyleRule
from pydantic import BaseModel, ConfigDict, Field, computed_field

from deadlock_assets_api.models.map_lanes import LANES

TOWER_IDS = {
    **{f"#Team{team_id + 1}Core": f"team{team_id}_core" for team_id in range(2)},
    **{f"#Team{team_id + 1}Titan": f"team{team_id}_titan" for team_id in range(2)},
    **{
        f"#Team{team_id + 1}Tier{tier + 1}_{i}": f"team{team_id}_tier{tier + 1}_{i}"
        for team_id in range(2)
        for tier in range(2)
        for i in range(1, 5)
    },
}


class ObjectivePosition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    left_relative: float = Field(
        ...,
        description="The relative margin left of the map image.",
    )
    top_relative: float = Field(
        ...,
        description="The relative margin top of the map image.",
    )


class ObjectivePositions(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    team0_core: ObjectivePosition
    team1_core: ObjectivePosition
    team0_titan: ObjectivePosition
    team1_titan: ObjectivePosition
    team0_tier2_1: ObjectivePosition
    team0_tier2_2: ObjectivePosition
    team0_tier2_3: ObjectivePosition
    team0_tier2_4: ObjectivePosition
    team1_tier2_1: ObjectivePosition
    team1_tier2_2: ObjectivePosition
    team1_tier2_3: ObjectivePosition
    team1_tier2_4: ObjectivePosition
    team0_tier1_1: ObjectivePosition
    team0_tier1_2: ObjectivePosition
    team0_tier1_3: ObjectivePosition
    team0_tier1_4: ObjectivePosition
    team1_tier1_1: ObjectivePosition
    team1_tier1_2: ObjectivePosition
    team1_tier1_3: ObjectivePosition
    team1_tier1_4: ObjectivePosition


class MapImages(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    background: str = Field(
        ...,
        description="The background image of the map.",
    )
    frame: str = Field(
        ...,
        description="The frame image of the map.",
    )
    mid: str = Field(
        ...,
        description="The mid image of the map.",
    )

    # lanes: list[str] = Field(
    #     ...,
    #     description="The lane images of the map.",
    # )
    # neutrals: dict[str, str] = Field(
    #     ...,
    #     description="The neutral images of the map.",
    # )

    def set_base_url(self, base_url: str):
        self.background = f"{base_url}{self.background}"
        self.frame = f"{base_url}{self.frame}"
        self.mid = f"{base_url}{self.mid}"
        # for i, lane in enumerate(self.lanes):
        #     self.lanes[i] = f"{base_url}{lane}"
        # for k, v in self.neutrals.items():
        #     self.neutrals[k] = f"{base_url}{v}"


class ZiplanePath(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    P0_points: list[tuple[float, float, float]] = Field(
        ...,
        description="The P0 points of the path.",
    )
    P1_points: list[tuple[float, float, float]] = Field(
        ...,
        description="The P1 points of the path.",
    )
    P2_points: list[tuple[float, float, float]] = Field(
        ...,
        description="The P2 points of the path.",
    )

    @classmethod
    def from_pathnodes(cls, pathnodes: list[list[float]]) -> "ZiplanePath":
        return cls(
            P0_points=[(n[0], n[1], n[2]) for n in pathnodes],
            P1_points=[(n[3], n[4], n[5]) for n in pathnodes],
            P2_points=[(n[6], n[7], n[8]) for n in pathnodes],
        )


class Map(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    images: MapImages = Field(
        ...,
        description="The images of the map.",
    )

    def set_base_url(self, base_url: str):
        self.images.set_base_url(base_url)

    @computed_field
    @property
    def objective_positions(self) -> ObjectivePositions:
        objectives = load_objectives()

        def parse_percentage(value: str) -> float:
            if value.endswith("%"):
                return float(value[:-1]) / 100
            return float(value)

        return ObjectivePositions.model_validate(
            {
                TOWER_IDS[rule.selectorText]: ObjectivePosition(
                    left_relative=parse_percentage(rule.style.marginLeft),
                    top_relative=parse_percentage(rule.style.marginTop),
                )
                for rule in objectives.cssRules
                if isinstance(rule, CSSStyleRule) and rule.selectorText in TOWER_IDS
            }
        )

    @computed_field(
        description="The ziplane paths of the map. Each path is a list of P0, P1, and P2 points, describing the cubic spline."
    )
    @property
    def zipline_paths(self) -> list[ZiplanePath]:
        return [ZiplanePath.from_pathnodes(lane) for lane in LANES]

    @classmethod
    def get_default(cls) -> "Map":
        return cls(
            images=MapImages(
                background="images/maps/minimap_bg_psd.png",
                frame="images/maps/minimap_frame_psd.png",
                mid="images/maps/minimap_mid_psd.png",
                # lanes=[
                #     "images/maps/minimap_lane_1_psd.png",
                #     "images/maps/minimap_lane_2_psd.png",
                #     "images/maps/minimap_lane_3_psd.png",
                #     "images/maps/minimap_lane_4_psd.png",
                # ],
                # neutrals={
                #     f.replace("_png.png", ""): os.path.join("images", "maps", "neutrals", f)
                #     for f in os.listdir("images/maps/neutrals")
                # },
            ),
        )


@lru_cache
def load_objectives():
    return css_parser.parseFile("res/objectives_map.css")
