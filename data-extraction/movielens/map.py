# userId,movieId,rating,timestamp

import sys

movieId_col = 1
rating_col = 2

def mapper():
    infile = sys.stdin
    next(infile)
    for line in infile:
        cols = line.strip().split(",")
        print(f"{cols[movieId_col]},{cols[rating_col]}")

if __name__ == "__main__":
    mapper()
