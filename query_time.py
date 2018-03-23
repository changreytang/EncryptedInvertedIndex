#!/usr/bin/env python3

import sys, os
from dotenv import find_dotenv, load_dotenv
from lib.inverted_index import InvertedIndex
from lib.encrypted_index import EncryptedIndex
from timeit import default_timer as timer
import numpy as np

load_dotenv(find_dotenv())

def main(index, enc_index):
    print("Query Format: [Desired Keyword] [Number of Documents] [Document Flag (y/n)]")
    print("Keyword Required. Default Document=10. Default Flag=n")
    print("Query: ", end="", flush=True)

    for line in sys.stdin:

        res = []
        line = line.rstrip()
        line_split = line.split()

        num_docs = 10
        doc_flag = 'n'


        if line == "quit()": # exit
            break

        if len(line_split) == 1: # arg parser
            pass
        elif len(line_split) == 3:
            if line_split[1].isdigit() and (line_split[2]=='y' or line_split[2]=='n'):
                num_docs = int(line_split[1])
                doc_flag = line_split[2]
            else:
                print ("Invalid Command")
                print("Query: ", end="", flush=True)
                continue
        else:
            print ("Invalid Command")
            print("Query: ", end="", flush=True)
            continue

        start = timer()

        for document in index.query(line[:-1]).most_common(num_docs):
            doc_word_count = (len(index.document(document[0]).split()))
            word_freq_count = document[1]

            buf = ((1000*(1+np.log(word_freq_count))/doc_word_count), document[0])
            res.append(buf)

        res.sort()
        end = timer()

        print("Normal Query Time: " + str(1000*(end - start)) + " ms")

        res = []
        start = timer()

        for document in enc_index.my_query(line_split[0], num_docs):
            doc_word_count = (len(enc_index.document(document[0]).split()))
            word_freq_count = (enc_index.document(document[0]).count(line_split[0]))

            buf = ((1000*(1+np.log(word_freq_count))/doc_word_count), document[0])
            res.append(buf)

        res.sort()
        end = timer()

        print("Encrypted Query Time: " + str(1000*(end - start)) + " ms")

        print("Query: ", end="", flush=True)



if __name__ == "__main__":

    # if len(sys.argv) != 2:
    #     print("USAGE: ./main.py path_to_trec_dataset")
    #     exit(0)

    # trec_file_path = sys.argv[1]
    secret_key = os.environ.get("SECRET_KEY").encode('utf-8')

    # index = EncryptedIndex(secret_key)
    enc_index = EncryptedIndex(secret_key, 'encrypted_index')
    # index = InvertedIndex()
    index = InvertedIndex('inverted_index')

    # index.index_TREC(trec_file_path)
    # index.save_index()
    main(index, enc_index)

    sys.exit(0)

