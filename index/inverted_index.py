import collections

class InvertedIndex(object):
    def __init__(self):
        self.inverted_index = dict()
        self.document_count = 0
        self.token_counts = collections.Counter()
        self.documents = dict()

    def document(self, document_id):
        try:
            return (self.documents[document_id], None)
        except KeyError as e:
            return (None, e)

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
        return set(self.inverted_index.get(token, collections.Counter()).keys())

    def query(self, q):
        return self.query_token(q)

    def indexTREC(self, file_path):
        with open(file_path) as fp:
            for line in fp:
                split_document = line.split()
                document_id = split_document[0]
                self.index(document_id, line, split_document[1:])
        # print(self.inverted_index)
        print(self.documents)


