import argparse
import datetime
import sys

ARGS = None

def t(m, s):
    return datetime.timedelta(minutes=m, seconds=s)


def make_times(offset, times, ending):
    return [time - offset for time in times] + [ending]


def make_splits(times):
    splits = []
    prev = t(0, 0)
    for curr in times:
        splits.append(curr - prev)
        prev = curr
    return splits


def make_deltas(news, olds):
    deltas = []
    for new, old in zip(news, olds):
        deltas.append(new - old)
    return deltas


def max_print_width(lst):
    max_width = 0
    for item in lst:
        width = len(str(item))
        if width > max_width:
            max_width = width
    return max_width


def time_string(time):
    return (   f"{int(time.total_seconds()) // 60:2d}"
            + f":{int(time.total_seconds()) % 60:02d}")


def split_string(time):
    return (   f"{int(time.total_seconds()) // 60:1d}"
            + f":{int(time.total_seconds()) % 60:02d}")


def delta_string(delta, width=0):
    return "{dt: >+{w}}".format(dt=int(delta.total_seconds()), w=width)


def print_splits(times, descriptions, spaces=0):
    splits = make_splits(times)
    for time, split, description in zip(times, splits, descriptions):
        print(f"`{" " * spaces}{time_string(time)} ({split_string(split)})` {description}")


def print_comparison(new_times, old_times, descriptions, time_width=0, split_width=0):
    new_splits = make_splits(new_times)
    old_splits = make_splits(old_times)

    delta_times = make_deltas(new_times, old_times)
    delta_splits = make_deltas(new_splits, old_splits)

    time_width = max(time_width, max_print_width(map(delta_string, delta_times)))
    split_width = max(split_width, max_print_width(map(delta_string, delta_splits)))

    for time, split, delta_time, delta_split, description in zip(new_times, new_splits, delta_times, delta_splits, descriptions):
        print(f"`{delta_string(delta_time, time_width)} {time_string(time)} ({delta_string(delta_split, split_width)} {split_string(split)})` {description}")


def read_from_timestamps():
    """
    Reads youtube formatted timestamps and turns them into splits!
    -   Reads from stdin, just paste them into the terminal (and add the actual
        run's time at the end on its own final line).
    -   Uses the first timestamp as an offset (assuming it is the timestamp for
        the run starting).
    -   Ignores the last timestamp's time and uses the actual finish time (but
        will use the final timestamp's description for this split.
    """
    line = sys.stdin.readline()
    m = int(line[0:2])
    s = int(line[3:5])
    offset = t(m, s)

    descriptions = []
    times = []
    for line in sys.stdin.readlines():
        m = int(line[0:2])
        s = int(line[3:5])
        times.append(t(m, s))
        descriptions.append(line[6:-1])

    ending = times[-1]
    times = times[0:-2]

    print_splits(make_times(offset, times, ending), descriptions, spaces=ARGS.spaces)


def compare_splits():
    """
    Reads from two sets of splits and compares them, generating splits which
    include the comparison.
    -   Reads from stdin, just paste them into the terminal, separated by a
        blank line.
    """
    old_times = []
    while True:
        line = sys.stdin.readline()
        if len(line) <= 1:
            break
        ci = line.index(":")
        m = int(line[0:ci])
        s = int(line[ci+1:ci+3])
        old_times.append(t(m, s))
    new_times = []
    descriptions = []
    while True:
        line = sys.stdin.readline()
        if len(line) <= 1:
            break
        ci = line.index(":")
        m = int(line[0:ci])
        s = int(line[ci+1:ci+3])
        description = line[ci+11:-1]
        new_times.append(t(m, s))
        descriptions.append(description)
    print_comparison(new_times, old_times, descriptions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--spaces", type=int, default=0, help="number of padding spaces")
    parser.add_argument("-c", "--compare", action="store_true", help="compare splits")
    global ARGS
    ARGS = parser.parse_args()

    if ARGS.compare:
        compare_splits()
    else:
        read_from_timestamps()


def test():
    news = [t(1, 11), t(1, 55), t(2, 32)]
    olds = [t(1, 22), t(1, 59), t(2, 31)]
    descriptions = ["one", "two", "three"]
    print_comparison(news, olds, descriptions)

if __name__ == "__main__":
    main()
