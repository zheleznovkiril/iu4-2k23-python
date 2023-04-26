import pytest
from src.jsonmod import CHeaderJSON


@pytest.mark.parametrize("json_input_file, json_output_file",
                         ["test_json.json", "test_output_json.json"])
def test_json(json_input_file: str, json_output_file: str):
    c_header_json = CHeaderJSON.from_json(json_input_file)
    c_header_json.write_data_to_json(json_output_file)

    with open(json_input_file, 'r') as file:
        input_data = file.read()

    with open(json_output_file, 'r') as file:
        output_data = file.read()

    assert input_data == output_data
