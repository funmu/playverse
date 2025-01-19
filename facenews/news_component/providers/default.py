#
#  default.py 
#
#  Primary file defining the implmentation for component
#

# all providers are derived from Provider; import it.
from verse.core import Provider
import requests
from .utility import DateTimeManager
from ..component import NewsItem


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

# the "Default" class is considered the primary entry point for provider
# one can define supplementary classes if needed
class Default(Provider):
    dateTimeManager:DateTimeManager = DateTimeManager()
    api_key: str = ""
    # PYTHON_NEWS:str = ""
    # HEADLINE_NEWS:str = ""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.HEADLINE_NEWS = 'https://newsapi.org/v2/top-headlines?apiKey=' + self.api_key + '&country='
        self.LATEST_NEWS = 'https://newsapi.org/v2/everything?sortBy=popularity&apiKey=' +self.api_key + "&q="
        self.NEWS_BY_SOURCE = 'https://newsapi.org/v2/top-headlines?sortBy=popularity&apiKey=' +self.api_key + "&sources="
        self.ALL_SOURCES = NEWS_SOURCES
        # self.PYTHON_NEWS = self.LATEST_NEWS + 'python'
        # self.INDIA_NEWS = self.LATEST_NEWS + 'india'

    def _getNews(self, newsRequest, newsUrl):
        newsItems = requests.get( newsUrl)
        inputNewsJson = newsItems.json()
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

    # our implementation for the component contract
    def hello(self) -> str:
        dtNow = self.dateTimeManager.get_datetime_string()
        return f"Hello world! Time now is: {dtNow}"

    # get all top headlines
    def headlines( self, country="us") -> dict:
        print( f"get headlines news for country = {country}")
        return self._getNews( f"headlines by country = {country}", self.HEADLINE_NEWS + country)

    # get the latest news for given area of scope
    def latest( self, scope: str = "technology") -> str:
        print( f"get latest news for scope = {scope}")
        return self._getNews(  f"latest by scope = {scope}", self.LATEST_NEWS + scope)

    # get the headlines by country
    def headlinesByCountry( self, country="us") -> dict:
        return self.headlines( country)

    # get the sources for getting news from
    def sources( self):
        return self.ALL_SOURCES;

    # get the headlines by source; default is from reuters
    def headlinesBySource( self, source="reuters", scope="") -> dict:
        urlQuery = source
        if ( scope != ""):
            urlQuery = urlQuery + "&q=" + scope

        return self._getNews(  f"headlines by sources = {urlQuery}", self.NEWS_BY_SOURCE + urlQuery)

