import asyncio
import logging
import socket
from websockets.asyncio.server import serve
from pynput.keyboard import Key, Controller

logger = logging.getLogger(__name__)
keyboard = Controller()

DEFAULT_PORT = 42121

async def main():  
    logging.basicConfig(filename='remotifierServer.log', level=logging.DEBUG)
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
        case _:
            logger.warning(f"Input not recognised: '{c}'")
            return None
        

if __name__ == "__main__":
    asyncio.run(main())