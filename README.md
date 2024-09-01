# Remotify
A server and client pair that allow the control of media playing on the server host by the client


## Installation
### Using the exe files
Copy the file you want to use to where you want it. Take remotify.exe for the client, and remotifyServer.exe for the server.
### Using sources
Copy the necessary source files where you want them. The remotifyCommon.py file is needed by both the server and the client. For a server installation you'll need remotifyServer.py and the common file. For a client installation you'll need the common file and remotify.py.
#### Dependencies
These programs depend on the following dependencies:    
1. For both server and client, you'll need the 'websockets' package
2. For the server you'll also need the 'pynput' dependency

Install these using
    
    pip install <dependency name>

## Usage

Note all documentation below uses the python files. The executables should be called in the command line directly, without going through python.

### Starting the Server

      python remotifyServer.py -h

      usage: remotifyServer.py [-h]

      Start a remotify server, which listens for single-character commands to execute. Commands recognised by the server:

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

      options:
        -h, --help  show this help message and exit

Execute the server by running either of the following command in the command line:

    python remotifyServer.py
or 

    remotifyServer.exe

The executable will respond with the following text

    Listening on host: <Host Name>

This indicates that the server has started up.

### Starting the Client

    python remotify.py -h

    usage: remotify.py [-h] host

    Start an interactive session to send media control commands to a remotifier server. Commands recognised by the server:

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

    positional arguments:
        host        IP or name of the machine to control

    options:
        -h, --help  show this help message and exit

The client is run using
    
    python remotify.py <Host Name>

or

    remotify.exe <Host Name>

where the host name can be found from the the server's startup message.

### Controlling the server using the client

The client expects a series of characters terminated by a return, where each character is a command to be sent (see the lists above).   
For example to start playing a video, put the volume up 3 times, and then move on to the next video, one would write `puuun` into the command prompt.

## Known issues
### Server stops reacting to client after client machine was suspended
This happens because the server closes the connection, but the client is not aware of the connection being closed. Waiting 60 seconds should allow the client to reset itself.

## Generating the exe files
The exes can be generated using pyinstaller. In the project root directory, execute:
    
    pyinstaller -F remotify.py
    pyinstaller -F remotifyServer.py

    