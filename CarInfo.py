from .Cursor import Cursor
from .DriverInfo import DriverInfo
from .Enums import CupCategory, Nationality


class CarInfo:

    def __init__(self, car_index: int):

        self.car_index = car_index
        self.model_type = -1
        self.team_name = ""
        self.race_number = -1
        self.cup_category = CupCategory.National
        self.current_driver_index = -1
        self.drivers = []
        self.nationality = Nationality.Any

    def update(self, cur: Cursor):

        self.model_type = cur.read_u8()
        self.team_name = cur.read_string()
        self.race_number = cur.read_i32()
        self.cup_category = CupCategory(cur.read_u8())
        self.current_driver_index = cur.read_u8()
        self.nationality = Nationality(cur.read_u16())

        self.drivers.clear()
        driver_count = cur.read_u8()
        for _ in range(driver_count):

            driver = DriverInfo(cur)
            cur = driver.get_cur()
            self.drivers.append(driver)

    def __str__(self) -> str:

        return f"ID: {self.car_index} Team: {self.team_name} " "N°: {self.race_number}"
