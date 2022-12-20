"""Walk directory trees (for the elves)."""

from __future__ import annotations
from io import TextIOBase
from typing import Iterator

import re
import sys


_digits = re.compile('^\d+$')
_MAX_SIZE_PT1 = 100_000
_FILESYSTEM_CAPACITY = 70000000
_NEEDED_SPACE = 30000000


class File:
    def __init__(self, name: str, parent: Directory, size: int):
        self.name: str = name
        self.parent: Directory = parent
        self._size: int = size

    def size(self) -> int:
        return self._size


class Directory:
    traversed: bool = False
    to_visit: list[str] = []
    root: Directory | None = None

    def __init__(self, name: str, parent: Directory | None = None, children: list[Directory | File] | None = None):
        self.name: str = name
        self.parent: Directory | None = parent
        if self.parent is None:
            Directory.root = self
        if children is not None:
            self.children = children
        else:
            self.children = []

    def traverse(self) -> Iterator[File | Directory]:
        to_visit: list[File | Directory] = [self]
        while to_visit:
            next_item = to_visit.pop()
            if isinstance(next_item, Directory):
                to_visit.extend(next_item.children)
            yield next_item
        return

    def fullname(self) -> str:
        d: Directory | None = self
        path: list[str] = [self.name]
        while d := self.parent:
            path.append(d.name)
        return '/'.join(reversed(path))

    def size(self) -> int:
        return sum(c.size() for c in self.children)


def parse_history(lines: TextIOBase) -> Directory | None:
    cwd: Directory | None = None
    Directory.to_visit.append('/')
    while line := lines.readline().rstrip('\n'):
        prefix, cmd, *args = line.split()
        assert prefix == '$', "reached non-command line"
        cwd = parse_command(lines, cwd, cmd, args)
    if not Directory.to_visit:
        Directory.traversed = True
    return Directory.root


def parse_command(lines: TextIOBase, cwd: Directory | None, cmd: str, args:
                  list[str]) -> Directory | None:
    match cmd:
        case 'cd':
            assert len(args) == 1, f"received more than one arg to cd: {args}"
            return parse_cd(lines, cwd, args[0])

        case 'ls':
            assert not args, "received args to ls"
            parse_ls(lines, cwd)
            return cwd

        case _:
            raise ValueError(f"bad command: {cmd=}, {args=}")


def parse_cd(lines: TextIOBase, cwd: Directory | None, new_dir: str) -> Directory | None:
    match new_dir:
        case '..':
            # move up one directory
            if cwd is None:
                raise ValueError("tried to move up with no directory set")
            return cwd.parent
        case child if child != '/':
            assert cwd, "tried to cd into child without active cwd"
            # ensure child is in the cwd
            for ch in cwd.children:
                if ch.name == child:
                    assert isinstance(ch, Directory), "found file when expecting dir"
                    Directory.to_visit.remove(ch.name)
                    return ch
            raise ValueError(f"tried to move into nonexistent child: {child}")
        case '/':
            # we know we're at the root
            assert not cwd, "tried to cd / more than once"
            Directory.to_visit.remove('/')
            return Directory('/')
    raise ValueError(f"received nonsensical cd argument: {new_dir}")


def parse_ls(lines: TextIOBase, cwd: Directory | None) -> None:
    assert cwd, "Tried to parse ls without a cwd"
    pos: int = lines.tell()
    # iterate until next $ line
    while line := lines.readline().rstrip('\n'):
        if line.startswith('$'):
            lines.seek(pos)
            return
        pos = lines.tell()

        desc, name = line.split()
        match desc:
            case 'dir':
                new_dir = Directory(name, parent=cwd)
                cwd.to_visit.append(new_dir.name)
                cwd.children.append(new_dir)

            case size if _digits.match(size):
                new_file = File(name, cwd, int(size))
                cwd.children.append(new_file)

            case _:
                raise ValueError('uh oh')


if __name__ == '__main__':
    with open('day07/input', 'r') as f:
        root = parse_history(f)
        if not root:
            print("no directories found", sys.stderr)
            sys.exit(1)
        matching_dirs = []
        for next_dir in root.traverse():
            if not isinstance(next_dir, Directory):
                continue
            if next_dir.size() < _MAX_SIZE_PT1:
                matching_dirs.append(next_dir)
        pt1_ans = sum(d.size() for d in matching_dirs)
        free_space = _FILESYSTEM_CAPACITY - root.size()
        space_to_free = _NEEDED_SPACE - free_space
        pt2_ans = min(d.size() for d in root.traverse() if
                      isinstance(d, Directory) and
                      d.size() >= space_to_free)

        print(f"part 1: {pt1_ans}")
        print(f"part 2: {pt2_ans}")
