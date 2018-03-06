import sys, os
import collections
import pickle

from Crypto.Cipher import AES
from Crypto.Cipher import ARC4
from Crypto.Hash import SHA256

class EncryptedIndex(object):
    def __init__(self, secret_key, saved_index_dir=None):
        hash = SHA256.new()
        hash.update(secret_key)
        self.aes = AES.new(hash.digest())
        if saved_index_dir:
            inverted_index_file = open("{}/inverted_index.txt".format(saved_index_dir), 'rb')
            document_count_file = open("{}/document_count.txt".format(saved_index_dir), 'rb')
            token_counts_file = open("{}/token_counts.txt".format(saved_index_dir), 'rb')
            documents_file = open("{}/documents.txt".format(saved_index_dir), 'rb')
            self.inverted_index = pickle.load(inverted_index_file)
            self.document_count = pickle.load(document_count_file)
            # self.token_counts = pickle.load(token_counts_file)
            self.documents = pickle.load(documents_file)
            inverted_index_file.close()
            document_count_file.close()
            token_counts_file.close()
            documents_file.close()
        else:
            self.inverted_index = dict() # { Key: string(Token) Value: dict{Key: string(document_id) Value: int(counter)} }
            self.document_count = 0 # holds document counter
            # self.token_counts = collections.Counter() # dictionary of token counter { Key: token Value: int(token_counter) }
            self.documents = dict() # holds all documents { Key: string(document_id) Value: string(document_content) }

    def document(self, document_id):
        try:
            return str(self.aes.decrypt(self.documents[document_id]), 'utf-8')
        except KeyError as e:
            return None

    def index_token(self, document_id, token):
        # self.token_counts[token] += 1

        count_buf = None

        if token not in self.inverted_index:
            self.inverted_index[token] = dict()

        if document_id not in self.inverted_index[token]:
            self.inverted_index[token][document_id] = dict()
            count_buf = 1
        else:
            count_buf = int(str(self.aes.decrypt(self.inverted_index[token][document_id]), 'utf-8').rstrip()) + 1

        self.inverted_index[token][document_id] = self.aes.encrypt(self.pad(str(count_buf)))


    def index_tokens(self, document_id, tokens):
        for token in tokens:
            encrypted_token = self.aes.encrypt(self.pad(token))
            self.index_token(document_id, encrypted_token)
        self.document_count += 1


    def add_document(self, document_id, document_content):
        self.documents[document_id] = document_content

    def index(self, document_id, document_content, document_tokens): 
        encrypted_doc_id = self.aes.encrypt(self.pad(document_id))
        encrypted_doc_content = self.aes.encrypt(self.pad(document_content))
        self.index_tokens(encrypted_doc_id, document_tokens)
        self.add_document(encrypted_doc_id, encrypted_doc_content)

    def query(self, q):
        encrypted_query = self.aes.encrypt(self.pad(q))
        return self.inverted_index.get(encrypted_query, collections.Counter())

    def my_query(self, q, num):
        '''
        Using simple sort call (nlogn)
        Can optimize to linear time using ranking algorithm to find top k numbers
        '''
        encrypted_query = self.aes.encrypt(self.pad(q))
        buf = []
        res = []
        tmp_num = num

        for doc_id in self.inverted_index[encrypted_query]:
            buf.append((int(str(self.aes.decrypt(self.inverted_index[encrypted_query][doc_id]), 'utf-8').rstrip()), doc_id))

        buf.sort()

        if num > len(buf): # safegaurd num larger than index numbers
            tmp_num = len(buf)

        for i in range(tmp_num):
            res.append((buf[i][1], buf[i][0]))

        return res

    def index_TREC(self, file_path):
        with open(file_path) as fp:
            for line in fp:
                split_document = line.split()
                document_id = split_document[0]
                self.index(document_id, line, split_document[1:])

    def save_index(self):
        if not os.path.exists('encrypted_index'):
            os.makedirs('encrypted_index')

        inverted_index_file = open('encrypted_index/inverted_index.txt', 'wb')
        document_count_file = open('encrypted_index/document_count.txt', 'wb')
        token_counts_file = open('encrypted_index/token_counts.txt', 'wb')
        documents_file = open('encrypted_index/documents.txt', 'wb')

        pickle.dump(self.inverted_index, inverted_index_file)
        pickle.dump(self.document_count, document_count_file)
        # pickle.dump(self.token_counts, token_counts_file)
        pickle.dump(self.documents, documents_file)

        inverted_index_file.close()
        document_count_file.close()
        token_counts_file.close()
        documents_file.close()

    def pad(self, content):
        '''
        0 padding to make cotent 16 in length for aes encryption
        '''
        pad_amount = 16 - len(content) % 16
        pad_content = ' ' * pad_amount
        return content + pad_content



