import argparse


def parse_argv(argv: list):
    parser = argparse.ArgumentParser(
        prog="GZPDHB",
        description="Copyright by 'Team of full D.'\nAll rights reserved.")

    parser.add_argument("-of", "--output-functions")
    parser.add_argument("-od", "--output-directives")
    parser.add_argument("-ot", "--output-types")

    parser.add_argument("-b", "--bonus") #  Придумать надо будет

    # Аргументы для входного и выходного файла
    parser.add_argument("-f", "--input-file")
    parser.add_argument("-j", "--json")

    return parser
