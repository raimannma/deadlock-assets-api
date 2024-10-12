from enum import Enum


class ItemTier(int, Enum):
    EModTier_1 = 1
    EModTier_2 = 2
    EModTier_3 = 3
    EModTier_4 = 4

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if isinstance(value, int) and value == member.value:
                return member
            if isinstance(value, str) and value.lower() == member.name.lower():
                return member
        return None


class AbilityType(str, Enum):
    EAbilityType_Innate = "innate"
    EAbilityType_Item = "item"
    EAbilityType_Signature = "signature"
    EAbilityType_Ultimate = "ultimate"
    EAbilityType_Weapon = "weapon"

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if value in [member.value.lower(), member.name.lower()]:
                return member
        return None
