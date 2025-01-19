import requests
import json
from flask import Flask, render_template, request

import os
from dotenv import load_dotenv
load_dotenv()

# MY SERVER ... get this from environment file
MY_NEWS_SERVER='http://localhost:8080/'  # use for testing purposes
server_location = os.getenv('MY_NEWS_SERVER') 

NewsNotFoundHTML = "newsNotFound.html"
HeadlineNewsTemplateHTML = 'index.headlines.html'
NewsHomeTemplateHTML = 'index.html'

NEWS_SOURCES = {
    "reuters"       : "Reuters",
    "associated-press": "Asspciated Press",
    "ap"            : "Associated Press",
    "bloomberg"     : "Bloomberg News",
    "fortune"       : "Fortune",
    "newsweek"      : "Newsweek",
    "new-york-magazine" : "New York Magazine",
    "new-scientist" : "New Scientist",

    "abc-news"      : "ABC News",
    "bbc-news"      : "BBC News",
    "cbs-news"      : "CBS News",
    "nbc-news"      : "National Broadcasting Corporation (NBC)",
    "cnn"           : "CNN (Cable News Network)",
    "cnbc"          : "CNBC",
    "msnbc"         : "Microsoft + National Broadcasting Corporation (NBC)",

    "buzzfeed"      : "Buzzfeed",
    "engadget"      : "Engadget",
    "ars-technica"  : "Ars Technica",
    "google-news"   : "Google News",
    "hacker-news"   : "Hacker News",
    "techcrunch"    : "TechCrunch",
    "gizmodo"       : "Gizmodo",
}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template( NewsHomeTemplateHTML, sources=NEWS_SOURCES)

@app.route('/hello')
def index_hello():
    print( "\n---------- \nGOT a test request")
    return "Hello World!"

@app.route('/headlines')
def index_headlines():
    return show_headlines()

@app.route('/headlines/source')
def index_headlines_by_source():
    """
    This route handles requests to /headlines with optional query parameters.

    Example usage:
    /headlines/source?source=<SOURCENAME>&scope=<SCOPE>
    """
    source = request.args.get('source', 'reuters')
    scope = request.args.get('scope', '')

    headline_args = { "source": source}
    if (scope != ''):
        headline_args['scope']=scope

    return show_headlines( 'headlinesBySource', headline_args)

def show_headlines( operation = "headlines", headline_args = {}):
    print( "\n---------- \nGetting the news articles")
    newsItems = getNewsItems( operation, op_args=headline_args)
    if ( newsItems != None):
        articles = newsItems["result"]["articles"]
        articles = filterOutPartialItems( articles)
        print( f"\t{len(articles)} articles are found")
        if ( len(articles) > 0):
            return render_template( HeadlineNewsTemplateHTML, items=articles)
        else:
            return render_template( NewsNotFoundHTML)
    else:
        print( "GOT ERROR")
        return render_template( NewsNotFoundHTML)

def getNewsItems( operation, op_args = {}):
    try:
        # Get the news data using a POST request
        # Get the server location from the .env file
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
                "name": operation,
                "args": op_args
            }
        }

        print( f"Sending request to {server_location}\n\theaders: {headers}\n\tdata: {data}");
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes

        items = response.json()
        return items

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news data: {e}")
        return None

def filterOutPartialItems( articles: [] ) -> []:
    filtered_items = [item for item in articles if item.get('title') != "[Removed]"] 
    return filtered_items

## ---- ---- ---- ---- ---- ---- ---- ---- ----
# MAIN CODE is here

if __name__ == '__main__':
    app.run(debug=True)    

## ---- ---- ---- ---- ---- ---- ---- ---- ----
# Following are for testing purposes only 

@app.route('/sample')
def index_sample():
    return render_template('index.sample.html', items=sample_items)

@app.route('/file1')
def index_file1():
    source_for_news = 'data/2024-12-15.headlines.json'
    # source_for_news = 'data/sample1.json' # for testing purposes
    return render_from_file( source_for_news, HeadlineNewsTemplateHTML)

# Sample data (replace with your actual data)
sample_items = [
    {'property1': 'value1', 'property2': 'value2', 'property3': 'value3'},
    {'property1': 'value4', 'property2': 'value5', 'property3': 'value6'},
    {'property1': 'value7', 'property2': 'value8', 'property3': 'value9'},
]

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
