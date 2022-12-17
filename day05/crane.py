"""Help the elves with their crane."""

from collections import deque


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
print(example_output)


def parse_stacks(lines):
    one, two, three = deque(), deque(), deque()
    while line := next(lines, ''):
        _1, _2, _3 = line[1:2].strip(), line[5:6].strip(), line[9:10].strip()
        _1 and one.appendleft(_1)
        _2 and two.appendleft(_2)
        _3 and three.appendleft(_3)
    return one, two, three
