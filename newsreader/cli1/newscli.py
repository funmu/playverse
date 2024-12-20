# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  CLI module for operations
#
# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

# SERVICE SPECIFIC DEFINITIONS AND NAMING 
# TODO: auto generate from Verse or other manifests
SERVICE_NAME="news_api"
SERVICE_DEFINITIONS="newsapi.definitions.json"

from cliverse import CliRunner, JsonHelpers
import sys

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
#  Main Program

if __name__ == "__main__":

    # operation_definitions = args.ops if args.ops else CLI_OPERATIONS_FILE

    cliRunner = CliRunner()
    cliOpsParser = cliRunner.create_cli( SERVICE_NAME, SERVICE_DEFINITIONS)
    jsonResults = cliRunner.execute_operation( sys.argv)

    jsonHelpers = JsonHelpers()
    jsonHelpers.pretty_print_json( jsonResults)


