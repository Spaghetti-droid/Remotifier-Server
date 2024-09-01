import remotifyCommon as common

import logging
import argparse
from websockets.sync.client import connect
from websockets.exceptions import ConnectionClosed
from inputimeout import inputimeout, TimeoutOccurred

logger = logging.getLogger(__name__)

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
    parser.add_argument("host", help="IP or name of the machine to control")
    return parser.parse_args()

def main(): 
    logging.basicConfig(filename='remotify.log', level=logging.DEBUG)
    args = initArgParser()
    reconnect = True
    while reconnect:
        reconnect = connectToServer(args.host)
            
def connectToServer(host:str) -> bool:
    """Connect to the server. Returns when connection has been closed.
    Args:
        host (str): Name of the host we are connecting to
    Returns:
        bool: True if we should wait for next user input and try to reopen the connection
    """
    firstinput = input("")
    with connect(f"ws://{host}:{common.DEFAULT_PORT}") as websocket:
        websocket.send(firstinput)
        while True:
            try:
                websocket.send(inputimeout("", timeout=60))
            except TimeoutOccurred:
                logger.debug("User inactive. Closing connection.")
                return True
            except KeyboardInterrupt:
                logger.debug("Interrupt received, terminating session.")
                return False
            except ConnectionClosed as cc:
                logger.warning("Connection is closed. Send cancelled", exc_info=cc)
                return True
            
if __name__ == "__main__":
    main()