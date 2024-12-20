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

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  helpers
from stverse import JsonHelpers, StRunner
import streamlit as st

styles = """
<style>
.results-container {
  max-height: 500px;
  overflow-y: auto;
}
</style>
"""

def main():
    # Set the page layout to 'wide' at the very beginning
    st.set_page_config(layout="wide")
    st.markdown(styles, unsafe_allow_html=True)

    st.title("News using news API")

    jsonHelpers = JsonHelpers()
    operations_data = jsonHelpers.load_rest_operations( SERVICE_NAME, SERVICE_DEFINITIONS)

    if operations_data:
        stRunner = StRunner( SERVICE_NAME)
        stRunner.showMainScreen( operations_data)

if __name__ == "__main__":
    main()