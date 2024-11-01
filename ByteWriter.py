import struct
import sys


class ByteWriter:

    def __init__(self) -> None:
        self.bytes_array = b""

    def write_u8(self, data: int) -> None:
        self.bytes_array += (data).to_bytes(1, sys.byteorder, signed=False)

    def write_u16(self, data: int) -> None:
        self.bytes_array += (data).to_bytes(2, sys.byteorder, signed=False)

    def write_u32(self, data: int) -> None:
        self.bytes_array += (data).to_bytes(4, sys.byteorder, signed=False)

    def write_i16(self, data: int) -> None:
        self.bytes_array += (data).to_bytes(2, sys.byteorder, signed=True)

    def write_i32(self, data: int) -> None:
        self.bytes_array += (data).to_bytes(4, sys.byteorder, signed=True)

    def write_f32(self, data: float) -> None:
        self.bytes_array += struct.pack("<f", data)[0]

    def write_str(self, data: str) -> None:
        # ACC does support unicode emoji but I do, hehe 😀
        byte_data = data.encode("utf-8")
        self.write_u16(len(byte_data))
        self.bytes_array += byte_data

    def get_bytes(self) -> bytes:
        return self.bytes_array
