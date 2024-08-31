import logging
from websockets.sync.client import connect

logger = logging.getLogger(__name__)

DEFAULT_PORT = 42121

def main(): 
    logging.basicConfig(filename='remotifier.log', level=logging.DEBUG)
    with connect(f"ws://localhost:{DEFAULT_PORT}") as websocket:
        while True:
            try:
                websocket.send(input(""))
            except KeyboardInterrupt:
                logger.info("Interrupt received, terminating session.")
                break
            
if __name__ == "__main__":
    main()