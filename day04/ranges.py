"""Simplify elves' assignments."""

from math import lcm


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


def ranges_overlap(r1, r2):
    step = lcm(r1.step, r2.step)
    intersection = range(max(r1.start, r2.start), min(r1.stop, r2.stop), step)
    return bool(intersection)


def parse_line(l):
    elf1, elf2 = l.strip().split(',')
    e1first, e1last = map(int, elf1.split('-'))
    e2first, e2last = map(int, elf2.split('-'))
    elf1 = range(e1first, e1last + 1)
    elf2 = range(e2first, e2last + 1)
    return elf1, elf2


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('filename')
    args = p.parse_args()

    with open(args.filename, 'r') as f:
        totals = {"contained": 0, "overlapped": 0}
        for line in f:
            elf1, elf2 = parse_line(line)
            # True -> 1, False -> 0
            totals["contained"] += int(subrange(elf1, elf2) or subrange(elf2, elf1))
            totals["overlapped"] += int(ranges_overlap(elf1, elf2))
        fmt = lambda adjective, count: f"This many pairs were {adjective}: {count}"
        for adj, c in totals.items():
            print(fmt(adj, c))
