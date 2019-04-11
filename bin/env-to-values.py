import click
from yaml import dump
from dotenv import dotenv_values


@click.command()
@click.option('--env-file', required=True, type=click.File(mode='r'), help="Environment file")
@click.option('--secrets-file', required=False, type=click.File(mode='r'), help="Secrets file")
def generate(env_file, secrets_file):

    values = dotenv_values(stream=env_file.name)
    yaml_values = {}

    for key, value in values.iteritems():
        _set_value(yaml_values, key, value)

    yaml_values['environment'] = {str(k): str(v) for k, v in values.iteritems()}

    if secrets_file:
        secrets_values = dotenv_values(stream=secrets_file.name)
        yaml_values['secrets'] = {str(k): str(v) for k, v in secrets_values.iteritems()}

    print dump(yaml_values)


def _set_value(values, key, value):
    parts = list(reversed(key.split('_')))
    stack = values

    while parts:
        part = parts.pop()
        lower_part = str(part.lower())
        if len(parts) > 0:
            stack[lower_part] = stack.get(lower_part, {})
            stack = stack.get(lower_part, {})
        else:
            stack[lower_part] = str(value)


if __name__ == '__main__':
    generate()
