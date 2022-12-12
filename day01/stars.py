"""summarize elf calorie inventories

Partitions file by empty lines and takes the sum of each partitio."""


def parse_elfs(lines):
    lines = iter(lines)
    try:
        # iterators are always True, so StopIteration is the only way out.
        while True:
            sum = 0
            while (line := next(lines).strip()):
                sum += int(line)
            yield sum
    except StopIteration:
        # Last sum gets interrupted, so yield it now.
        yield sum
        return


def _example():
    lines = ['10', '20', '', '5', '', '100', '500', '1000']
    print(list(parse_elfs(lines)))
    # expect: [30, 5, 1600]


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('filename')
    args = p.parse_args()
    if args.filename:
        with open(args.filename, 'r') as f:
            elfs = list(parse_elfs(f))
        print(f'found {len(elfs)} elfs with max cals: {max(elfs)}')
        top3cals = sum(sorted(elfs, reverse=True)[:3])
        print(f'top 3 elfs are holding: {top3cals} cals')
