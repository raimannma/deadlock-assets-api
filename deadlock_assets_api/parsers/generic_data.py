from deadlock_assets_api.models.v1.generic_data import GenericDataV1


def parse_generic_data(data: dict) -> GenericDataV1:
    return GenericDataV1(**data)
