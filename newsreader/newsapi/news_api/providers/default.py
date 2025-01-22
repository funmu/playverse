#
#  default.py 
#
#  Primary file defining the implmentation for component
#

# all providers are derived from Provider; import it.
from verse.core import Provider
import requests
from .utility import DateTimeManager

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

BASE_NEWSAPI_URL:str = "https://newsapi.org/v2"

# the "Default" class is considered the primary entry point for provider
# one can define supplementary classes if needed
class Default(Provider):
    fVerbose = False
    dateTimeManager:DateTimeManager = DateTimeManager()
    api_key: str = ""
    # PYTHON_NEWS:str = ""
    # HEADLINE_NEWS:str = ""

    def __init__(self, api_key: str):
        self.fVerbose = True
        self.api_key = api_key      # API KEY will be sent in via the X-Api-Key header
        self.NEWS_SOURCES   = BASE_NEWSAPI_URL + '/top-headlines/sources'
        self.HEADLINE_NEWS  = BASE_NEWSAPI_URL + '/top-headlines'
        self.LATEST_NEWS    = BASE_NEWSAPI_URL + '/everything'
        self.NEWS_BY_SOURCE = BASE_NEWSAPI_URL + '/top-headlines'
        self.ALL_SOURCES = NEWS_SOURCES

    # our implementation for the component contract
    def hello(self) -> str:
        dtNow = self.dateTimeManager.get_datetime_string()
        return f"Hello world! Time now is: {dtNow}"

    def _process_http_request(self, url, method="GET", headers=None, params=None, data=None):
        """
        Creates an HTTP request and sends it immediately.

        Args:
            url: The URL for the request.
            method: The HTTP method (GET, POST, PUT, DELETE, etc.). Defaults to GET.
            headers: A dictionary of headers to include in the request.
            data: The request body data (for POST, PUT, etc.).
            params: Query parameters for the request.

        Returns:
            requests.Response: The response object from the server.
        """

        if headers is None:
            headers = {}
        headers['X-Api-Key'] = self.api_key

        if ( self.fVerbose ):
            print( f"sending request to {url} with params {params}")

        # Send the request directly
        response = requests.request(method, url, headers=headers, params=params, data=data)

        print(response)
        return response

    def _cleanup_news_results( self, newsRequest: str, rawNewsInputs: str):
        inputNewsJson = rawNewsInputs.json()
        if "articles" in inputNewsJson:
            articles = inputNewsJson["articles"]
            filteredItems = [item for item in articles if item.get('title') != "[Removed]"]
            print( f"[{newsRequest}]: filtered {len(articles)} and got {len(filteredItems)} news items")
            inputNewsJson["articles"] = filteredItems
            return inputNewsJson
        else:
            print( f"[{newsRequest}]: Error: No News articles are found")
            print(inputNewsJson)
            return { "Error": "No news articles are found"}        
    
    def sources( self):
        """
        Get a list of all the news sources

        Returns:
            list of news sources (a JSON array)
        """
        urlQuery = self.NEWS_SOURCES
        newsSources = self._process_http_request( urlQuery)
        return newsSources.json()

    def headlines( self, country="us") -> dict:
        """
        Get all the headlines for specific countries

        Returns:
            list of headline NewsItems (a JSON array) along with results count
        """
        newsRequest = f"headlines by country = {country}"
        headlines = self._process_http_request( self.HEADLINE_NEWS, params={ "country" : country})
        return self._cleanup_news_results( newsRequest, headlines)
    
    def latest( self, source = "reuters", scope: str = "technology") -> str:
        """
        Get the latest news for given area of scope

        Returns:
            list of all NewsItems (a JSON array) along with results count
        """
        newsRequest = f"latest by scope = {scope}"
        latestNews = self._process_http_request( 
            self.LATEST_NEWS, 
            params={ "q" : scope, "sortBy": "popularity"})
        return self._cleanup_news_results( newsRequest, latestNews)

    # get the headlines by country
    def headlinesByCountry( self, country = "us") -> dict:
        return self.headlines( country)

    # get the headlines by source; default is from reuters
    def headlinesBySource( self, source = "reuters", scope = "") -> dict:
        newsRequest = f"headlines by sources = {source}"
        params = { "sources" : source}
        if (scope != ""):
            params["q"] = scope
        headlines = self._process_http_request( self.LATEST_NEWS, params=params)
        return self._cleanup_news_results( newsRequest, headlines)
