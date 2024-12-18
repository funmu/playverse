#
#  default.py 
#
#  Primary file defining the implmentation for component
#

# all providers are derived from Provider; import it.
from verse.core import Provider
import requests
from .utility import DateTimeManager

# the "Default" class is considered the primary entry point for provider
# one can define supplementary classes if needed
class Default(Provider):
    api_key: str = ""
    PYTHON_NEWS:str = ""
    US_HEADLINE_NEWS:str = ""
    dateTimeManager:DateTimeManager = DateTimeManager()

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.US_HEADLINE_NEWS = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=' + self.api_key
        self.PYTHON_NEWS = 'https://newsapi.org/v2/everything?q=python&sortBy=popularity&apiKey=' +self.api_key
        self.INDIA_NEWS = 'https://newsapi.org/v2/everything?q=india&sortBy=popularity&apiKey=' +self.api_key
        self.LATEST_NEWS = 'https://newsapi.org/v2/everything?sortBy=popularity&apiKey=' +self.api_key + "&q="

    # our implementation for the component contract
    def hello(self) -> str:
        dtNow = self.dateTimeManager.get_datetime_string()
        return f"Hello world! Time now is: {dtNow}"

    # get all top headlines
    def headlines( self, country="us") -> dict:
        usheadlines = requests.get( self.US_HEADLINE_NEWS)
        res = usheadlines.json()
        return usheadlines.json()

    # get all top headlines for python
    def python_news( self) -> dict:
        pynews = requests.get( self.PYTHON_NEWS)
        return pynews.json()

    # get all top headlines for India
    def india_headlines( self) -> str:
        indiaHeadlines = requests.get( self.INDIA_NEWS)
        res = indiaHeadlines.json()
        return indiaHeadlines.json()

    # get the latest news for given area of scope
    def latest( self, scope: str) -> str:
        print( f"latest called for scope = {scope}")
        latestNews = requests.get( self.LATEST_NEWS + scope)
        res = latestNews.json()
        return latestNews.json()

