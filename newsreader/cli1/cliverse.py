# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  cliverse.py
#
#  helpers for creating and using CLI with Verse operations
#
#  Created: Murali Krishnan, Dec 19, 2024
# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  JSON helpers
import json

class JsonHelpers:

    def load_rest_operations( self, input_file):
        """Loads REST operations from a JSON file."""
        try:
            with open(input_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading {SERVICE_NAME} REST operations: {e}")
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
                print(f"Error: Invalid JSON string: {e}")
            return

        print(json.dumps(json_data, indent=4, sort_keys=True))

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  Set up commad line parsers
import sys
import argparse
import requests

class CliRunner:

    operations = None
    cliParser = None

    def _create_main_parser( self, serviceName: str):

        cliName = serviceName+"_cli"
        cliDescription = "CLI for using the " + serviceName

        parser = argparse.ArgumentParser(
            prog = cliName,
            description = cliDescription,
            epilog="Thanks for using " + cliName
            )
        parser.add_argument( "operation", help="operation to be conducted")

        # Use follwoing if we want to configure where the service definitions come from
        # parser.add_argument("--ops", help="Override the default operations definitions using this file")  
    
        # Add argument for URL to send the request to
        parser.add_argument("--url", help="Override the default URL for the operation")  

        return parser

    def create_cli( self, serviceName: str, operation_definitions_json_file: str):
        """
        Creates a CLI sub parsers based on REST operations.
        """

        self.cliParser = self._create_main_parser( serviceName)

        jsonHelpers = JsonHelpers()
        self.operations = jsonHelpers.load_rest_operations(operation_definitions_json_file)

        subparsers = self.cliParser.add_subparsers(dest='operation', required=True)

        for op_name, op_data in self.operations.items():
            
            subparser = subparsers.add_parser(op_name, help=op_data.get('help', ''))

            # Add arguments for query parameters
            for param_name, param_data in op_data.get('queryParams', {}).items():
                subparser.add_argument(f"--{param_name}", help=param_data.get('help', ''), required=param_data.get('required', False))

            for param_name, param_data in op_data.get('bodyParams', {}).items():
                subparser.add_argument(f"--{param_name}", help=param_data.get('help', ''), required=param_data.get('required', False))

            # Add argument for input file
            if 'inputFile' in op_data:
                subparser.add_argument("input_file", help=op_data['inputFile'].get('help', ''))

        return self.cliParser

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    #  Do Operations

    def execute_operation( self, inputArgs):
        """
        
        Executes the specified REST operation.

        Returns:
            JSON results; None if there was an error
        
        """

        cli_args = self.cliParser.parse_args( inputArgs)

        operation = cli_args.operation
        args = cli_args
        operations_data = self.operations

        op_data = operations_data.get(operation)
        if not op_data:
            print(f"Invalid operation: {operation}")
            exit(1)

        # Use URL from command line argument if provided, otherwise use default from operations.json
        # url = args.url if args.url else op_data['url'] 
        url =  op_data['url']

        method = op_data['method']
        headers = op_data.get('headers', {})

        # Construct query parameters
        queryParams = {param: getattr(args, param) for param in op_data.get('queryParams', {})}

        # Read data from input file if specified
        # if 'inputFile' in op_data:
        #     try:
        #         with open(args.input_file, 'r') as f:
        #             data = json.load(f)  # Assuming JSON input, adjust as needed
        #     except (FileNotFoundError, json.JSONDecodeError) as e:
        #         print(f"Error reading input file: {e}")
        #         exit(1)
        # else:
        #     data = {}

        # Construct the POST body data
        opArgs = {}
        for param in op_data.get('bodyParams', {}):
            opArgs[param] = getattr(args, param)
        
        data = {
            "operation": {
                "name": op_data.get('operationName', operation),  # Use operation name from definition or default to operation key
                "args": opArgs
            }
        }

        try:
            response = requests.request(method, url, 
                headers=headers, params=queryParams, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error executing operation: {e}")
            return None
