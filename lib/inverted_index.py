import sys, os
import collections
import pickle

class InvertedIndex(object):
    def __init__(self, saved_index_dir=None):
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
            return self.documents[document_id]
        except KeyError as e:
            return None

    def index_token(self, document_id, token):
        self.token_counts[token] += 1
        if token not in self.inverted_index:
            self.inverted_index[token] = collections.Counter()
        self.inverted_index[token][document_id] += 1

    def index_tokens(self, document_id, tokens):
        for token in tokens:
            self.index_token(document_id, token)
        self.document_count += 1

    def add_document(self, document_id, document_content):
        self.documents[document_id] = document_content

    def index(self, document_id, document_content, document_tokens):
        self.index_tokens(document_id, document_tokens)
        self.add_document(document_id, document_content)

    def query_token(self, token):
        return self.inverted_index.get(token, collections.Counter())

    def query(self, q):
        return self.query_token(q)

    def index_TREC(self, file_path):
        with open(file_path) as fp:
            for line in fp:
                split_document = line.split()
                document_id = split_document[0]
                self.index(document_id, line, split_document[1:])

    def save_index(self):
        if not os.path.exists('inverted_index'):
            os.makedirs('inverted_index')

        inverted_index_file = open('inverted_index/inverted_index.txt', 'wb')
        document_count_file = open('inverted_index/document_count.txt', 'wb')
        token_counts_file = open('inverted_index/token_counts.txt', 'wb')
        documents_file = open('inverted_index/documents.txt', 'wb')

        pickle.dump(self.inverted_index, inverted_index_file)
        pickle.dump(self.document_count, document_count_file)
        pickle.dump(self.token_counts, token_counts_file)
        pickle.dump(self.documents, documents_file)

        inverted_index_file.close()
        document_count_file.close()
        token_counts_file.close()
        documents_file.close()


            # self.inverted_index = dict()
            # self.document_count = 0
            # self.token_counts = collections.Counter()
            # self.documents = dict()


