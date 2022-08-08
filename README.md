# structex

A simple Python 3.10 library that allows you to access structured data from binary data.

## Usage
Define `Struct`s with either sequential or fixed layout and initialize them with a memory interface (e.g. to a byte-buffer) and address (e.g. an offset into a byte-buffer). Add `IField` class-variables (e.g. `FixedString` or `Primitive`) to `Struct`s to make them accessible and automatically (de-)serialize data upon access.

### Structs
Sequential structs calculate their size and the offsets of their fields themselves at runtime. Fixed structs require their fields to have offsets specified explicitely.

Here's an example of the [IMAGE_SECTION_HEADER](https://docs.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-image_section_header) structure ported to structex:

```python
class IMAGE_SECTION_HEADER(Struct):
    _layout: StructLayout = StructLayout.Sequential

    Name: str = FixedString(8)
    VirtualSize: int = Primitive(uint32_t) 
    VirtualAddress: int = Primitive(uint32_t) 
    SizeOfRawData: int = Primitive(uint32_t) 
    PointerToRawData: int = Primitive(uint32_t) 
    PointerToRelocations: int = Primitive(uint32_t) 
    PointerToLinenumbers: int = Primitive(uint32_t) 
    NumberOfRelocations: int = Primitive(uint16_t) 
    NumberOfLinenumbers: int = Primitive(uint16_t) 
    Characteristics: int = Primitive(uint32_t) 
```

Structs have a set of special class-variables:

* `_size: int`: If unspecified (`None`), structs calculate their size themselves (once per type). If specified, the given value is used in internal calculations instead. (Default: `None`)
* `_layout: StructLayout`: Specifies the type of struct layout to use for offset and size computation. (Default: `Fixed`)

### Fields
There are various types of fields available in structex. By making use of the `__get__` and `__set__` dunders, they implement some logic to read and write data. There's a collection of fields implemented in structex:

* `Primitive`: Wraps Python's built-in `struct` library to read/write primitive data-types (signed & unsigned integers of 8/16/32/64 bits of length, float & double).
* `FixedString`: Reads/writes a string of fixed length (in bytes).
* `Array`: An array of arbitrary (static) length, its elements' type is subclass of either `IField` or `Struct`.
* `Instance`: An instance of a struct inside another struct. Must not form a cyclic relationship between types!
* `Pointer`: Reads a pointer to a subclass of either a `IField` or `Struct` element.