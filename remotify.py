import remotifyCommon as common

import logging
import argparse
from websockets.sync.client import connect

logger = logging.getLogger(__name__)

DEFAULT_HOST = 'localhost'

def initArgParser() -> argparse.Namespace:
    """Defines the arguments that the program can use

    Returns:
        argparse.Namespace: The argument values the user specified to the application
    """
    parser = argparse.ArgumentParser(prog="remotify.py", 
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=f'''\
Start an interactive session to send media control commands to a remotifier server. {common.SERVER_COMMAND_DESCRIPTION}
''')
    parser.add_argument("--host", help="IP or name of the machine to control", default=DEFAULT_HOST)
    return parser.parse_args()

def main(): 
    logging.basicConfig(filename='remotify.log', level=logging.DEBUG)
    args = initArgParser()
    with connect(f"ws://{args.host}:{common.DEFAULT_PORT}") as websocket:
        while True:
            try:
                websocket.send(input(""))
            except KeyboardInterrupt:
                logger.info("Interrupt received, terminating session.")
                break
            
if __name__ == "__main__":
    main()