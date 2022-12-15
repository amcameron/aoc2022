"""Simplify elves' assignments."""

def subrange(sub, container):
    if not sub:
        # empty range is everywhere
        return True
    if not container:
        # empty range contains nothing
        return False
    if len(sub) > 1 and sub.step % container.step:
        return False
    return sub.start in container and sub[-1] in container


def parse_and_test_line(l):
    elf1, elf2 = l.strip().split(',')
    e1first, e1last = map(int, elf1.split('-'))
    e2first, e2last = map(int, elf2.split('-'))
    elf1 = range(e1first, e1last + 1)
    elf2 = range(e2first, e2last + 1)
    return subrange(elf1, elf2) or subrange(elf2, elf1)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('filename')
    args = p.parse_args()

    with open(args.filename, 'r') as f:
        count = sum(1 for line in f if parse_and_test_line(line))
        print(f"This many pairs were redundant: {count}")
