import datetime
import queue
import socket
import time
from copy import deepcopy
from enum import Enum
from multiprocessing import Pipe, Process, Queue
from multiprocessing.connection import Connection

from .ByteWriter import ByteWriter
from .Cursor import Cursor
from .EntryList import EntryList
from .Enums import CupCategory, SessionType
from .RealTimeCarUpdate import RealTimeCarUpdate
from .RealTimeUpdate import RealTimeUpdate
from .Registration import Registration
from .TrackData import TrackData


class accUpdInterface:

    def __init__(self, ip, port, instance_info):

        self.registration = Registration()
        self.session = RealTimeUpdate()
        self.track = TrackData()
        self.entry_list = EntryList()
        self.connected = False

        self._name = instance_info["name"]
        self._psw = instance_info["password"]
        self._speed = instance_info["speed"]
        self._cmd_psw = instance_info["cmd_password"]

        self._udp_data = {
            "connection": {"id": -1, "connected": False},
            "entries": {},
            "session": {
                "track": "None",
                "session_type": SessionType.NONE.name,
                "session_time": datetime.datetime.fromtimestamp(0),
                "session_end_time": datetime.datetime.fromtimestamp(0),
                "air_temp": 0,
                "track_temp": 0,
            },
        }

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(("", 3400))

        self._ip = ip
        self._port = port
        self._last_time_requested = datetime.datetime.now()
        self._last_connection = datetime.datetime.now()

        self.child_pipe, self.parent_pipe = Pipe()
        self.data_queue = Queue()
        self.udp_interface_listener = Process(
            target=self.listen_udp_interface, args=(self.child_pipe, self.data_queue)
        )

    @property
    def udp_data(self):
        self.parent_pipe.send("DATA_REQUEST")
        if self.parent_pipe.recv() == "DATA_OK":
            try:
                return self.data_queue.get_nowait()

            except queue.Empty:
                # idk return None
                return None

    def listen_udp_interface(self, child_pipe: Connection, data_queue: Queue):

        self.connect()

        message = ""
        while message != "STOP_PROCESS":

            if child_pipe.poll():
                message = child_pipe.recv()

            now = datetime.datetime.now()
            # if connection was lost or not established wait 2s before asking again
            if not self.connected and (now - self._last_connection).total_seconds() > 2:
                self.connect()
                self._last_connection = datetime.datetime.now()

            else:
                self.update()

            if message == "DATA_REQUEST":
                data_queue.put(deepcopy(self._udp_data))
                child_pipe.send("DATA_OK")
                message = ""

        self.disconnect()
        self._socket.close()
        child_pipe.send("PROCESS_TERMINATED")
        print("[ASM_Reader]: Process Terminated.")

    def start(self):

        print("[pyUIL] Listening to the UDP interface...")
        self.udp_interface_listener.start()

    def stop(self):

        print("[pyUIL]: Sending stopping command to process...")
        self.parent_pipe.send("STOP_PROCESS")

        print("[pyUIL]: Waiting for process to finish...")
        if self.parent_pipe.recv() == "PROCESS_TERMINATED":
            # Need to empty the queue before joining process (qsize() isn't 100% accurate)
            while self.data_queue.qsize() != 0:
                try:
                    _ = self.data_queue.get_nowait()
                except queue.Empty:
                    pass
        else:
            print(
                "[pyUIL]: Received unexpected message, program might be deadlock now."
            )

        self.udp_interface_listener.join()

    def update(self):

        # Add timeout after 1s delay to no get stuck for ever
        self._socket.settimeout(1.0)

        data = None
        try:
            data, _ = self._socket.recvfrom(2048)

        except socket.error:
            self.connected = False
            self._udp_data["connection"]["connected"] = False

        except socket.timeout:
            self.connected = False
            self._udp_data["connection"]["connected"] = False

        finally:
            self._socket.settimeout(None)

        if data:

            cur = Cursor(data)
            packet_type = cur.read_u8()

            if packet_type == 1:
                self.registration.update(cur)

                info = self._udp_data["connection"]
                info["id"] = self.registration.connection_id
                info["connected"] = True

                self.request_track_data()
                self.request_entry_list()

            elif packet_type == 2:
                self.session.update(cur)
                self.update_leaderboard_session()

            elif packet_type == 3:
                car_update = RealTimeCarUpdate(cur)
                self.is_new_entry(car_update)

            elif packet_type == 4:
                self.entry_list.update(cur)
                self.add_to_leaderboard()

            elif packet_type == 5:
                self.track.update(cur)

            elif packet_type == 6:
                self.entry_list.update_car(cur)

            elif packet_type == 7:
                # Don't care (:
                pass

    def is_new_entry(self, car_update):

        is_unkown = True
        for car in self.entry_list.entry_list:
            if car_update.car_index == car.car_index:
                is_unkown = False

        last_request = datetime.datetime.now() - self._last_time_requested
        if is_unkown and last_request.total_seconds() >= 1:
            self.request_entry_list()
            self._last_time_requested = datetime.datetime.now()

        elif not is_unkown:
            self.update_leaderboard(car_update)

    def add_to_leaderboard(self) -> None:

        self._udp_data["entries"].clear()

        for entry in self.entry_list.entry_list:
            self._udp_data["entries"].update({entry.car_index: {}})

    def update_leaderboard(self, data: RealTimeCarUpdate) -> None:

        entry_list = self.entry_list.entry_list

        entry_index = -1
        for index, entry in enumerate(entry_list):
            if entry.car_index == data.car_index:
                entry_index = index

        if entry_index >= 0 and len(entry_list[entry_index].drivers) > 0:
            car_info = entry_list[entry_index]
            drivers = car_info.drivers

            race_number = car_info.race_number
            cup_category = car_info.cup_category
            model_type = car_info.model_type
            team_name = car_info.team_name
            first_name = drivers[data.driver_index].first_name
            last_name = drivers[data.driver_index].last_name

        else:
            race_number = -1
            cup_category = CupCategory.National
            model_type = -1
            team_name = "Team Name"
            first_name = "First Name"
            last_name = "Last Name"

        self._udp_data["entries"][data.car_index].update(
            {
                "position": data.position,
                "car_number": race_number,
                "car_id": data.car_index,
                "cup_category": cup_category.name,
                "cup_position": data.cup_position,
                "manufacturer": model_type,
                "team": team_name,
                "driver": {
                    "first_name": first_name,
                    "last_name": last_name,
                },
                "lap": data.lap,
                "delta": data.delta,
                "current_lap": data.current_lap.lap_time_ms,
                "last_lap": data.last_lap.lap_time_ms,
                "best_session_lap": data.best_session_lap.lap_time_ms,
                "sectors": data.last_lap.splits,
                "car_location": data.car_location.name,
                "world_pos_x": data.world_pos_x,
                "world_pos_y": data.world_pos_y,
            }
        )

    def update_leaderboard_session(self) -> None:

        session = self._udp_data["session"]
        session.clear()

        session["track"] = self.track.track_name
        session["session_type"] = self.session.session_type.name
        session["session_time"] = self.session.session_time
        session["session_end_time"] = self.session.session_end_time
        session["air_temp"] = self.session.ambient_temp
        session["track_temp"] = self.session.track_temp

    def connect(self) -> None:

        msg = ByteWriter()
        msg.write_u8(1)
        msg.write_u8(4)
        msg.write_str(self._name)
        msg.write_str(self._psw)
        msg.write_i32(self._speed)
        msg.write_str(self._cmd_psw)

        print(msg.get_bytes())

        self._socket.sendto(msg.get_bytes(), (self._ip, self._port))
        self.connected = True

    def disconnect(self) -> None:

        c_id = self.registration.connection_id

        msg = ByteWriter()
        msg.write_u8(9)
        msg.write_i32(c_id)

        self._socket.sendto(msg.get_bytes(), (self._ip, self._port))

    def request_entry_list(self) -> None:

        c_id = self.registration.connection_id

        if c_id != -1:

            msg = ByteWriter()
            msg.write_u8(10)
            msg.write_i32(c_id)

            self._socket.sendto(msg.get_bytes(), (self._ip, self._port))

    def request_track_data(self) -> None:

        c_id = self.registration.connection_id

        msg = ByteWriter()
        msg.write_u8(11)
        msg.write_i32(c_id)

        self._socket.sendto(msg.get_bytes(), (self._ip, self._port))


if __name__ == "__main__":

    # Test zone

    info = {"name": "Ryan Rennoir", "password": "asd", "speed": 250, "cmd_password": ""}

    aui = accUpdInterface("127.0.0.1", 9000, info)
    aui.start()

    now = time.time()
    while time.time() < now + 3:
        data = aui.udp_data
        if data:
            print(data["entries"])
    aui.stop()
