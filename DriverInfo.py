from .Cursor import Cursor
from .Enums import DriverCategory, Nationality


class DriverInfo:

    def __init__(self, cur: Cursor):
        self.first_name = cur.read_string()
        self.last_name = cur.read_string()
        self.short_name = cur.read_string()
        self.category = DriverCategory(cur.read_u8())
        self.nationality = Nationality(cur.read_u16())

        self._cur = cur

    def get_cur(self) -> Cursor:
        cur = self._cur
        self._cur = None
        return cur

    def __str__(self) -> str:

        return f"Name: {self.first_name} {self.last_name}"
