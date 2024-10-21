from pydantic import BaseModel, computed_field

RANK_COLORS = [
    "#333333",
    "#CB643B",
    "#96C86F",
    "#66AEBC",
    "#C15F78",
    "#705B9C",
    "#D7644F",
    "#7DD1BA",
    "#E75CC0",
    "#B37134",
    "#A89F96",
    "#D9963F",
]


class RankV2(BaseModel):
    tier: int
    name: str
    # image: str

    @computed_field
    @property
    def color(self) -> str:
        return RANK_COLORS[self.tier]

    @classmethod
    def from_tier(cls, tier: int, localization: dict[str, str]) -> "RankV2":
        return cls(
            tier=tier,
            name=localization[f"Citadel_ranks_rank{tier}"],
        )
