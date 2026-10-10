# PyAccUdpInterface

ACC UDP interface listener written in python 😀.

## Usage

Basic code example.

```py
    # Setup basic information
    info = {
        "name": "Ryan Rennoir",
        "password": "asd",
        "speed": 250,
        "cmd_password": ""
    }

    # Create UDP listener instance
    aui = accUpdInterface("127.0.0.1", 9000, info)

    aui.start()

    while condition:
        # Receive most latest data available
        data = aui.udp_data # Return a dict

    # Close listener process and socket
    aui.stop()
```

## Data structure

Kunos don't give any documentation on their udp interface except the code example they give and I'm too lazy to write one myself 😅

```py
{
    "connection": {
        "id": ...,
        "connected": ...
    },
    "entries": {},
    "session": {
        "track": "None",
        "session_type": ...,
        "session_time": ...,
        "session_end_time": ...,
        "air_temp": ...,
        "track_temp": ...
    },
}
```

## Provided Files

### RealTimeUpdate.py

Handles real-time updates from the UDP interface.

#### Class: RealTimeUpdate

- `event_index`: int
- `session_index`: int
- `session_type`: SessionType
- `phase`: SessionPhase
- `session_time`: datetime
- `session_end_time`: datetime
- `focused_car_index`: int
- `active_camera_set`: str
- `active_camera`: str
- `current_hud_page`: str
- `is_replay_playing`: bool
- `replay_session_time`: datetime
- `replay_remaining_time`: datetime
- `time_of_day`: datetime
- `ambient_temp`: int
- `track_temp`: int
- `best_session_lap`: LapInfo

### RealTimeCarUpdate.py

Handles real-time car updates from the UDP interface.

#### Class: RealTimeCarUpdate

- `car_index`: int
- `driver_index`: int
- `driver_count`: int
- `gear`: int
- `world_pos_x`: float
- `world_pos_y`: float
- `yaw`: float
- `car_location`: CarLocation
- `kmh`: int
- `position`: int
- `cup_position`: int
- `track_position`: int
- `spline_position`: float
- `lap`: int
- `delta`: int
- `best_session_lap`: LapInfo
- `last_lap`: LapInfo
- `current_lap`: LapInfo

### PyAccUdpInterface.py

Main interface for setting up and managing the UDP listener.

#### Class: accUpdInterface

- `registration`: Registration
- `session`: RealTimeUpdate
- `track`: TrackData
- `entry_list`: EntryList
- `connected`: bool
- `_name`: str
- `_psw`: str
- `_speed`: int
- `_cmd_psw`: str
- `_udp_data`: dict
- `_socket`: socket
- `_ip`: str
- `_port`: int
- `_last_time_requested`: datetime
- `_last_connection`: datetime
- `child_pipe`: Pipe
- `parent_pipe`: Pipe
- `data_queue`: Queue
- `udp_interface_listener`: Process

### LapInfo.py

Handles lap information data structure.

#### Class: LapInfo

- `lap_time_ms`: int
- `car_index`: int
- `driver_index`: int
- `splits`: list
- `is_invalid`: bool
- `is_valid_for_best`: bool
- `late_type`: LapType
- `_cur`: Cursor

### Enums.py

Contains enumerations used throughout the project.

#### Enums

- `Nationality`: Enum
- `CarLocation`: Enum
- `DriverCategory`: Enum
- `CupCategory`: Enum
- `SessionType`: Enum
- `SessionPhase`: Enum
- `LapType`: Enum

### EntryList.py

Manages the list of car entries.

#### Class: EntryList

- `entry_list`: list[CarInfo]

### DriverInfo.py

Handles driver information data structure.

#### Class: DriverInfo

- `first_name`: str
- `last_name`: str
- `short_name`: str
- `category`: DriverCategory
- `nationality`: Nationality
- `_cur`: Cursor

### Cursor.py

Utility for reading data from byte streams.

#### Class: Cursor

- `_cursor`: int
- `_byte_array`: bytes

### CarInfo.py

Handles car information data structure.

#### Class: CarInfo

- `car_index`: int
- `model_type`: int
- `team_name`: str
- `race_number`: int
- `cup_category`: CupCategory
- `current_driver_index`: int
- `drivers`: list[DriverInfo]
- `nationality`: Nationality

### Registration.py

Handles registration data structure.

### TrackData.py

Handles track data structure.