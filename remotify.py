import remotifyCommon as common

import logging
import argparse
import asyncio
from websockets.asyncio.client import connect

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
    reconnect = await connectToServer(args.host)
    while reconnect:
        print("Attempting to reconnect to server")
        reconnect = await connectToServer(args.host)
            
            
async def connectToServer(host:str) -> bool:
    async with connect(f"ws://{host}:{common.DEFAULT_PORT}") as websocket:
        print(f"Connected to server")
        while True:
            try:
                toSend = input("")
                async with asyncio.timeout(delay=5):
                    await websocket.send(toSend)
                    await asyncio.sleep(0)  # yield control to the event loop
            except KeyboardInterrupt:
                logger.info("Interrupt received, terminating session.")
                return False
            except TimeoutError:
                logger.info("Send timed out. Closing connection.")
                return True
            except Exception as e:
                logger.error("Exception during connection", e)
                return False
            
if __name__ == "__main__":
    asyncio.run(main())