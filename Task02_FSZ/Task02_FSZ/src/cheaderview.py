from dataclasses import dataclass


class CommonCTypeClass:
    """
    Базовый класс, от которого будут наследоваться другие классы.
    Содержит общие методы и свойства, необходимые для работы классов-наследников.
    """
    def __init__(self, string_number: int, name: str):
        self.string_number = str(string_number)
        self.name = name


@dataclass
class Function(CommonCTypeClass):
    arguments: list
    return_type: str

    def __dict__(self):
        return {
            "string": self.string_number,
            "name": self.name,
            "return type": self.return_type,
            "arguments": self.arguments,
            "parse type": "function"
        }


@dataclass
class Typedef(CommonCTypeClass):
    type: str
    list: None

    def __dict__(self):
        typedef_dict = {
            "string": self.string_number,
            "name": self.name,
            "type": self.type,
            "parse type": "typedef"
        }
        if self.list:
            typedef_dict["struct types"] = self.list

        return typedef_dict


@dataclass
class Directive(CommonCTypeClass):
    value: str

    def __dict__(self) -> dict:
        return {
            "string": self.string_number,
            "name": self.name,
            "value": self.value,
            "parse type": "directive"
        }


def dict_to_func(input_dict: dict) -> Function:
    pass


def dict_to_typedef(input_dict: dict) -> Typedef:
    pass


def dict_to_directive(input_dict: dict) -> Directive:
    pass


@dataclass()
class CHeaderView:
    functions: list = None
    typedefs: list = None
    directives: list = None

    def add_func(self, func: Function):
        self.functions.append(func)

    def add_typedef(self, typed: Typedef):
        self.typedefs.append(typed)

    def add_directive(self, directive: Directive):
        self.directives.append(directive)

    def __dict__(self) -> dict:
        c_header_dict = {}
        for it in self.functions:
            c_header_dict[it.string_number] = dict(it)
        for it in self.typedefs:
            c_header_dict[it.string_number] = dict(it)
        for it in self.directives:
            c_header_dict[it.string_number] = dict(it)
        return dict(sorted(c_header_dict.items()))

    def dict_to_c_header_view(self, input_dict: dict):
        self.functions = []
        self.typedefs = []
        self.directives = []
        for key, value in input_dict:
            if value["parse type"] == "function":
                self.functions.append(dict_to_func(value))
            elif value["parse type"] == "typedef":
                self.typedefs.append(dict_to_typedef(value))
            elif value["parse type"] == "directive":
                self.directives.append(dict_to_directive(value))
