from .chat import Chat

class Client(Chat):
    """
    This is the child class of ```Chat``` that handles client interaction.

    Args:
        
        Chat (Chat): 
            The parent class ```Chat``` contains most of the handlers for socket
            interaction, message parsing, and terminal interaction.
        
    """
    
    def __init__(self) -> None:
        super().__init__()
        
    def run(self):
        """
        This is a driver method to begin a ```Client``` session. The client will
        connect to a socket at ```self.SOCKADDR```, and it will begin exchanging
        messages with a ```Server```. Once a message to terminate is received,
        the client will return.
        """
        self._connect_socket()
        self.print_help()
        while True:
            if self._send_message() == self.STOP:
                return
            if self._receive_message() == self.STOP:
                return
    
        