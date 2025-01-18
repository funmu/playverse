#
#  component.py 
#
#  MUST Have file for Verse
#  This file gives the defintion with decorated methods
#

# all components derive from Component, so import it
# we will use the "operation" attribute, so import it as well
from verse.core import Component, operation, DataModel

# our news items are hosted here
class NewsItem( DataModel):

    """
    here is a sample news item that will get mapped
    {
        "source": {
          "id": null,
          "name": "Yahoo Entertainment"
        },
        "author": "Mat Smith",
        "title": "The Morning After: What to expect at CES 2025",
        "description": "The holidays haven’t even kicked off, but we’re already looking to next year when, almost immediately, some of the Engadget team will head to Las Vegas for tech’s biggest annual conference. The pitches from companies, both legit and unhinged, are already fill…",
        "url": "https://consent.yahoo.com/v2/collectConsent?sessionId=1_cc-session_b8d5b11a-45bf-40d5-98c0-33fe6962feb7",
        "urlToImage": null,
        "publishedAt": "2024-12-17T12:15:28Z",
        "content": "If you click 'Accept all', we and our partners, including 237 who are part of the IAB Transparency &amp; Consent Framework, will also store and/or access information on a device (in other words, use … [+678 chars]"
      },
    """
    title: str
    description: str
    author: str

    url: str
    urlToImage: str
    publishedAt: str
    # content: str
    # sourceName: str


# Our first component for this project
class CustomComponent(Component):

    @operation()
    def hello(self) -> str: pass 

    # get all top headlines
    @operation()
    def headlines( self, country="us") -> str: pass

    # get the latest news for given area of scope
    @operation()
    def latest( self, scope: str="technology") -> str: pass

    # get the headlines by country
    @operation()
    def headlinesByCountry( self, country="us"): pass

    # get the sources for getting news from
    @operation()    
    def sources( self): pass
    
    # get the headlines by source; default is from reuters
    @operation()    
    def headlinesBySource( self, source="reuters"): pass
