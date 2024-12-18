import argparse
import json
import requests

NAME_OF_THIS_CLI="CLI for news_api"
CLI_OPERATIONS_FILE="newsapi.definitions.json"

def load_rest_operations(input_file):
    """Loads REST operations from a JSON file."""
    try:
        with open(input_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading REST operations: {e}")
        exit(1)

def create_cli(operations):
    """Creates a CLI parser based on REST operations."""
    parser = argparse.ArgumentParser(description=NAME_OF_THIS_CLI)
    subparsers = parser.add_subparsers(dest='operation', required=True)

    for op_name, op_data in operations.items():
        subparser = subparsers.add_parser(op_name, help=op_data.get('help', ''))

        # Add arguments for query parameters
        for param_name, param_data in op_data.get('queryParams', {}).items():
            subparser.add_argument(f"--{param_name}", help=param_data.get('help', ''), required=param_data.get('required', False))

        # Add argument for input file
        if 'inputFile' in op_data:
            subparser.add_argument("input_file", help=op_data['inputFile'].get('help', ''))

    return parser

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
    params = {param: getattr(args, param) for param in op_data.get('queryParams', {})}

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
    data = {
        "operation": {
            "name": op_data.get('operationName', operation),  # Use operation name from definition or default to operation key
            "args": {}  # You can add operation-specific arguments here if needed
        }
    }
    try:
        response = requests.request(method, url, headers=headers, params=params, json=data)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error executing operation: {e}")
        exit(1)

def parse_arguments():
    parser = argparse.ArgumentParser(description=NAME_OF_THIS_CLI)
    parser.add_argument( "operation", help="operation to be conducted")

    parser.add_argument("--ops", help="Override the default operations definitions using this file")  
#    parser.add_argument("input_file", help="JSON file with REST operation definitions")
   
    # Add argument for URL
    parser.add_argument("--url", help="Override the default URL for the operation")  

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_arguments()

    operation_definitions = args.ops if args.ops else CLI_OPERATIONS_FILE
    operations_data = load_rest_operations(operation_definitions)
    cli_parser = create_cli(operations_data)
    cli_args = cli_parser.parse_args()

    execute_operation(cli_args.operation, cli_args, operations_data)
