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
    parser.add_argument("-l", "--log-level", dest="logLevel", help=f"Level of detail for logged events. Default: {common.DEFAULT_LOG_LEVEL}", default=common.DEFAULT_LOG_LEVEL)
    parser.add_argument("-p", "--port", help=f"Host port to connect to. Normally, this can be left at the default value. Default: {common.DEFAULT_PORT}.", default=common.DEFAULT_PORT)
    return parser.parse_args()

def main(): 
    args = initArgParser()
    logging.basicConfig(format=common.LOG_FORMAT, filename='remotify.log', level=args.logLevel.upper())
    
    try:
        logger.warning("Starting up")
        
        comThread = threading.Thread(target=connectToServer, args=[args.host, args.port], daemon=True)
        comThread.start()
        
        # comThread should only die if an unhandled exception happens. In this case, there is no point filling the queue as it won't be consumed
        while comThread.is_alive():
            toSend.put(input(""))
    except KeyboardInterrupt:
        logger.debug("Keyboard interrupt received. Shutting down.")
    finally:
        logger.warning("Shutting down")
         
def connectToServer(host:str, port:int):
    """Connect to the server via websocket. If the connection was closed deliberately, get ready to reopen it. 

    Args:
        host (str): 
        port (int)
    """
    print("Ready to connect to server")
    reconnect = True
    while(reconnect):
        try:
            connectOnce(host, port)
        except queue.Empty:
            logger.debug('User is inactive. Disconnecting websocket')
        except ConnectionClosed as cc:
            logger.warning('Connection was closed. Reopening it.', exc_info=cc)
            
def connectOnce(host:str, port:int) -> None:
    """Connect to the server via websocket upon first message received.
    Send all further messages until a timeout or an error happens
    Args:
        host (str): Name of the host we are connecting to
    Raises:
        queue.Empty: When there hasn't been any user input in {TIMEOUT} seconds
        ConnectionClosed: When the server has closed the connection
    """
    firstinput = toSend.get()
    with connect(f"ws://{host}:{port}") as websocket:
        logger.info("Connected to server")
        websocket.send(firstinput)
        while True:
            websocket.send(toSend.get(timeout=60)) 
            toSend.task_done()
            
if __name__ == "__main__":
    main()