from dataclasses import dataclass


@dataclass
class DefinedStructBase:
    name: str
    type: str
    namespace: str


@dataclass
class DefinedStructEnum(DefinedStructBase):
    underlying: str
    flags: bool
    values: dict[str, int]


@dataclass
class DefinedStructFuncParam:
    name: str
    type: str

    def __post_init__(self) -> None:
        if self.type == '__fastcall':
            self.type = '__int64'


@dataclass
class DefinedStructVFunc:
    name: str
    return_type: str | None
    offset: int
    parameters: list[DefinedStructFuncParam]


@dataclass
class DefinedStructMemFunc:
    signature: str
    return_type: str
    parameters: list[DefinedStructFuncParam]
    name: str

@dataclass
class DefinedStructField(DefinedStructFuncParam):
    offset: int
    base: bool


@dataclass
class DefinedStructFuncField(DefinedStructField):
    return_type: str | None
    params: list[DefinedStructFuncParam] | None

    # The original version of this function had a params kwarg but stored as parameters
    @property
    def parameters(self) -> list[DefinedStructFuncParam] | None:
        return self.params


@dataclass
class DefinedStructStaticMember:
    signature: str
    relative_offsets: list[int]
    return_type: str
    is_pointer: bool


@dataclass
class DefinedStructFixedField(DefinedStructField):
    size: str | None


class DefinedStructFixedFieldOld(DefinedStructField, object):
    def __init__(self, name, type, offset, base, size):
        # type: (str, str, int, bool, str | None) -> None
        super(DefinedStructFixedField, self).__init__(name, type, offset, base)
        self.size = size

@dataclass
class DefinedStruct(DefinedStructBase):
    fields: list[DefinedStructField]
    size: int | None
    vtable_size: int | None
    virtual_functions: list[DefinedStructVFunc] | None
    member_functions: list[DefinedStructMemFunc]
    union: bool
    static_member_functions: list[DefinedStructMemFunc] | None
    static_members: list[DefinedStructStaticMember] | None

    def __post_init__(self) -> None:
        self.union = bool(self.union)


@dataclass
class DefinedStructExport:
    enums: list[DefinedStructEnum]
    structs: list[DefinedStruct]
