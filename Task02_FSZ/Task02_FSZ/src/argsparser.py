import click


def is_valid_input_file(value):
    if not value.endswith('.h') and not value.endswith('.json'):
        raise click.BadParameter('Входной файл должен иметь расширение .h или .json')
    else:
        return value


def is_valid_output_file(value):
    if not value.endswith('.json'):
        raise click.BadParameter('Выходной файл должен иметь расширение .json')
    else:
        return value


@click.command()
@click.option('-f', '--input-file', type=click.Path(exists=True), required=True, help='Имя входного файла')
@click.option('-j', '--output-file', required=True, help='Имя выходного JSON файла')
@click.option('-os', '--output-structures', is_flag=True, help='Вывести список всех структур (бонус 2)')
@click.option('-of', '--output-functions', is_flag=True, help='Вывести список всех функций')
@click.option('-od', '--output-directives', is_flag=True, help='Вывести список всех директив компилятора')
@click.option('-ot', '--output-types', is_flag=True, help='Вывести список всех объявлений типов')
@click.pass_context
def parse_command_line(ctx, **kwargs) -> dict:
    is_valid_input_file(kwargs['input_file'])
    is_valid_output_file(kwargs['output_file'])

    return kwargs
