from .chat import Chat

class Server(Chat):
    """
    This is the child class of ```Chat``` that handles server interaction.

    Args:
        
        Chat (Chat): 
            The parent class ```Chat``` contains most of the handlers for socket
            interaction, message parsing, and terminal interaction.
    """
    
    def __init__(self) -> None:
        super().__init__()
        
    def run(self):
        """
        This is a driver method to begin a ```Server``` session. The server will
        bind to a socket at ```self.SOCKADDR```, and it will begin listening on
        that socket. After a connection is accepted, the server will begin
        exchanging messages with the connected client. Once a message to
        terminate is received, the server will return.
        """
        self._bind_socket()
        self._wait_for_connection()
        if self._receive_message() == self.STOP:
            return
        self.print_help()
        while True:
            if self._send_message() == self.STOP:
                return
            if self._receive_message() == self.STOP:
                return
