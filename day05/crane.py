"""Help the elves with their crane."""

from typing import Iterator


example_input = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

 move 1 from 2 to 1
 move 3 from 1 to 3
 move 2 from 2 to 1
 move 1 from 1 to 2"""

example_output = """\
        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3"""


Stacks = tuple[list[str], ...]


def parse_stacks(lines: Iterator[str]) -> Stacks:
    stacks: Stacks = tuple()
    while line := next(lines, '').rstrip('\n'):
        # Assume that the input stacks are padded with whitespace, so you don't
        # need to worry about dynamically adjusting the amount of stacks. You
        # can read it once.
        # But how does stack count relate to line length?
        # Each stack uses 3 characters for a crate, and every pair of stacks
        # has one character separating them: "[E] [G]". So for n fields there
        # are 3n characters + (n - 1) separator characters, for a total of
        # len(line) = 4n - 1 characters. Therefore:
        if not stacks:
            num_stacks = (len(line) + 1) // 4
            stacks = tuple(list() for _ in range(num_stacks))
        crates = [line[i:i+1].strip() for i in range(1, len(line), 4)]
        for crate, stack in zip(crates, stacks):
            if crate:
                stack.insert(0, crate)
    return stacks


def parse_move(line: str) -> tuple[int, str, str]:
    _, count, _, _from, _, _to = line.strip().split()
    return int(count), _from, _to


def apply_move(count: int, frm: str, to: str, stacks: Stacks, pt1: bool = True) -> None:
    _from = stacks[int(frm) - 1]
    _to = stacks[int(to) - 1]
    if pt1:
        for _ in range(count):
            _to.append(_from.pop())
        return
    else:
        crates = _from[-count:]
        del _from[-count:]
        _to.extend(crates)
        return


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('filename')
    args = p.parse_args()

    with open(args.filename, 'r') as f:
        stacks = parse_stacks(f)
        while line := next(f, ''):
            count, frm, to = parse_move(line)
            apply_move(count, frm, to, stacks)
        print(''.join(stack.pop() for stack in stacks))

    with open(args.filename, 'r') as f:
        stacks = parse_stacks(f)
        while line := next(f, ''):
            count, frm, to = parse_move(line)
            apply_move(count, frm, to, stacks, pt1=False)
        print(''.join(stack.pop() for stack in stacks))
