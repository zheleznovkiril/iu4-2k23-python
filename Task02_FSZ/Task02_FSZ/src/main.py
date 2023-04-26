import sys
from argsparser import parse_command_line
from jsonmod import CHeaderJSON
from cheaderview import CHeaderView
from cheaderparser import parse_header_file


def main():
    argparse_result = parse_command_line(standalone_mode=False)

    if argparse_result['input_file'].endswith('.h'):
        c_header_view = parse_header_file(argparse_result['input_file'])
    elif argparse_result['input_file'].endswith('.json'):
        c_header_view = CHeaderView.from_dict(CHeaderJSON.from_json(argparse_result['input_file']).json_data)
    else:
        return -1

    if argparse_result['output_functions'] is True:
        c_header_view.print_functions()

    if argparse_result['output_types'] is True:
        c_header_view.print_types()

    if argparse_result['output_directives'] is True:
        c_header_view.print_directives()

    if argparse_result['output_structures'] is True:
        c_header_view.print_structures()

    c_header_json = CHeaderJSON.from_c_header_view(c_header_view)
    c_header_json.write_data_to_json(argparse_result['output_file'])


if __name__ == "__main__":
    sys.exit(main())
