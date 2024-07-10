from whoosh.index import open_dir
from whoosh.qparser import QueryParser

# Open the existing index
ix = open_dir("indexdir")

# Get the search query from the user
user_query = input("Enter your search query: ")

# Create a searcher and parser
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse(user_query)
    results = searcher.search(query)

    # Print the results
    for result in results:
        print(f"Title: {result['title']}, Path: {result['path']}")