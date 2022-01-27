import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--upper", action="store_true")
parser.add_argument("--lines", type=int)
parser.add_argument("source")
parser.add_argument("destination")
args = parser.parse_args()


with open(args.source, "r") as source:
    with open(args.destination, "w") as destination:
        temp = source.readlines()
        for i in range(args.lines):
            try:
                destination.write(temp[i] if not args.upper else temp[i].upper())
            except IndexError:
                pass
