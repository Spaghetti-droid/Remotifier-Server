import logging
import argparse
from websockets.sync.client import connect

logger = logging.getLogger(__name__)

DEFAULT_PORT = 42121
DEFAULT_HOST = 'localhost'

def initArgParser() -> argparse.Namespace:
    """Defines the arguments that the program can use

    Returns:
        argparse.Namespace: The argument values the user specified to the application
    """
    parser = argparse.ArgumentParser(prog="remotifier.py", 
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='''\
Start an interactive session to send media control commands to a remotifier server. Commands recognised by the server:

    -'p':'Play/Pause'
    -'n':'Next'
    -'b':'Back'
    -'u':'Volume Up'
    -'d':'Volume Down'
    -'m':'Mute'
    
Several commands can be chained together (ie 'uuu' will increase volume 3 times)
''')
    parser.add_argument("--host", help="IP or name of the machine to control")
    return parser.parse_args()

def main(): 
    logging.basicConfig(filename='remotifier.log', level=logging.DEBUG)
    args = initArgParser()
    with connect(f"ws://{args.host}:{DEFAULT_PORT}") as websocket:
        while True:
            try:
                websocket.send(input(""))
            except KeyboardInterrupt:
                logger.info("Interrupt received, terminating session.")
                break
            
if __name__ == "__main__":
    main()