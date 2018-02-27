#!/usr/bin/env python3

import sys
from index.inverted_index import InvertedIndex

def main(index):
    print("Query: ", end="", flush=True)
    for line in sys.stdin:
        for doc_id in index.query(line[:-1]):
            print(doc_id)
        print("Query: ", end="", flush=True)

if len(sys.argv) != 2:
    print("USAGE: ./main.py path_to_trec_dataset")
    exit(0)

trec_file_path = sys.argv[1]

if __name__ == "__main__":
    index = InvertedIndex()
    index.indexTREC(trec_file_path)
    main(index)

