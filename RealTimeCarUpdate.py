from .Cursor import Cursor
from .Enums import CarLocation
from .LapInfo import LapInfo


class RealTimeCarUpdate:

    def __init__(self, cur: Cursor):

        self.car_index = cur.read_u16()
        self.driver_index = cur.read_u16()
        self.driver_count = cur.read_u8()
        self.gear = cur.read_u8()
        self.world_pos_x = cur.read_f32()
        self.world_pos_y = cur.read_f32()
        self.yaw = cur.read_f32()
        self.car_location = CarLocation(cur.read_u8())
        self.kmh = cur.read_u16()
        self.position = cur.read_u16()
        self.cup_position = cur.read_u16()
        self.track_position = cur.read_u16()
        self.spline_position = cur.read_f32()
        self.lap = cur.read_u16()
        self.delta = cur.read_i32()
        self.best_session_lap = LapInfo(cur)
        cur = self.best_session_lap.get_cur()
        self.last_lap = LapInfo(cur)
        cur = self.last_lap.get_cur()
        self.current_lap = LapInfo(cur)
