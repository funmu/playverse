# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  CLI module for operations
#
# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

# SERVICE SPECIFIC DEFINITIONS AND NAMING 
# TODO: auto generate from Verse or other manifests
SERVICE_NAME="news_api"
SERVICE_DEFINITIONS="newsapi.definitions.json"

NAME_OF_THIS_CLI=SERVICE_NAME+"_cli"
DESCRIPTION_OF_THIS_CLI="CLI for using the " + SERVICE_NAME
THANK_YOU_MESSAGE="Thanks for using " + NAME_OF_THIS_CLI


# TODO: Move the helpers to separate module and import them in
# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  JSON helpers
import json

def load_rest_operations(input_file):
    """Loads REST operations from a JSON file."""
    try:
        with open(input_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {SERVICE_NAME} REST operations: {e}")
        exit(1)

def pretty_print_json(json_data):
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

def create_main_parser():
    parser = argparse.ArgumentParser(
        prog=NAME_OF_THIS_CLI,
        description=DESCRIPTION_OF_THIS_CLI,
        epilog=THANK_YOU_MESSAGE
        )
    parser.add_argument( "operation", help="operation to be conducted")

    # Use follwoing if we want to configure where the service definitions come from
    # parser.add_argument("--ops", help="Override the default operations definitions using this file")  
   
    # Add argument for URL to send the request to
    parser.add_argument("--url", help="Override the default URL for the operation")  

    return parser

def create_cli(parser, operations):
    """
    Creates a CLI sub parsers based on REST operations.
    """
    subparsers = parser.add_subparsers(dest='operation', required=True)

    for op_name, op_data in operations.items():
        
        subparser = subparsers.add_parser(op_name, help=op_data.get('help', ''))

        # Add arguments for query parameters
        for param_name, param_data in op_data.get('queryParams', {}).items():
            subparser.add_argument(f"--{param_name}", help=param_data.get('help', ''), required=param_data.get('required', False))

        for param_name, param_data in op_data.get('bodyParams', {}).items():
            subparser.add_argument(f"--{param_name}", help=param_data.get('help', ''), required=param_data.get('required', False))

        # Add argument for input file
        if 'inputFile' in op_data:
            subparser.add_argument("input_file", help=op_data['inputFile'].get('help', ''))

    return parser

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  Do Operations
import requests

def execute_operation(operation, args, operations_data):
    """Executes the specified REST operation."""
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
        # print(response.json())
        pretty_print_json(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error executing operation: {e}")
        exit(1)

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  Main Program

if __name__ == "__main__":

    parser = create_main_parser()

    # operation_definitions = args.ops if args.ops else CLI_OPERATIONS_FILE
    operation_definitions = SERVICE_DEFINITIONS
    operations_data = load_rest_operations(operation_definitions)

    cli_parser = create_cli(parser, operations_data)

    cli_args = cli_parser.parse_args( sys.argv)

    execute_operation(cli_args.operation, cli_args, operations_data)
