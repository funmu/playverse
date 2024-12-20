import requests
import json
from flask import Flask, render_template, request

import os
from dotenv import load_dotenv
load_dotenv()

# MY SERVER ... get this from environment file
MY_NEWS_SERVER='https://myServer/'  # use for testing purposes

NewsNotFoundHTML = "newsNotFound.html"
NewsTemplateHTML = 'index.html'

app = Flask(__name__)

@app.route('/')
def index():
    print( "\n---------- \nGetting the news articles")
    newsItems = getNewsItems()
    if ( newsItems != None):
        articles = newsItems["result"]["articles"]
        articles = filterOutPartialItems( articles)
        print( f"\t{len(articles)} articles are found")
        return render_template( NewsTemplateHTML, items=articles)
    else:
        print( "GOT ERROR")
        return render_template( NewsNotFoundHTML)

def getNewsItems():
    try:
        # Get the news data using a POST request
        # Get the server location from the .env file
        server_location = os.getenv('MY_NEWS_SERVER') 
        if not server_location:
            print( f"Error: SERVER_LOCATION not found in .env file.")
            return None

        url = server_location  # Construct the URL using the environment variable
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            "operation": {
                "name": "headlines",
                "args": {}
            }
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes

        items = response.json()
        return items

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news data: {e}")
        return None


# Sample data (replace with your actual data)
sample_items = [
    {'property1': 'value1', 'property2': 'value2', 'property3': 'value3'},
    {'property1': 'value4', 'property2': 'value5', 'property3': 'value6'},
    {'property1': 'value7', 'property2': 'value8', 'property3': 'value9'},
]

@app.route('/sample')
def index_sample():
    return render_template('index.sample.html', items=sample_items)

@app.route('/file1')
def index_file1():
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