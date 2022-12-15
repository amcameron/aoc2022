"""Help elves repack their backpacks."""

import string


_lowers_then_uppers = ''.join((string.ascii_lowercase, string.ascii_uppercase))
_priorities = dict(zip(_lowers_then_uppers, range(1, 53)))


def split_into_compartments(backpack):
    assert not len(backpack) % 2, f"Illegal backpack with length {len(backpack)}: {backpack}"
    half = len(backpack) // 2
    return backpack[:half], backpack[half:]


def split_into_groups(elves):
    try:
        while True:
            yield (next(elves).strip(), next(elves).strip(),
                   next(elves).strip())
    except StopIteration:
        return


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('filename')
    args = p.parse_args()

    with open(args.filename, 'r') as f:
        print("Part 1:")
        print(sum(_priorities[set(_lowers_then_uppers).intersection(*split_into_compartments(line.strip())).pop()]
                  for line in f))
        f.seek(0)
        print("\nPart 2:")
        print(sum(_priorities[set(_lowers_then_uppers).intersection(*elves).pop()]
                  for elves in split_into_groups(f)))
