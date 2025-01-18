#
#  component.py 
#
#  MUST Have file for Verse
#  This file gives the defintion with decorated methods
#

# all components derive from Component, so import it
# we will use the "operation" attribute, so import it as well
from verse.core import Component, operation


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
