from enum import Enum


class Nationality(Enum):

    Any = 0
    Italy = 1
    Germany = 2
    France = 3
    Spain = 4
    GreatBritain = 5
    Hungary = 6
    Belgium = 7
    Switzerland = 8
    Austria = 9
    Russia = 10
    Thailand = 11
    Netherlands = 12
    Poland = 13
    Argentina = 14
    Monaco = 15
    Ireland = 16
    Brazil = 17
    SouthAfrica = 18
    PuertoRico = 19
    Slovakia = 20
    Oman = 21
    Greece = 22
    SaudiArabia = 23
    Norway = 24
    Turkey = 25
    SouthKorea = 26
    Lebanon = 27
    Armenia = 28
    Mexico = 29
    Sweden = 30
    Finland = 31
    Denmark = 32
    Croatia = 33
    Canada = 34
    China = 35
    Portugal = 36
    Singapore = 37
    Indonesia = 38
    USA = 39
    NewZealand = 40
    Australia = 41
    SanMarino = 42
    UAE = 43
    Luxembourg = 44
    Kuwait = 45
    HongKong = 46
    Colombia = 47
    Japan = 48
    Andorra = 49
    Azerbaijan = 50
    Bulgaria = 51
    Cuba = 52
    CzechRepublic = 53
    Estonia = 54
    Georgia = 55
    India = 56
    Israel = 57
    Jamaica = 58
    Latvia = 59
    Lithuania = 60
    Macau = 61
    Malaysia = 62
    Nepal = 63
    NewCaledonia = 64
    Nigeria = 65
    NorthernIreland = 66
    PapuaNewGuinea = 67
    Philippines = 68
    Qatar = 69
    Romania = 70
    Scotland = 71
    Serbia = 72
    Slovenia = 73
    Taiwan = 74
    Ukraine = 75
    Venezuela = 76
    Wales = 77
    Iran = 78
    Bahrain = 79
    Zimbabwe = 80
    ChineseTaipie = 81
    Chile = 82
    Uruguay = 83
    Madagascar = 84
    placeholder2 = 85
    placeholder3 = 86
    placeholder4 = 87
    placeholder5 = 88
    placeholder6 = 89
    placeholder7 = 90


class CarLocation(Enum):

    NONE = 0
    Track = 1
    Pitlane = 2
    PitEntry = 3
    PitExit = 4


class DriverCategory(Enum):

    bronze = 0
    Silver = 1
    Gold = 2
    Platium = 3


class CupCategory(Enum):

    Pro = 0
    ProAm = 1
    Am = 2
    Silver = 3
    National = 4


class SessionType(Enum):

    Practice = 0
    Qualifying = 4
    Superpole = 9
    Race = 10
    Hotlap = 11
    Hotstint = 12
    HotlapSuperpole = 13
    Replay = 14
    NONE = 15


class SessionPhase(Enum):

    NONE = 0
    Starting = 1
    PreFormation = 2
    FormationLap = 3
    PreSession = 4
    Session = 5
    SessionOver = 6
    PostSession = 7
    ResultUI = 8


class LapType(Enum):

    ERROR = 0
    OutLap = 1
    Regular = 2
    InLap = 3
