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

def execute_operation(operation, params, bodyParams, operations_data):
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

    print( f"sending request to {url} for operation: {operation}")
    print( f"with headers {headers}")
    print( f"with body {bodyParams}")

    try:
        response = requests.request(method, url, headers=headers, params=params, json=bodyParams)
        response.raise_for_status()
        st.json(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error executing operation: {e}")

def main():
    st.title("News using news API")

    jsonHelpers = JsonHelpers()
    operations_data = jsonHelpers.load_rest_operations( SERVICE_NAME, SERVICE_DEFINITIONS)
    if operations_data:
        operation = st.selectbox("Select operation", list(operations_data.keys()))
        op_data = operations_data[operation]

        queryParams = {}
        for param_name, param_data in op_data.get('queryParams', {}).items():
            queryParams[param_name] = st.text_input(param_data.get('help', param_name), value=param_data.get('default', ''))

        opArgs = {}
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

        if st.button("Execute"):
            execute_operation(operation, queryParams, bodyParams, operations_data)

if __name__ == "__main__":
    main()