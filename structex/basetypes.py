from abc import ABC
from enum import Enum
import struct
from typing import Any, List, Type
import inspect

from structex.common import IMemory, ISerializable, IMemObject

class IField(ABC):
    def __init__(self, offset: int = None) -> None:
        self._offset = offset

    @property
    def offset(self) -> int:
        return self._offset

    @offset.setter
    def offset(self, value: int) -> None:
        self._offset = value

    def __set_name__(self, owner: Type['Struct'], name):
        if owner._layout == StructLayout.Fixed or self.offset is not None:
            return

        if not owner._size:
            owner._size = 0
        
        self.offset = owner._size
        owner._size += self.get_size()

    def __get__(self, obj: 'Struct', objtype=None) -> Any:
        return self.get_value(obj.mem, obj.offset + self._offset)

    def __set__(self, obj: 'Struct', value):
        self.set_value(obj.mem, obj.offset + self._offset, value)

    def get_value(self, mem: IMemory, address: int) -> Any:
        raise NotImplementedError
        
    def set_value(self, mem: IMemory, address: int, value: Any) -> None:
        raise NotImplementedError

    def get_size(self) -> int:
        raise NotImplementedError

class StructLayout(Enum):
    Fixed = 0
    Sequential = 1

class Struct(IMemObject):
    _size: int = None
    _layout : StructLayout = StructLayout.Fixed
    
    def __init__(self, mem: IMemory, offset: int) -> None:
        super().__init__(mem, offset)
        self.get_size()

    @classmethod
    def get_size(cls) -> int:
        if not cls._size:
            match cls._layout:
                case StructLayout.Fixed:                    
                    fields : List[IField] = [value for _, value in inspect.getmembers(cls, lambda fv: isinstance(fv, IField))]
                    largest = max(fields, key = lambda value: value.offset + value.get_size())
                    cls._size = largest.offset + largest.get_size()
                case StructLayout.Sequential:
                    # fields : List[IField] = inspect.getmembers(cls, lambda fv: isinstance(fv, IField))
                    # offset = 0
                    # for name, field in fields:
                    #     field.offset = offset
                    #     offset += field.get_size()
                    # cls._size = offset
                    pass
                case _:
                    raise NotImplementedError

        return cls._size


class BinarySerializable(ISerializable):
    format: str
    _size: int = None

    @classmethod
    def get_size(cls) -> int:
        if not cls._size:
            cls._size = struct.calcsize(cls.format)
        
        return cls._size

    @classmethod
    def serialize(cls, thing: Any) -> bytes:
        return struct.pack(cls.format, thing)

    @classmethod
    def deserialize(cls, data: bytes) -> Any:
        return struct.unpack(cls.format, data)[0]

class uint8_t(BinarySerializable):
    format = "B"

class int8_t(BinarySerializable):
    format = "b"

class uint16_t(BinarySerializable):
    format = "H"

class int16_t(BinarySerializable):
    format = "h"

class uint32_t(BinarySerializable):
    format = "I"

class int32_t(BinarySerializable):
    format = "i"

class uint64_t(BinarySerializable):
    format = "Q"

class int64_t(BinarySerializable):
    format = "q"

class float32_t(BinarySerializable):
    format = "f"

class float64_t(BinarySerializable):
    format = "d"