import datetime

from .Cursor import Cursor
from .Enums import SessionPhase, SessionType
from .LapInfo import LapInfo


class RealTimeUpdate:

    def __init__(self):
        self.event_index = -1
        self.session_index = -1
        self.session_type = SessionType.NONE
        self.phase = SessionPhase.NONE

        self.session_time = datetime.datetime.fromtimestamp(0)
        self.session_end_time = datetime.datetime.fromtimestamp(0)

        self.focused_car_index = -1
        self.active_camera_set = ""
        self.active_camera = ""
        self.current_hud_page = ""
        self.is_replay_playing = False
        self.replay_session_time = datetime.datetime.fromtimestamp(0)
        self.replay_remaining_time = datetime.datetime.fromtimestamp(0)

        self.time_of_day = datetime.datetime.fromtimestamp(0)
        self.ambient_temp = -1
        self.track_temp = -1
        self.best_session_lap = None

    def update(self, cur: Cursor):

        self.event_index = cur.read_u16()
        self.session_index = cur.read_u16()
        self.session_type = SessionType(cur.read_u8())
        self.phase = SessionPhase(cur.read_u8())

        session_time = cur.read_f32() // 1000
        if session_time == -1:
            # -1 means there is no time limit
            session_time = 0

        self.session_time = datetime.datetime.fromtimestamp(session_time)

        session_end_time = cur.read_f32() // 1000
        if session_end_time == -1:
            # -1 means there is no time limit
            session_end_time = 0

        self.session_end_time = datetime.datetime.fromtimestamp(session_end_time)

        self.focused_car_index = cur.read_i32()
        self.active_camera_set = cur.read_string()
        self.active_camera = cur.read_string()
        self.current_hud_page = cur.read_string()
        self.is_replay_playing = cur.read_u8() > 0
        self.replay_session_time = datetime.datetime.fromtimestamp(0)
        self.replay_remaining_time = datetime.datetime.fromtimestamp(0)

        if self.is_replay_playing:

            replay_session_time = cur.read_f32() // 1000
            if replay_session_time != -1:
                # -1 means there is no time limit
                self.replay_session_time = datetime.datetime.fromtimestamp(
                    replay_session_time
                )

            replay_remaining_time = cur.read_f32() // 1000
            if replay_remaining_time != -1:
                # -1 means there is no time limit
                self.replay_remaining_time = datetime.datetime.fromtimestamp(
                    replay_remaining_time
                )

        self.time_of_day = datetime.datetime.fromtimestamp(cur.read_f32() / 1000)
        self.ambient_temp = cur.read_u8()
        self.track_temp = cur.read_u8()
        self.best_session_lap = LapInfo(cur)
