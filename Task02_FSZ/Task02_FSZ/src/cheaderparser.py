import re
from cheaderview import CHeaderView


def parse_header_file(filename: str) -> CHeaderView:
    with open(filename, 'r') as f:
        header_data = f.read()

    function_regex = re.compile(r'([\w\s*]+)\s+(\w+)\s*\((.*)\);')
    typedef_regex = re.compile(r'typedef\s+([\w\s*]+)\s+(\w+)\s*;')

    functions = []
    typedefs = []
    directives = []

    for it, line in enumerate(header_data.split('\n')):
        match = function_regex.search(line)
        if match:
            return_type, name, args = match.groups()
            arg_types = [arg.strip().split()[0] for arg in args.split(',')] if args else []
            functions.append({
                'name': name,
                'string_number': it+1,
                'return_type': return_type.strip(),
                'arguments': arg_types
            })
            continue

        match = typedef_regex.search(line)
        if match:
            type_name, name = match.groups()
            typedefs.append({
                'name': name,
                'string_number': it+1,
                'type': type_name.strip()
            })
            continue
            
            #MAX KIDAESH SUDA typedef and structure 

    return CHeaderView.from_dict({
        'functions': functions,
        'typedefs': typedefs,
        'directives': directives
    })
