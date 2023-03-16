class Delimiter():
    """
    This class contains methods that delimit messages meant for IO transfer.
    """
    
    def __init__(self) -> None:
        self._soh = "SOH"
        self._eot = "EOT"
        self._esc = "ESC"
        self._escsoh = "ESCX"
        self._esceot = "ESCY"
        self._escesc = "ESCZ"
    
    def encode_msg(self, msg: str):
        """
        This method encodes a string with a start-of-header and
        end-of-transmission tag at the beginning and end of the string,
        respectively. All occurrnces of SOH, EOT, and ESC (the literal escape
        tag) are replaced with respective escape tags.

        Args:
            
            msg (str): 
                This is the string to be encoded.

        Returns:
            
            (str): 
                This is the encoded string
        """
        msg = msg.replace(self._esc, self._escesc)
        msg = msg.replace(self._soh, self._escsoh)
        msg = msg.replace(self._eot, self._esceot)
        msg = ''.join([self._soh, msg, self._eot])
        return msg

    def decode_msg(self, msg: str):
        """
        This method decodes a string that has been encoded via ```Delimiter```.
        First, the message is checked for valid start-of-header and 
        end-of-transmission tags. Next, ```msg``` is parsed for occurrences
        of escape tags, which are subsequently replaced with their original
        text.

        Args:
            
            msg (str): 
                This is the string to be decoded.

        Raises:
            
            ValueError: 
                If ```msg``` is found to be without proper encoding, this error
                is raised

        Returns:
            
            (str): 
                This is the decoded string.
        """
        if not self._msg_is_valid(msg):
            raise ValueError("Message cannot be decoded")
        msg = msg.replace(self._escsoh, self._soh)
        msg = msg.replace(self._esceot, self._eot)
        msg = msg.replace(self._escesc, self._esc)
        msg = msg[3:-3]
        return msg
        
    def _msg_is_valid(self, msg):
        """
        This method checks ```msg``` for occurences of the start-of-header and
        the end-of-transmission tags at the beginning and end of ```msg```,
        respectively.

        Args:
            
            msg (str): 
                This is the message to be checked.

        Returns:
            
            (bool): 
                Returns ```True``` if the message has been encoded properly.
                
                Returns ```False``` if the message has not been encoded 
                properly.
        """
        if len(msg) < 6:
            return False
        if msg[:3] != self._soh:
            return False
        if msg[-3:] != self._eot:
            return False
        return True
    
    def _demo(self):
        """
        This is a demo method to quickly check the functionality of
        ```Delimiter```.
        """
        message = "This is my message SOH EOT ESC"
        message_encoded = self.encode_msg(message)
        message_decoded = self.decode_msg(message_encoded)
        print(message)
        print(message_encoded)
        print(message_decoded)
        if message_decoded == message:
            print(True)
            return
        print(False)
        