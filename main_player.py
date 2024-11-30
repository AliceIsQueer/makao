from player import Player


class MainPlayer(Player):
    def __init__(self, name, cards=None):
        super().__init__(name, cards)
        self._special_message = ''

    @property
    def special_message(self):
        return self._special_message

    def add_special_message(self, new_message):
        self._special_message += new_message

    def clear_special_message(self):
        self._special_message = ''
