import remotifyCommon as common

import logging
import argparse
import asyncio
from websockets.sync.client import connect

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

async def main(): 
    logging.basicConfig(filename='remotify.log', level=logging.DEBUG)
    args = initArgParser()
    reconnect = connectToServer(args.host)
    while reconnect:
        connectToServer(args.host)
            
            
async def connectToServer(host:str) -> bool:
    async with connect(f"ws://{host}:{common.DEFAULT_PORT}") as websocket:
        while True:
            try:
                websocket.send(input(""))
                websocket.recv()
            except KeyboardInterrupt:
                logger.info("Interrupt received, terminating session.")
                return False
            except Exception as e:
                logger.error("Exception during connection", e)
                return True
            
if __name__ == "__main__":
    asyncio.run(main())