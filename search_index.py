from whoosh.index import open_dir
from whoosh.qparser import QueryParser

ix = open_dir("indexdir")

user_query = input("Enter your search query: ")

with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse(user_query)
    results = searcher.search(query)

    for result in results:
        print(f"Title: {result['title']}, Path: {result['path']}")