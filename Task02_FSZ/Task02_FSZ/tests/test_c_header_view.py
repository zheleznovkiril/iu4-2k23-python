import pytest
from src.jsonmod import CHeaderJSON
from src.cheaderview import CHeaderView, Function
from src.cheaderparser import parse_header_file


@pytest.mark.parametrize("h_input_file, expected_data_file",
                         ["test_h_file.h", "test_json.json"]
                         )
def test_parse_header_file(h_input_file: str, expected_data_file: str):
    c_header_view_input = parse_header_file(h_input_file)

    c_header_json_expected = CHeaderJSON.from_json(expected_data_file)
    c_header_view_expected = CHeaderView.from_dict(c_header_json_expected.json_data)

    assert c_header_view_input == c_header_view_expected


@pytest.mark.parametrize("input_dict, c_header_view_expected",
                         [{"functions": [
                             {
                                 "string_number": 10,
                                 "name": "add",
                                 "arguments": [
                                     "int",
                                     "int"
                                 ],
                                 "return_type": "int"
                             }]},
                             CHeaderView(functions=(Function(
                                 string_number=10,
                                 name='add',
                                 arguments=['int', 'int'],
                                 return_type='int'
                             )))]
                         )
def test_c_header_view_from_dict(input_dict: dict, c_header_view_expected: CHeaderView):
    c_header_view_test = CHeaderView.from_dict(input_dict)

    assert c_header_view_test == c_header_view_expected
