from dataclasses import dataclass


@dataclass
class DefinedStructBase:
    name: str
    type: str
    namespace: str

class DefinedStructBaseOld:
    def __init__(self, name, type, namespace):
        # type: (str, str, str) -> None
        self.name = name
        self.type = type
        self.namespace = namespace


@dataclass
class DefinedStructEnum(DefinedStructBase):
    underlying: str
    flags: bool
    values: dict[str, int]


class DefinedStructEnumOld(DefinedStructBase, object):
    def __init__(self, name, type, underlying, namespace, flags, values):
        # type: (str, str, str, str, bool, dict[str, int]) -> None
        super(DefinedStructEnum, self).__init__(name, type, namespace)
        self.name = name
        self.type = type
        self.values = values
        self.flags = flags
        self.underlying = underlying


@dataclass
class DefinedStructFuncParam:
    name: str
    type: str

    def __post_init__(self) -> None:
        if self.type == '__fastcall':
            self.type = '__int64'


class DefinedStructFuncParamOld:
    def __init__(self, name, type):
        # type: (str, str) -> None
        self.name = name
        if type == "__fastcall":
            self.type = "__int64"
        else:
            self.type = type

@dataclass
class DefinedStructVFunc:
    name: str
    return_type: str | None
    offset: int
    parameters: list[DefinedStructFuncParam]


class DefinedStructVFuncOld:
    def __init__(self, name, return_type, offset, parameters):
        # type: (str, str, int, list[DefinedStructFuncParam]) -> None
        self.name = name
        self.return_type = return_type
        self.offset = offset
        self.parameters = parameters


@dataclass
class DefinedStructMemFunc:
    signature: str
    return_type: str
    parameters: list[DefinedStructFuncParam]
    name: str

class DefinedStructMemFuncOld:
    def __init__(self, signature, return_type, parameters, name):
        # type: (str, str, list[DefinedStructFuncParam], str) -> None
        self.signature = signature
        self.return_type = return_type
        self.parameters = parameters
        self.name = name


@dataclass
class DefinedStructField(DefinedStructFuncParam):
    offset: int
    base: bool

class DefinedStructFieldOld(DefinedStructFuncParam, object):
    def __init__(self, name, type, offset, base):
        # type: (str, str, int, bool) -> None
        super(DefinedStructField, self).__init__(name, type)
        self.offset = offset
        self.base = base


@dataclass
class DefinedStructFuncField(DefinedStructField):
    return_type: str | None
    params: list[DefinedStructFuncParam] | None

    # The original version of this function had a params kwarg but stored as parameters
    @property
    def parameters(self) -> list[DefinedStructFuncParam] | None:
        return self.params

class DefinedStructFuncFieldOld(DefinedStructField, object):
    def __init__(self, name, type, offset, base, return_type, params):
        # type: (str, str, int, bool, str | None, list[DefinedStructFuncParam] | None) -> None
        super(DefinedStructFuncField, self).__init__(name, type, offset, base)
        self.return_type = return_type
        self.parameters = params


@dataclass
class DefinedStructStaticMember:
    signature: str
    relative_offsets: list[int]
    return_type: str
    is_pointer: bool

class DefinedStructStaticMemberOld:
    def __init__(self, signature, relative_offsets, return_type, is_pointer):
        # type: (str, list[int], str, bool) -> None
        self.signature = signature
        self.relative_offsets = relative_offsets
        self.return_type = return_type
        self.is_pointer = is_pointer


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


class DefinedStructOld(DefinedStructBase, object):
    def __init__(
        self,
        name, # str
        type, # str
        namespace, # str
        # new
        fields, # list[DefinedStructField]
        size, # int | None
        vtable_size, # int | None
        virtual_functions, # list[DefinedStructVFunc] | None
        member_functions, # list[DefinedStructMemFunc]
        union, # str
        static_member_functions, # list[DefinedStructMemFunc] | None,
        static_members, # list[DefinedStructStaticMember] | None
    ):
        # type: (str, str, str, list[DefinedStructField], int | None, int | None, list[DefinedStructVFunc] | None, list[DefinedStructMemFunc], str, list[DefinedStructMemFunc] | None, list[DefinedStructStaticMember] | None) -> None
        super(DefinedStruct, self).__init__(name, type, namespace)
        self.fields = fields
        self.size = size
        self.vtable_size = vtable_size
        self.virtual_functions = virtual_functions
        self.member_functions = member_functions
        self.union = bool(union)
        self.static_member_functions = static_member_functions
        self.static_members = static_members



@dataclass
class DefinedStructExport:
    enums: list[DefinedStructEnum]
    structs: list[DefinedStruct]

class DefinedStructExportOld:
    def __init__(self, enums, structs):
        # type: (list[DefinedStructEnum], list[DefinedStruct]) -> None
        self.enums = enums
        self.structs = structs
