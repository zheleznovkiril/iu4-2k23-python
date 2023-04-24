from dataclasses import dataclass, asdict
from typing import Union
import json


@dataclass
class CommonCTypeClass:
    """
    Базовый класс, от которого будут наследоваться другие классы.
    Содержит общие методы и свойства, необходимые для работы классов-наследников.
    """
    string_number: int
    name: str


@dataclass
class Function(CommonCTypeClass):
    arguments: list
    return_type: str


@dataclass
class Typedef(CommonCTypeClass):
    type: str
    struct_types: list[str] = None


@dataclass
class Directive(CommonCTypeClass):
    value: str


@dataclass
class CHeaderView:
    functions: list[Function] = None
    typedefs: list[Typedef] = None
    directives: list[Directive] = None

    def append_element(self, element: Union[Function, Typedef, Directive]):
        if isinstance(element, Function):
            self.functions.append(element)
        elif isinstance(element, Typedef):
            self.typedefs.append(element)
        elif isinstance(element, Directive):
            self.directives.append(element)
        else:
            raise TypeError(
                f"Invalid element type. Only Function, Typedef or Directive objects are allowed. "
                f"Got {type(element)} instead."
            )

    @staticmethod
    def from_dict(input_dict: dict):
        functions = [Function(**functions_dict) for functions_dict in input_dict.get("functions", [])]
        typedefs = [Typedef(**typedefs_dict) for typedefs_dict in input_dict.get("typedefs", [])]
        directives = [Directive(**directives_dict) for directives_dict in input_dict.get("directives", [])]
        return CHeaderView(functions=functions, typedefs=typedefs, directives=directives)

    def print_functions(self):
        dict_c_header = asdict(self)
        data = json.dumps(dict_c_header['functions'], indent=4)
        print('\'functions\' = ' + data)

    def print_types(self):
        dict_c_header = asdict(self)
        data = json.dumps(dict_c_header['typedefs'], indent=4)
        print('\'types\' = ' + data)

    def print_directives(self):
        dict_c_header = asdict(self)
        data = json.dumps(dict_c_header['directives'], indent=4)
        print('\'directives\' = ' + data)

    def print_structures(self):
        dict_c_header = asdict(self)
        print('\'structures\' = ', end='')
        for it in dict_c_header['typedefs']:
            if it['type'] == 'struct':
                print(json.dumps(it, indent=4))
