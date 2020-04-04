from itertools import product
from random import choices
from string import ascii_lowercase
from uuid import uuid4


def bad_values_generator(values_list, separators=None):
    """"""  # todo add docstring

    if separators is None:
        separators = ['__', '%20%20', '.', '-', '']

    new_values = [str(uuid4())[:8], '{}']

    for value, sep in product(filter(lambda x: ' ' in x, values_list), separators):
        new_values.append(value.lower().replace(' ', sep))

    for value in filter(lambda x: ' ' not in x, values_list):
        new_values.append(''.join(choices(ascii_lowercase, k=2)) + value.lower())
        new_values.append(value.lower() + ''.join(choices(ascii_lowercase, k=2)))

    return new_values


# if __name__ == '__main__':
#     print(bad_values_generator(['Bb', 'cc eee', 'aa', 'Ff Tttt']))
