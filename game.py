from player import Player
from card_stack import CardStack
from opponent import Opponent
from deck import Deck
from typing import List
import os


class InvalidOppNumError(Exception):
    def __init__(self):
        super().__init__("The number of opponents has to be between 1 and 3.")


class InvalidMoveError(Exception):
    def __init__(self):
        super().__init__("This is not a valid move.")


class InvalidTopCardError(Exception):
    def __init__(self):
        super().__init__("You cannot put this card on top of the card stack.")


class Game:
    """
    Class Game. Contains attributes:

    :param players: The list of players taking part in the game
    :type players: List['Player']

    :param deck: The deck used in this game
    :type deck: 'Deck'

    :param stack: The card stack used in the game
    :type stack: 'Stack'

    :param turn_num: The current game's turn
    :type turn_num: int
    """
    def __init__(self, player_name: str, num_of_opponets: int) -> None:
        if num_of_opponets < 1 or num_of_opponets > 3:
            raise InvalidOppNumError()

        self._players = []
        self._players.append(Player(player_name))
        for i in range(num_of_opponets):
            self._players.append(Opponent(f'Player{i+1}'))

        self._deck = Deck()
        self._stack = CardStack()

        self._previous_turn_message = ''

        self._deck.shuffle_deck()

        self._stack.add_card_on_top(self._deck.draw_card())
        for i in range(5):
            for player in self._players:
                player.add_card(self._deck.draw_card())

        self._turn_num = 0
        self.handle_turn()

    @property
    def players(self) -> List['Deck']:
        return self._players

    @property
    def deck(self) -> 'Deck':
        return self._deck

    @property
    def stack(self) -> 'CardStack':
        return self._stack

    @property
    def turn_num(self) -> int:
        return self._turn_num

    def increment_turn(self) -> None:
        self._turn_num += 1

    def get_current_player(self) -> 'Player':
        return self.players[self.turn_num % len(self.players)]

    def left_of_player(self, player_index: int) -> 'Player':
        return self.players[(player_index-1) % len(self.players)]

    def right_of_player(self, player_index: int) -> 'Player':
        return self.players[(player_index+1) % len(self.players)]

    def handle_turn(self) -> None:
        playing = self.get_current_player()
        if not isinstance(playing, Opponent):
            self.handle_player_turn()
        else:
            self.handle_opponent_turn()

    def handle_player_turn(self) -> None:
        while True:
            os.system('clear')
            player = self.get_current_player()

            additional_information = self._previous_turn_message
            if self._previous_turn_message != '':
                additional_information += '\n'

            first_part = str(self.stack) + '\n'
            second_part = self.get_current_player().get_hand_description()
            third_part = f'{len(player.hand)+1} - Pass your turn and draw a card \n'
            fourth_part = 'Your option is: '

            sentence = (additional_information + first_part + second_part +
                        third_part + fourth_part)
            try:
                move = int(input(sentence)) - 1
                if move > len(player.hand) or move < 0:
                    raise InvalidMoveError

                else:
                    if move == len(player.hand):
                        player.add_card(self.deck.draw_card())
                        self.increment_turn()
                        self.handle_turn()
                        break

                    card_to_put = player.hand[move]

                    if not card_to_put.can_put_card(self.stack.top_card):
                        raise InvalidTopCardError

                    else:
                        self.stack.add_card_on_top(player.remove_card(move))
                        self.increment_turn()
                        self.handle_turn()

                        break
            except InvalidMoveError:
                self._previous_turn_message = 'This is not a valid option'
            except InvalidTopCardError:
                self._previous_turn_message = ('You cannot put this '
                                               'card on top of the card pile\n')

    def handle_opponent_turn(self) -> None:
        opponent = self.get_current_player()
        card_index = opponent.get_optimal_card(self.stack)

        if card_index == -1:
            opponent.add_card(self.deck.draw_card())
            self._previous_turn_message = 'Your opponent passes and draws a card\n'
            self.increment_turn()
            self.handle_turn()
        else:
            card = opponent.hand[card_index]
            self.stack.add_card_on_top(opponent.remove_card(card_index))
            self._previous_turn_message = f'Your opponent played {card}\n'
            self.increment_turn()
            self.handle_turn()
