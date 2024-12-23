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

    def execute_operation( self, opsPackage, operations_data):
        """
            Executes the specified REST operation.
        """

        operation = opsPackage["operation"]
        queryParams = opsPackage["queryParams"]
        bodyParams = opsPackage["bodyParams"]

        op_data = operations_data.get( operation)
        if not op_data:
            st.error(f"Invalid operation: { operation}")
            return

        url = op_data['url']
        method = op_data['method']
        headers = op_data.get('headers', {
            'Content-Type': 'application/json' 
        })

        response = requests.request(method, url, 
            headers=headers, 
            params=queryParams, 
            json=bodyParams)
        response.raise_for_status()
        return response.json()

    def prepare_operation( self, operations_data):
        """
            Prepare the operation and return operation package

            Returns:
                operation package used for execution

        """

        opArgs = {}
        queryParams = {}
        operation = "hello"

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

        return { "operation": operation, 
                 "queryParams": queryParams, 
                 "bodyParams": bodyParams, 
                 "displayType": displayType }