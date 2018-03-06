#!/usr/bin/env python3

import sys, os
from dotenv import find_dotenv, load_dotenv
from lib.inverted_index import InvertedIndex
from lib.encrypted_index import EncryptedIndex

load_dotenv(find_dotenv())

def main(index):
    print("Query: ", end="", flush=True)
    for line in sys.stdin: 

        if line.rstrip() == "quit()": # exit 
            break

        # for document in index.query(line[:-1]).most_common(10):
        for document in index.my_query(line[:-1], 10):
            print(document[0])
            print(document[1])
            print(index.document(document[0]))
        print("Query: ", end="", flush=True)






if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("USAGE: ./main.py path_to_trec_dataset")
        exit(0)

    trec_file_path = sys.argv[1]
    secret_key = os.environ.get("SECRET_KEY").encode('utf-8')

    index = EncryptedIndex(secret_key)
    #index = InvertedIndex()

    index.index_TREC(trec_file_path)
    #index.save_index()
    main(index)

    sys.exit(0)

