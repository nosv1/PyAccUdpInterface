from .Cursor import Cursor


class Registration:

    def __init__(self):

        self.connection_id = -1
        self.connection_succes = False
        self.is_read_only = False
        self.error_msg = "Not Initialized yet"

    def update(self, cur: Cursor):

        self.connection_id = cur.read_i32()
        self.connection_succes = cur.read_u8() > 0
        self.is_read_only = cur.read_u8() == 0
        self.error_msg = cur.read_string()
