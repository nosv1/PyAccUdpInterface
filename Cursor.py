import struct
import sys


class Cursor:

    def __init__(self, byte: bytes):
        self._cursor = 0
        self._byte_array = byte

    def read_u8(self) -> int:

        data = self._byte_array[self._cursor : self._cursor + 1]
        self._cursor += 1

        return int.from_bytes(data, byteorder=sys.byteorder, signed=False)

    def read_u16(self) -> int:

        data = self._byte_array[self._cursor : self._cursor + 2]
        self._cursor += 2

        return int.from_bytes(data, byteorder=sys.byteorder, signed=False)

    def read_u32(self) -> int:

        data = self._byte_array[self._cursor : self._cursor + 4]
        self._cursor += 4

        return int.from_bytes(data, byteorder=sys.byteorder, signed=False)

    def read_i8(self) -> int:

        data = self._byte_array[self._cursor : self._cursor + 1]
        self._cursor += 1

        return int.from_bytes(data, byteorder=sys.byteorder, signed=True)

    def read_i16(self) -> int:

        data = self._byte_array[self._cursor : self._cursor + 2]
        self._cursor += 2

        return int.from_bytes(data, byteorder=sys.byteorder, signed=True)

    def read_i32(self) -> int:

        data = self._byte_array[self._cursor : self._cursor + 4]
        self._cursor += 4

        return int.from_bytes(data, byteorder=sys.byteorder, signed=True)

    def read_f32(self) -> float:

        data = self._byte_array[self._cursor : self._cursor + 4]
        self._cursor += 4

        return struct.unpack("<f", data)[0]

    def read_string(self) -> str:

        length = self.read_u16()

        string = self._byte_array[self._cursor : self._cursor + length]
        self._cursor += length

        # ACC doesn't support unicode emoji (and maybe orther
        # unicode charactere)
        # so if an emoji is in a name it put garbage bytes...
        # 6 bytes of trash idk why, so I ingore them
        return string.decode("utf-8", errors="ignore")
