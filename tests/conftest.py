TEST_DB_NAME = "test_db"


class FakeCollection:
    def __init__(self, documents=None, aggregate_result=None):
        self.documents = list(documents or [])
        self.aggregate_result = list(aggregate_result or [])
        self.inserted_many = []

    def aggregate(self, pipeline):
        self.pipeline = pipeline
        return iter(self.aggregate_result)

    def find(self, query=None, projection=None):
        query = query or {}
        if query == {}:
            return iter(self.documents)

        ids = set(query.get("_id", {}).get("$in", []))
        return iter(document for document in self.documents if document.get("_id") in ids)

    def count_documents(self, query):
        return len(self.documents)

    def insert_many(self, documents):
        inserted = list(documents)
        self.inserted_many.append(inserted)
        self.documents.extend(inserted)


class FakeDatabase:
    def __init__(self, collections=None):
        self.collections = dict(collections or {})

    def __getitem__(self, name):
        if name not in self.collections:
            self.collections[name] = FakeCollection()
        return self.collections[name]
