from enum import StrEnum


class Language(StrEnum):
    Brazilian = "brazilian"
    Bulgarian = "bulgarian"
    Czech = "czech"
    Danish = "danish"
    Dutch = "dutch"
    English = "english"
    Finnish = "finnish"
    French = "french"
    German = "german"
    Greek = "greek"
    Hungarian = "hungarian"
    Indonesian = "indonesian"
    Italian = "italian"
    Japanese = "japanese"
    Koreana = "koreana"
    Latam = "latam"
    Norwegian = "norwegian"
    Polish = "polish"
    Portuguese = "portuguese"
    Romanian = "romanian"
    Russian = "russian"
    Schinese = "schinese"
    Spanish = "spanish"
    Swedish = "swedish"
    Tchinese = "tchinese"
    Thai = "thai"
    Turkish = "turkish"
    Ukrainian = "ukrainian"
    Vietnamese = "vietnamese"

    def __missing__(self, _):
        return Language.English
