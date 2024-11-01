from .Cursor import Cursor


class TrackData:

    def __init__(self):

        self.track_name = ""
        self.track_id = -1
        self.track_meters = -1

        self.camera_sets = {}
        self.hud_page = []

    def update(self, cur: Cursor):

        _ = cur.read_i32()  # Connection id
        self.track_name = cur.read_string()
        self.track_id = cur.read_i32()
        self.track_meters = cur.read_i32()

        self.camera_sets: dict[str, list] = {}
        camera_set_count = cur.read_u8()
        for _ in range(camera_set_count):

            camera_set_name = cur.read_string()
            self.camera_sets.update({camera_set_name: []})

            camera_count = cur.read_u8()
            for _ in range(camera_count):
                camera_name = cur.read_string()
                self.camera_sets[camera_set_name].append(camera_name)

        self.hud_page = []
        hud_page_count = cur.read_u8()
        for _ in range(hud_page_count):
            self.hud_page.append(cur.read_string())
