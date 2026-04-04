from __future__ import annotations


def get_definition(schema: dict[str, str]) -> Definition:
    if "type" in schema:
        if schema["type"] == "array":
            return RepeatDefinition(schema)
    return Definition(schema)


class Definition:
    def __init__(self, obj: dict[str, str]) -> None:
        self.name = obj["name"]
        if "pendingName" in obj:
            self.pendingName = obj["pendingName"]

    def get_name(self) -> str:
        if hasattr(self, "pendingName"):
            return self.pendingName
        else:
            return self.name

    def __repr__(self) -> str:
        return self.name


class RepeatDefinition(Definition):
    def __init__(self, obj: dict[str, str]) -> None:
        super().__init__(obj)
        self.obj = obj
        self.count = obj["count"]
        self.inner_defs = []
        self.process_inner()

    def process_inner(self) -> None:
        if "fields" in self.obj:
            for field in self.obj["fields"]:
                if "name" in field:
                    self.inner_defs.append(get_definition(field))
                else:
                    self.inner_defs.append(Definition({"name": ""}))
        if self.inner_defs == []:
            self.inner_defs.append(Definition({"name": ""}))

    def flatten(self, extern: str) -> list[Definition]:
        defs = []
        extern = extern + self.name
        for i in range(0, int(self.count)):
            for inner in self.inner_defs:
                if isinstance(inner, RepeatDefinition):
                    defs.extend(inner.flatten(extern + i.__str__()))
                else:
                    defs.append(Definition({"name": extern + i.__str__() + inner.name}))
        return defs

    def __repr__(self) -> str:
        return '\n'.join([repr(x) for x in self.flatten("")])


class SemanticVersion:
    """Represents a semantic version string that can compare versions"""

    def __init__(self, year: int, month: int, date: int, patch: int, build: int = 0):
        self.year = year
        self.month = month
        self.date = date
        self.patch = patch
        self.build = build

    def __lt__(self, other: SemanticVersion) -> bool:
        return (
            self.year < other.year
            or self.month < other.month
            or self.date < other.date
            or self.patch < other.patch
            or self.build < other.build
        )

    def __repr__(self) -> str:
        return "{0}.{1}.{2}.{3}.{4}".format(
            self.year,
            self.month.__str__().rjust(2, "0"),
            self.date.__str__().rjust(2, "0"),
            self.patch.__str__().rjust(4, "0"),
            self.build.__str__().rjust(4, "0"),
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, SemanticVersion):
            return False
        return (
            self.year == __value.year
            and self.month == __value.month
            and self.date == __value.date
            and self.patch == __value.patch
            and self.build == __value.build
        )

    def __hash__(self) -> int:
        return hash(repr(self))
