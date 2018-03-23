#!/usr/bin/env python3

import sys, os
from dotenv import find_dotenv, load_dotenv
from lib.inverted_index import InvertedIndex
from lib.encrypted_index import EncryptedIndex
from timeit import default_timer as timer
import numpy as np

load_dotenv(find_dotenv())

if __name__ == "__main__":

    # if len(sys.argv) != 2:
    #     print("USAGE: ./main.py path_to_trec_dataset")
    #     exit(0)

    trec_file_path = '/Users/changreytang/dev/university/EncryptedInvertedIndex/data/sample-data.txt'
    secret_key = os.environ.get("SECRET_KEY").encode('utf-8')

    enc_index = EncryptedIndex(secret_key)
    # index = EncryptedIndex(secret_key, 'encrypted_index')
    index = InvertedIndex()
    # index = InvertedIndex('inverted_index')

    start = timer()
    index.index_TREC(trec_file_path)
    end = timer()
    print("Normal Indexing Time: " + str(1000*(end - start)) + " ms")

    start = timer()
    enc_index.index_TREC(trec_file_path)
    end = timer()
    print("Encrypted Indexing Time: " + str(1000*(end - start)) + " ms")
    # index.save_index()
    # main(index)

    sys.exit(0)

