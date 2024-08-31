import argparse
import asyncio
import logging
import socket
from websockets.asyncio.server import serve
from pynput.keyboard import Key, Controller

logger = logging.getLogger(__name__)
keyboard = Controller()

DEFAULT_PORT = 42121

def initArgParser() -> argparse.Namespace:
    """Defines the arguments that the program can use

    Returns:
        argparse.Namespace: The argument values the user specified to the application
    """
    parser = argparse.ArgumentParser(prog="remotifier.py", 
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='''\
Start a remotifier server, which listens for single-character commands to execute. Commands recognised by the server:

    -'p':'Play/Pause'
    -'n':'Next'
    -'b':'Back'
    -'u':'Volume Up'
    -'d':'Volume Down'
    -'m':'Mute'
    -'>':'Press Forewards key'
    -'<':'Press Backwards key'
    - 0 to 9, 'f', 'j', 'l', 's':'Press this key' (Useful for common streaming service shortcuts)
    
Several commands can be chained together (ie 'uuu' will increase volume 3 times)
''')
    return parser.parse_args()

async def main():  
    logging.basicConfig(filename='remotifierServer.log', level=logging.DEBUG)
    initArgParser()
    logger.info("Server starting up")
    async with serve(listen, "", DEFAULT_PORT):
        hostIdMessage = f'Listening on host: {socket.gethostname()}'
        print(hostIdMessage)
        logger.info(hostIdMessage)
        await asyncio.get_running_loop().create_future() 

async def listen(websocket):
    """Listen for commands on websocket
    Args:
        websocket
    """
    async for message in websocket:
        logger.debug(f"Recieved input:'{message}'")
        for c in message:
            key = getKey(c)
            if key:
                keyboard.press(key)
                keyboard.release(key)
        
def getKey(c: str) -> Key:
    """Convert c into a Key
    Args:
        c (str): A character representing an operation to perform
    Returns:
        Key: The key press that the character represents
    """
    match c:
        case 'p':
            return Key.media_play_pause
        case 'n':
            return Key.media_next
        case 'b':
            return Key.media_previous
        case 'u':
            return Key.media_volume_up
        case 'd':
            return Key.media_volume_down
        case 'm':
            return Key.media_volume_mute
        case '>':
            # Common +5s key
            return Key.right
        case '<':
            # Common -5s key
            return Key.left
        case 'j':
            # Common +10s key
            return 'j'
        case 'l':
            # Common -10s key
            return 'l'
        case 's':
            # Common skip intro key
            return 's'
        case 'f':
            # Common toggle fullscreen key
            return 'f'
        case _:
            try:
                # 0-9 are common seek x0% keys
                int(c)
                return c
            except ValueError:
                logger.warning(f"Input not recognised: '{c}'")
                return None
        

if __name__ == "__main__":
    asyncio.run(main())