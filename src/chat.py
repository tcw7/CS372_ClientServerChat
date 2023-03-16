# reference:
# [Python3 socket docs](https://docs.python.org/3/library/socket.html#socket.socket.connect)
# [StringIO guide](https://www.geeksforgeeks.org/stringio-module-in-python/)
# [bytes encoding/decoding](https://stackoverflow.com/questions/14472650/python-3-encode-decode-vs-bytes-str)

from socket import socket
from .delimiter import Delimiter
from io import StringIO
from time import sleep

class Chat():
    """
    The ```Chat``` class includes the majority of the driver code for the child
    classes ```Server``` and ```Client```. ```Chat``` Handles socket
    manipulation and IO. It uses the ```Delimiter``` class to render messages,
    and it relies on ```Delimiter``` encoding/decoding to determine the start
    and beginning of messages.

    Raises:
        
        BrokenPipeError: 
            This error is raised when something has gone wrong
            while performing operations on a socket. 
        
        ValueError: 
            This error is raised when the contents of a recevied
            message do not contain the proper start-of-header or
            end-of-transmission values.
    """
    PORTNUM = 7171
    ADDRESS = "localhost"
    SOCKETADDR = (ADDRESS, PORTNUM)
    CONTINUE = "continue"
    STOP = "stop"
    ERROR = "error"
    
    def __init__(self) -> None:
        self._delimiter = Delimiter()
        self._socket = socket()
        self._socket_server = None
    
    def _connect_socket(self):
        """
        This is a handler for clients to connect to the ```SOCKETADDR```.

        Raises:
            
            BrokenPipeError: 
                This error is thrown if something has gone wrong
                while attempting to connect to the socket at ```SOCKETADDR```.
        """
        try: self._socket.connect(self.SOCKETADDR)
        except: raise BrokenPipeError("Connection failed.")
        print(
            f"Connected to {self.SOCKETADDR}."
        )

    def _bind_socket(self):
        """
        This is a handler for servers to bind and listen on a socket at
        ```SOCKETADDR```.

        Raises:
            
            BrokenPipeError: 
                This error is raised if there is some problem
                while attempting to bind the server to the socket
                or listen on the binded socket.
        """
        try: 
            self._socket.bind(self.SOCKETADDR)
            self._socket.listen()
            print(f"Server listening on {self.SOCKETADDR}")
        except: 
            raise BrokenPipeError(f"Could not bind to {self.SOCKETADDR}")
        
    def _send_socket(self, msg: str):
        """
        This sends ```msg``` to the connected socket in order to transmit the
        message to the other end of the pipe. First, ```msg``` is encoded as
        bytes before sending to the connected socket.

        Args:
            
            msg (str): 
                This is the message to be sent. ```msg``` should be of
                type ```str```.

        Raises:
            
            BrokenPipeError: 
                This error is thrown if ```msg``` fails to send
                through the connected socket.
        """
        msg = bytes(msg, encoding="utf-8")
        try: self._socket.send(msg)
        except: raise BrokenPipeError("Error sending message.")

    def _send_message(self):
        """
        This is the higher-level method to be used by ```Client``` or
        ```Server``` for sending messages to each other. The message is gathered
        from the user via terminal input first. Then, the message is encoded
        using the ```Delimiter```. Finally, the message is decoded and checked
        for a user request to end the chat.

        Returns:
            
            (str): 
                This method returns a string literal that indicates to the
                caller (```Server``` or ```Client```) whether the user has
                requested to end the chat.

            STOP = "stop"; 
                indicates that the user has requested to end
                the chat.
        """
        message = input("> ")
        message = self._delimiter.encode_msg(message)
        self._send_socket(message)
        message = self._delimiter.decode_msg(message)
        if message == "\q":
            self._end_chat()
            return self.STOP
        return self.CONTINUE
        
    def _end_chat(self):
        """
        This is a wrapper method to indicate to the user that the chat is
        ending. Subsequently, the respective sockets are closed.
        """
        print("Ending the chat...")
        self._close_socket()

    def _receive_message(self):
        """
        This is a higher-level method for ```Client``` and ```Server``` to
        receive messages from a connected socket. First, the message is
        received from the connected socket, then the message is decoded using
        the ```Delimiter```. Finally, the decoded message is checked for a
        request to end the chat.

        Returns:
            
            (str): 
                This method returns a constant string literal that indicates
                to the caller (```Client``` or ```Server```) whether the
                correspondent at the endpoint has requested to end the chat.
                
            STOP = "stop"; 
                indicates that the chat should stop.
        """
        message = self._recv_socket()
        message = self._delimiter.decode_msg(message)
        print(message)
        if message == "\q":
            self._end_chat()
            return self.STOP

            
    def print_help(self):
        """
        This method prints help instructions to the terminal
        for the user to begin chatting.
        """
        print(
            "Type \q to quit.\n"\
            "Enter a message..."
        )

    def _wait_for_connection(self):
        """
        This method handles the process of waiting for a connection on the 
        binded server socket. The resulting socket overwrites the original
        binded socket, which is saved before overwriting.
        """
        while True:
            try: 
                self._socket_server = self._socket
                self._socket, ret_addr = self._socket.accept()
                print(
                    f"Connection established with {ret_addr}."
                )
                return
            except:
                sleep(1)
        
    def _close_socket(self):
        """
        This method closes all opened or connected sockets. For ```Server```s,
        this method will also close the originally binded socket as well.

        Raises:
            
            BrokenPipeError: 
                This error is raised if a socket cannot be closed
                for some reason.
        """
        try: self._socket.close()
        except: raise BrokenPipeError("Couldn't close the socket.")
        if self._socket_server:
            try: self._socket_server.close()
            except: raise BrokenPipeError("Couldn't close the socket")
        
    def _recv_socket(self):
        """
        This method is the lower-level handler for receiving data from the
        connected socket. A ```StringIO``` is used to efficiently write bytes
        received from the socket into a dynamic buffer. Bytes are iteratviely
        written to the buffer; each iteration writes one byte to the buffer.
        After each byte is written to the buffer, the message is checked for
        validity. Once the message has been fully received, it is returned
        as a string.

        Returns:
            
            (str): 
                This is the resulting message.
        """
        message = StringIO("")
        while True:
            byte = self._socket.recv(1).decode()
            message.write(byte)
            try: 
                if not self._recv_should_continue(message):
                    break
            except: return None
        return message.getvalue()
            
    def _recv_should_continue(self, msg: StringIO):
        """
        This is a wrapper that returns a conditional string based on the
        contents of ```msg```.

        Args:
            
            msg (StringIO): 
                This is the message buffer to be checked.

        Raises:
            
            ValueError: 
                This error is thrown if the message is found to contain
                an error, such as a bad header.

        Returns:
            
            (bool): 
                True = continue receiving more bytes.
                
                False = stop reading bytes from the connected socket.
        """
        result = self._check_recv_msg(msg=msg)
        if result == self.ERROR:
            raise ValueError("Message received is invalid.")
        if result == self.STOP:
            return False
        return True
    
    def _check_recv_msg(self, msg: StringIO):
        """
        This method performs a series of checks on ```msg```. First, ```msg```
        is converted to a string. Then, its length is checked; if less than 3,
        a continue message is returned. Next, if the length of ```msg``` is 3,
        it is checked for a valid header ("SOH"); based on the validity of the
        header, a constant string literal is returned. If the previous checks
        pass, then the message is check for and end-of-transmission delimiter.
        If the EOT delimiter is found, then a stop message is returned;
        otherwise, a conitnue message is returned.

        Args:
            
            msg (StringIO): 
                This is the message to check.

        Returns:
            
            (str): 
                This is the constant string literal to indicate the
                resulting status of the message based on the delimiters.
                
            CONTINUE = "continue"; 
                indicates that more bytes are required to end recv.
                
            STOP = "stop"; 
                indicates that a valid message has been read, and recv should 
                end.
                
            ERROR = "error";
                indicates that the message does not have a
                valid start-of-header, recv is compromised for this message.
        """
        msg = msg.getvalue()
        if len(msg) < 3:
            return self.CONTINUE
        if len(msg) == 3:
            soh = msg[:3]
            if soh != self._delimiter._soh:
                return self.ERROR
            return self.CONTINUE
        eot = msg[-3:]
        if eot == self._delimiter._eot:
            return self.STOP
        return self.CONTINUE
            