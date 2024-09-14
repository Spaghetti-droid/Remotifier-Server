# Constants that are shared between server and client

DEFAULT_PORT = 42121
DEFAULT_LOG_LEVEL = "WARNING"

SERVER_COMMAND_DESCRIPTION = """\
Commands recognised by the server:

    - 'p': Play/Pause
    - 'n': Next Track
    - 'b': Back/Previous Track
    - 'u': Volume Up
    - 'd': Volume Down
    - 'm': Mute
    - '>': Press Forewards key
    - '<': Press Backwards key
    - '^': Press Up Key
    - 'v': Press Down Key
    - 'e': Press Enter Key
    - '!': Enter literal mode. All characters after this one will be interpreted as requests to press that character's key. For example '!fish' will cause the host to press the 'f', 'i', 's', 'h' keys.
    
Several commands can be chained together (ie 'uuu' will increase volume 3 times)
"""