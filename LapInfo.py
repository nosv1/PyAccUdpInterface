from .Cursor import Cursor
from .Enums import LapType


class LapInfo:

    def __init__(self, cur: Cursor):

        self.lap_time_ms = cur.read_u32()
        self.car_index = cur.read_u16()
        self.driver_index = cur.read_u16()

        split_count = cur.read_u8()
        self.splits = []
        for _ in range(split_count):
            self.splits.append(cur.read_i32())

        self.is_invalid = cur.read_u8() > 0
        self.is_valid_for_best = cur.read_u8() > 0

        is_out_lap = cur.read_u8() > 0
        is_in_lap = cur.read_u8() > 0

        if is_out_lap:
            self.late_type = LapType.OutLap

        elif is_in_lap:
            self.late_type = LapType.InLap

        else:
            self.late_type = LapType.Regular

        for i, split in enumerate(self.splits):
            if split == 2147483647:  # Max int32 value
                self.splits[i] = 0

        if self.lap_time_ms == 2147483647:
            self.lap_time_ms = 0

        self._cur = cur

    def get_cur(self):
        cur = self._cur
        self._cur = None
        return cur
