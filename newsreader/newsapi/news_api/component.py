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

    @operation()
    def headlines( self) -> str: pass

    @operation()
    def python_news( self) -> str: pass

    @operation()
    def india_headlines( self) -> str: pass

    @operation()
    def latest( self, scope: str) -> str: pass
