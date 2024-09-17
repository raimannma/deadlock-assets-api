from deadlock_assets_api.models.generic_data import GenericData


def parse_generic_data(data: dict) -> GenericData:
    return GenericData(**data)
