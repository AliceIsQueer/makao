from player import Player


class MainPlayer(Player):
    def __init__(self, name, cards=None):
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

    def add_special_message(self, new_message):
        self._special_messages.append(new_message)

    def clear_special_message(self):
        self._special_messages.clear()

    def set_error_message(self, new_message):
        self._error_message = new_message

    def clear_error_message(self):
        self._error_message = ''
