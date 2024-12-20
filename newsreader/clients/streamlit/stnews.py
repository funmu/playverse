# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  stnews.py
#
#  create streamlit based UI for news api
#
#  Created: Murali Krishnan, Dec 19, 2024
# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

SERVICE_NAME="news_api"
SERVICE_DEFINITIONS="newsapi.definitions.json"

import requests
from stverse import JsonHelpers, StRunner
import streamlit as st

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  helper for News Results


# sampleNews = {
#     'result': 
#         {'status': 'ok', 'totalResults': 2, 
#         'articles': [{'source': {'id': None, 'name': '[Removed]'}, 'author': None, 'title': '[Removed]', 'description': '[Removed]', 'url': 'https://removed.com', 'urlToImage': None, 'publishedAt': '2024-12-19T16:26:00Z', 'content': '[Removed]'}, 
#         {'source': {'id': None, 'name': 'Yahoo Entertainment'}, 'author': 'MICHELLE CHAPMAN', 'title': 'Frozen French fry maker Lamb Weston names new CEO, moves to loss in Q2 and cuts outlook - Yahoo Finance', 'description': 'Lamb Weston is naming a new CEO as the company moved to a loss in its second quarter and trimmed its fiscal 2025 forecast amid weakening demand for frozen...', 'url': 'https://finance.yahoo.com/news/frozen-french-fry-maker-lamb-142043456.html', 'urlToImage': 'https://s.yimg.com/ny/api/res/1.2/OvN6DIBDbUZkbMp8.MtJAQ--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyMDA7aD05MDA-/https://s.yimg.com/os/creatr-uploaded-images/2024-10/ab16fac0-8dbd-11ef-8eef-a08682173ddb', 'publishedAt': '2024-12-19T15:58:47Z', 'content': 'Lamb Weston is naming a new CEO as the company moved to a loss in its second quarter and trimmed its fiscal 2025 forecast amid weakening demand for frozen potato products in North America.\r\nShares of… [+3208 chars]'},
#         ]
#     }
# }


class StNewsResults:
    """
        Has methods to display news results
        It formats the items based on values received.
        Handles null values as well
    """

    serviceName: str = "ST CLIENT"

    def __init__(self, serviceName: str):
        self.serviceName = serviceName

    def get_news_item( self, item):
        """ 
        Inspects the input and ensures that all None / invalid items are removed

        """
        # ToDo: is there a cheaper way to reformat?

        news_item = {}
        input_fields = [ "urlToImage", "url", "title", "description"]
        for field in input_fields:
            if field in item:
                news_item[field] = item[field]

        news_item["footer"] = ""
        if "author" in item and item["author"] != None:
            news_item["footer"] = item["author"]
        
        if "source" in item and "name" in item["source"] and item["source"]["name"] != None:
            news_item["footer"] = news_item["footer"] + " of " + item["source"]["name"]
            
        if "publishedAt" in item and item["publishedAt"] != None:
            news_item["footer"] = news_item["footer"] + ", " + item["publishedAt"]

        return news_item
    
    def show_pretty_results( self, filteredItems):

        for item in filteredItems:
            news_item = self.get_news_item( item)

            st.markdown('<div class="item-container">', unsafe_allow_html=True)
            if ( news_item["urlToImage"] != None):
                st.image(news_item["urlToImage"], width=140)  # Display the image

            st.markdown('<div>', unsafe_allow_html=True)  # Create a div for text content
            st.markdown(f'<p class="title"><a href="{news_item["url"]}" target="_blank">{news_item["title"]}</a></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="description">{news_item["description"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="footer">{news_item["footer"]}</p>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)  # Close the text content div
            st.markdown('</div>', unsafe_allow_html=True)  # Close the item container div

            st.write("--------")  # Add a separator between items

    def show_results( self, displayType, responseJson):

        st.header( self.serviceName + " Results")
        print( responseJson)
        if "result" in responseJson and "articles" in responseJson["result"]:
                
            articles = responseJson["result"]["articles"]
            filteredItems = [item for item in articles if item.get('title') != "[Removed]"]

            with st.container():
                # st.json(responseJson(), height=500)  # Adjust height as needed
                st.markdown('<div class="results-container">', unsafe_allow_html=True)
                if (displayType == 'json'):
                    st.json( filteredItems)
                else:
                    self.show_pretty_results( filteredItems)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.json( responseJson)

def main():
    # Set the page layout to 'wide' at the very beginning
    st.set_page_config(layout="wide")
    with open('news_styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)    

    st.title("News using news API")

    jsonHelpers = JsonHelpers()
    operations_data = jsonHelpers.load_rest_operations( SERVICE_NAME, SERVICE_DEFINITIONS)

    if operations_data:
        stRunner = StRunner( SERVICE_NAME)
        left_column, right_column = st.columns([0.2, 0.8])
        resultsJson = { "error": "Still processing"}
        with left_column:            
            opsPackage = stRunner.prepare_operation( operations_data)
            if st.button("Execute"):
                with right_column:
                    try:
                        resultsJson = stRunner.execute_operation( opsPackage, operations_data)
                        stResults = StNewsResults( SERVICE_NAME)
                        stResults.show_results( opsPackage["displayType"], resultsJson)
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error executing operation: {e}")

if __name__ == "__main__":
    main()