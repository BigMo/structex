from abc import ABC
from typing import Any

class ISerializable(ABC):
    @classmethod
    def serialize(cls, thing: Any) -> bytes:
        raise NotImplementedError
        
    @classmethod
    def deserialize(cls, data: bytes) -> Any:
        raise NotImplementedError

    @classmethod
    def get_size(cls) -> int:
        raise NotImplementedError

class IMemory(ABC):
    def read(self, address: int, count: int) -> bytes:
        raise NotImplementedError
        
    def write(self, address: int, data: bytes) -> None:
        raise NotImplementedError

class IMemObject(ABC):
    def __init__(self, mem: IMemory, offset: int) -> None:
        self._offset = offset
        self._mem = mem

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def mem(self) -> IMemory:
        return self._mem