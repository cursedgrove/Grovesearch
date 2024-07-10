from flask import Flask, request, render_template
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser

app = Flask(__name__)

# Open the existing index
ix = open_dir("indexdir")

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    user_query = request.form['query']
    print(f"User query: {user_query}")  # Debug print
    with ix.searcher() as searcher:
        parser = MultifieldParser(["title", "content"], ix.schema)
        query = parser.parse(user_query + '*')  # Adding wildcard for partial matches
        results = searcher.search(query)
        print(f"Number of results: {len(results)}")  # Debug print
        for result in results:
            print(f"Title: {result['title']}, URL: {result['url']}")  # Debug print
        return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
