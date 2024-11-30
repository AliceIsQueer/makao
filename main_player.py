from player import Player


class MainPlayer(Player):
    """
    Class MainPlayer. Inherits from Player. Contains attributes:

    :param special_message: The messages to be displayed 
    to the player before their turn

    :type special_messages: List[str]

    :param error_message: Error message to be displayed
    to the player during special turns

    :type error_message: str
    """
    def __init__(self, name, cards=None):
        """Initialises the MainPlayer class"""
        super().__init__(name, cards)
        self._special_messages = []
        self._error_message = ''

    @property
    def special_messages(self):
        return self._special_messages

    @property
    def special_message(self):
        sentence = ''
        for message in self.special_messages:
            sentence += message
        return sentence

    @property
    def error_message(self):
        return self._error_message

    def add_special_message(self, new_message: str) -> None:
        """
        Adds a special message to display
        During the player's turn
        """
        self._special_messages.append(new_message)

    def clear_special_message(self) -> None:
        """Clears the special message array"""
        self._special_messages.clear()

    def set_error_message(self, new_message: str) -> None:
        """Sets an error message after a special interaction happens"""
        self._error_message = new_message

    def clear_error_message(self) -> None:
        """Clears the special error message"""
        self._error_message = ''
