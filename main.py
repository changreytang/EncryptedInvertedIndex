#!/usr/bin/env python3

import sys, os
from dotenv import find_dotenv, load_dotenv
from lib.inverted_index import InvertedIndex

load_dotenv(find_dotenv())

def main(index):
    print("Query: ", end="", flush=True)
    for line in sys.stdin:
        for document in index.query(line[:-1]).most_common(10):
            print(document)
        print("Query: ", end="", flush=True)

# if len(sys.argv) != 2:
#     print("USAGE: ./main.py path_to_trec_dataset")
#     exit(0)

#trec_file_path = sys.argv[1]
secret_key = os.environ.get("SECRET_KEY")

if __name__ == "__main__":
    index = InvertedIndex('inverted_index')
    #index.index_TREC(trec_file_path)
    index.save_index()
    main(index)

