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
            self.token_counts = pickle.load(token_counts_file)
            self.documents = pickle.load(documents_file)
            inverted_index_file.close()
            document_count_file.close()
            token_counts_file.close()
            documents_file.close()
        else:
            self.inverted_index = dict()
            self.document_count = 0
            self.token_counts = collections.Counter()
            self.documents = dict()

    def document(self, document_id):
        try:
            return str(self.aes.decrypt(self.documents[document_id]), 'utf-8')
        except KeyError as e:
            return None

    def index_token(self, document_id, token):
        self.token_counts[token] += 1
        if token not in self.inverted_index:
            self.inverted_index[token] = collections.Counter()
        self.inverted_index[token][document_id] += 1

    def index_tokens(self, document_id, tokens):
        for token in tokens:
            encrypted_token = self.aes.encrypt(self.pad(token))
            # print(encrypted_token)
            self.index_token(document_id, encrypted_token)
        self.document_count += 1

    def add_document(self, document_id, document_content):
        self.documents[document_id] = document_content

    def index(self, document_id, document_content, document_tokens):
        encrypted_doc_id = self.aes.encrypt(self.pad(document_id))
        encrypted_doc_content = self.aes.encrypt(self.pad(document_content))
        self.index_tokens(encrypted_doc_id, document_tokens)
        self.add_document(encrypted_doc_id, encrypted_doc_content)

    def query_token(self, token):
        # print(self.inverted_index[token])
        return self.inverted_index.get(token, collections.Counter())

    def query(self, q):
        encrypted_query = self.aes.encrypt(self.pad(q))
        # print(encrypted_query)
        return self.query_token(encrypted_query)

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
        pickle.dump(self.token_counts, token_counts_file)
        pickle.dump(self.documents, documents_file)

        inverted_index_file.close()
        document_count_file.close()
        token_counts_file.close()
        documents_file.close()

    def pad(self, content):
        return content.ljust(16)[:16]



