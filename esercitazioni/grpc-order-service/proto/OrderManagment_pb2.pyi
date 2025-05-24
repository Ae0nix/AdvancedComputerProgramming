from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Order(_message.Message):
    __slots__ = ("id", "itemList", "description", "price", "destination")
    ID_FIELD_NUMBER: _ClassVar[int]
    ITEMLIST_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    itemList: _containers.RepeatedScalarFieldContainer[str]
    description: str
    price: float
    destination: str
    def __init__(self, id: _Optional[str] = ..., itemList: _Optional[_Iterable[str]] = ..., description: _Optional[str] = ..., price: _Optional[float] = ..., destination: _Optional[str] = ...) -> None: ...

class Shipment(_message.Message):
    __slots__ = ("id", "state", "orderList")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ORDERLIST_FIELD_NUMBER: _ClassVar[int]
    id: str
    state: str
    orderList: _containers.RepeatedCompositeFieldContainer[Order]
    def __init__(self, id: _Optional[str] = ..., state: _Optional[str] = ..., orderList: _Optional[_Iterable[_Union[Order, _Mapping]]] = ...) -> None: ...

class StringMessage(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...
