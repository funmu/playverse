# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  stverse.py
#
#  helpers for creating and using Streamlit with Verse operations
#
#  Created: Murali Krishnan, Dec 19, 2024
# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  JSON helpers
import json
import streamlit as st

class JsonHelpers:

    def load_rest_operations( self, serviceName: str, input_file: str):
        """Loads REST operations from a JSON file."""
        try:
            with open(input_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            st.error(f"Error loading {serviceName} REST operations: {e}")
            exit(1)

    def pretty_print_json( self, json_data):
        """
        Pretty prints JSON data with indentation and sorting.

        Args:
            json_data: The JSON data (can be a string or a Python object).
        """

        if isinstance(json_data, str):
            try:
                json_data = json.loads(json_data)
            except json.JSONDecodeError as e:
                st.error(f"Error: Invalid JSON string: {e}")
            return

        st.json(json_data)
        # print(json.dumps(json_data, indent=4, sort_keys=True))

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  Set up commad line parsers

import requests

class StRunner:

    serviceName: str = "ST CLIENT"

    def __init__(self, serviceName: str):
        self.serviceName = serviceName

    def show_pretty_results( self, filteredItems):

        for item in filteredItems:
            footer = item["author"] + " of " \
                + item["source"]["name"] \
                + ", " + item["publishedAt"]

            st.markdown('<div class="item-container">', unsafe_allow_html=True)
            if ( item["urlToImage"] != None):
                st.image(item["urlToImage"], width=140)  # Display the image

            st.markdown('<div>', unsafe_allow_html=True)  # Create a div for text content
            st.markdown(f'<p class="title"><a href="{item["url"]}" target="_blank">{item["title"]}</a></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="description">{item["description"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="footer">{footer}</p>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)  # Close the text content div
            st.markdown('</div>', unsafe_allow_html=True)  # Close the item container div

            st.write("--------")  # Add a separator between items

    def show_results( self, displayType, responseJson):

        st.header( self.serviceName + " Results")
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

    def execute_operation( self, operation, params, bodyParams, operations_data):
        """
            Executes the specified REST operation.
        """
        op_data = operations_data.get(operation)
        if not op_data:
            st.error(f"Invalid operation: {operation}")
            return

        url = op_data['url']
        method = op_data['method']
        headers = op_data.get('headers', {
            'Content-Type': 'application/json' 
        })

        response = requests.request(method, url, headers=headers, params=params, json=bodyParams)
        response.raise_for_status()
        return response.json()

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    #  Do Operations

    def showMainScreen( self, operations_data):

        left_column, right_column = st.columns([0.2, 0.8])
        opArgs = {}
        queryParams = {}
        operation = "hello"

        with left_column:
            st.header( self.serviceName + " Operations")
            if operations_data:
                operation = st.selectbox("Select operation", list(operations_data.keys()))
                op_data = operations_data[operation]

            for param_name, param_data in op_data.get('queryParams', {}).items():
                queryParams[param_name] = st.text_input(param_data.get('help', param_name), value=param_data.get('default', ''))

            for param_name, param_data in op_data.get('bodyParams', {}).items():
                opArgs[param_name] = st.text_input(param_data.get('help', param_name), value=param_data.get('default', ''))

        # name: op_data.get('operationName', operation),  # Use operation name from definition or default to operation key

            bodyParams = {
                "operation": {
                    "name": operation,
                    "args": opArgs
                }
            }

        # for importing in file data
        # input_data = {}
        # if 'inputFile' in op_data:
        #     input_file_content = st.text_area("Input data (JSON)")
        #     if input_file_content:
        #         try:
        #             input_data = json.loads(input_file_content)
        #         except json.JSONDecodeError:
        #             st.error("Invalid JSON format in input data")

            displayType = st.radio("Select Display", ['json', 'pretty'])

            if st.button("Execute"):
                try:
                    resultsJson = self.execute_operation(operation, queryParams, bodyParams, operations_data)
                    with right_column:
                        self.show_results( displayType, resultsJson)
                except requests.exceptions.RequestException as e:
                    st.error(f"Error executing operation: {e}")