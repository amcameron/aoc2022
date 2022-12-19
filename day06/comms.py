"""Help the elves decode a signal."""

from collections import deque


PACKET_MARKER_SIZE = 4
MESSAGE_MARKER_SIZE = 14


def count_offset(stream, marker_size):
    span = deque(maxlen=marker_size)
    for i, c in enumerate(stream):
        span.append(c)
        if len(set(span)) == marker_size:
            # this is not the offset, as we are at the end of the marker
            return i + 1
    return -1


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('filename')
    args = p.parse_args()

    with open(args.filename, 'r') as f:
        stream = f.read()
        print(count_offset(stream, PACKET_MARKER_SIZE))
        print(count_offset(stream, MESSAGE_MARKER_SIZE))
