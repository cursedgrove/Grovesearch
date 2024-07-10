import json
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
import os

schema = Schema(
    title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    url=ID(stored=True),
    content=TEXT(analyzer=StemmingAnalyzer())
)
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

ix = create_in("indexdir", schema)
writer = ix.writer()

json_file_path = 'websites.json'
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    for site in data:
        try:
            writer.add_document(title=site['title'], url=site['url'], content=site['content'])
        except Exception as e:
            print(f"Error processing document: {e}")
writer.commit()
print("Index created and documents added.")
