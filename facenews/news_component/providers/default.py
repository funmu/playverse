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

# the "Default" class is considered the primary entry point for provider
# one can define supplementary classes if needed
class Default(Provider):
    api_key: str = ""
    US_HEADLINE_NEWS:str = ""
    dateTimeManager:DateTimeManager = DateTimeManager()

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.US_HEADLINE_NEWS = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=' + self.api_key
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

    # get the latest news for given area of scope
    def latest( self, scope: str) -> str:               # list[NewsItem]:
        print( f"latest called for scope = {scope}")
        latestNews = requests.get( self.LATEST_NEWS + scope)
        res = latestNews.json()
        return latestNews.json()

