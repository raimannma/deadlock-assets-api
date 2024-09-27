import os

from pydantic import BaseModel, ConfigDict, Field


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
    lanes: list[str] = Field(
        ...,
        description="The lane images of the map.",
    )
    mid: str = Field(
        ...,
        description="The mid image of the map.",
    )
    neutrals: dict[str, str] = Field(
        ...,
        description="The neutral images of the map.",
    )

    def set_base_url(self, base_url: str):
        self.background = f"{base_url}{self.background}"
        self.frame = f"{base_url}{self.frame}"
        self.mid = f"{base_url}{self.mid}"
        for i, lane in enumerate(self.lanes):
            self.lanes[i] = f"{base_url}{lane}"
        for k, v in self.neutrals.items():
            self.neutrals[k] = f"{base_url}{v}"


class Map(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    images: MapImages = Field(
        ...,
        description="The images of the map.",
    )

    def set_base_url(self, base_url: str):
        self.images.set_base_url(base_url)


def get_default_map() -> Map:
    neutrals = {
        f.replace("_png.png", ""): os.path.join("images", "maps", "neutrals", f)
        for f in os.listdir("images/maps/neutrals")
    }
    return Map(
        images=MapImages(
            background="images/maps/minimap_bg_psd.png",
            frame="images/maps/minimap_frame_psd.png",
            lanes=[
                "images/maps/minimap_lane_1_psd.png",
                "images/maps/minimap_lane_2_psd.png",
                "images/maps/minimap_lane_3_psd.png",
                "images/maps/minimap_lane_4_psd.png",
            ],
            mid="images/maps/minimap_mid_psd.png",
            neutrals=neutrals,
        )
    )
