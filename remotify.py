import remotifyCommon as common

import logging
import argparse
import queue
import threading
from websockets.sync.client import connect
from websockets.exceptions import ConnectionClosed

# If the user isn't using the connection, we close it
CONNECTION_TIMEOUT = 60 
logger = logging.getLogger(__name__)
toSend = queue.Queue()

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
    
    comThread = threading.Thread(target=connectToServer, args=[args.host], daemon=True)
    comThread.start()
    
    # t should only die if an unhandled exception happens. In this case, there is no point filling the queue as it won't be consumed
    while comThread.is_alive():
        toSend.put(input(""))
         
def connectToServer(host:str):
    """Connect to the server via websocket. If the connection was closed deliberately, get ready to reopen it. 

    Args:
        host (str): _description_
    """
    print("Ready to connect to server")
    reconnect = True
    while(reconnect):
        try:
            connectOnce(host)
        except queue.Empty:
            logger.debug('User is inactive. Disconnecting websocket')
        except ConnectionClosed as cc:
            logger.warning('Connection was closed. Reopening it.', exc_info=cc)
            
def connectOnce(host:str) -> None:
    """Connect to the server via websocket upon first message received.
    Send all further messages until a timeout or an error happens
    Args:
        host (str): Name of the host we are connecting to
    Raises:
        queue.Empty: When there hasn't been any user input in {TIMEOUT} seconds
        ConnectionClosed: When the server has closed the connection
    """
    firstinput = toSend.get()
    with connect(f"ws://{host}:{common.DEFAULT_PORT}") as websocket:
        logger.info("Connected to server")
        websocket.send(firstinput)
        while True:
            websocket.send(toSend.get(timeout=60)) 
            toSend.task_done()
            
if __name__ == "__main__":
    main()