import json
from dataclasses import dataclass, asdict
from cheaderview import CHeaderView


@dataclass
class CHeaderJSON:
    """
    Класс для работы с JSON форматом.
    """
    json_data: dict = None

    def write_data_to_json(self, file_path: str):
        with open(file_path, 'w') as file:
            json.dump(self.json_data, file, indent=4)

    @staticmethod
    def from_c_header_view(data: CHeaderView):
        json_data = asdict(data)
        return CHeaderJSON(json_data)

    @staticmethod
    def from_json(file_path: str):
        with open(file_path) as json_file:
            json_data = json.load(json_file)
        return CHeaderJSON(json_data)
