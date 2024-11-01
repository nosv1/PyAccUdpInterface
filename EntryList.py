from .CarInfo import CarInfo
from .Cursor import Cursor


class EntryList:

    def __init__(self):

        self.entry_list: list[CarInfo] = []

    def update(self, cur: Cursor):

        self.entry_list = []

        _ = cur.read_i32()  # Connection id
        car_entry_count = cur.read_u16()
        for _ in range(car_entry_count):
            self.entry_list.append(CarInfo(cur.read_u16()))

    def update_car(self, cur: Cursor):
        car_id = cur.read_u16()

        car_info = None
        for car in self.entry_list:
            if car.car_index == car_id:
                car_info = car

        if car_info:
            car_info.update(cur)
