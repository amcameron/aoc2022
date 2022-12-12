"""summarize elf calorie inventories

Partitions file by empty lines and takes the sum of each partitio."""

def parse_elfs(lines):
    while lines:
        sum = 0
        while lines and (line := lines.pop(0)):
            sum += int(line)
        yield sum

if __name__ == '__main__':
    lines = ['10', '20', '', '5', '', '100', '500', '1000']
    print(list(parse_elfs(lines)))
    # expect: [30, 5, 1600]
