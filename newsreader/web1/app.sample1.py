import json
from flask import Flask, render_template

app = Flask(__name__)

# Sample data (replace with your actual data)
sample_items = [
    {'property1': 'value1', 'property2': 'value2', 'property3': 'value3'},
    {'property1': 'value4', 'property2': 'value5', 'property3': 'value6'},
    {'property1': 'value7', 'property2': 'value8', 'property3': 'value9'},
]

@app.route('/sample')
def index_sample():
    return render_template('index.sample.html', items=sample_items)

@app.route('/')
def index():
    return render_from_file( 'data/2024-12-15.headlines.json', 'index.html')

    # for testing:
    #     return render_from_file( 'data/sample1.json', 'index.html')

def filterOutPartialItems( articles: [] ) -> []:
    filtered_items = [item for item in articles if item.get('title') != "[Removed]"] 
    return filtered_items

def render_from_file( jsonDataFile: str, templateHTML: str):
    try:
        print( f"Loading data from {jsonDataFile}")
        with open( jsonDataFile, 'r') as f:
            loadedFile = json.load(f)
            articles = loadedFile["result"]["articles"]
            articles = filterOutPartialItems( articles)
            print( f"\n---------- \n {len(articles)} articles are found")
        return render_template( templateHTML, items=articles)
    except FileNotFoundError:
        return f"Error: JSON {jsonDataFile} file not found."
    except json.JSONDecodeError:
        return f"Error: Invalid JSON format {jsonDataFile} in file."

if __name__ == '__main__':
    app.run(debug=True)    