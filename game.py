from card_stack import CardStack
from opponent import Opponent
from player import Player, Status, WrongCardIndexError
from main_player import MainPlayer
from deck import Deck, EmptyDeckError
from typing import List
from card import Suits
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


class InvalidStatusTransferError(Exception):
    def __init__(self):
        super().__init__("You cannot play this card.")


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
        self._main_player = MainPlayer(player_name)
        self._players.append(self._main_player)
        for i in range(num_of_opponets):
            self._players.append(Opponent(f'Player{i+1}'))

        self._stack = CardStack()
        self._deck = Deck(self._stack)

        self._deck.shuffle_deck()

        self._stack.add_cards_on_top([self._deck.draw_card()])
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

    @property
    def main_player(self):
        return self._main_player

    def increment_turn(self) -> None:
        self._turn_num += 1

    def get_current_player(self) -> 'Player':
        return self.players[self.turn_num % len(self.players)]

    def get_player_index(self, player: 'Player') -> int:
        for index, plr in enumerate(self.players):
            if player == plr:
                return index

    def left_of_player(self, player: 'Player') -> 'Player':
        player_index = self.get_player_index(player)
        return self.players[(player_index-1) % len(self.players)]

    def prev_player(self, player: 'Player') -> 'Player':
        prev = self.left_of_player(player)
        while prev.status_effect == Status.BLOCKED:
            index = self.players.index(prev)
            prev = self.players[(index - 1) % len(self.players)]
        return prev

    def right_of_player(self, player: 'Player') -> 'Player':
        player_index = self.get_player_index(player)
        return self.players[(player_index+1) % len(self.players)]

    def next_player(self, player: 'Player'):
        next = self.right_of_player(player)
        while next.status_effect == Status.BLOCKED:
            index = self.players.index(next)
            next = self.players[(index + 1) % len(self.players)]
        return next

    def handle_turn(self) -> None:
        playing = self.get_current_player()

        clear_messages = False
        if playing.status_effect != Status.NOEFFECT:
            self.prepare_special_turn()

        if isinstance(playing, MainPlayer):
            clear_messages = True

        self.handle_player_turn()

        if playing.blocked_turns > 0:
            playing.decrement_block()

        if playing.cards_to_draw > 0:
            self.main_player.add_special_message(f'{playing} drew {playing.cards_to_draw} cards') # NOQA
            for _ in range(playing.cards_to_draw):
                playing.add_card(self.deck.draw_card())
            self.main_player.add_special_message(f' (at {len(playing.hand)} cards) \n') # NOQA
            playing.reset_cards_to_draw()

        self.progress_turn(clear_messages)

    def handle_player_turn(self) -> None:
        while True:
            try:
                moves = self.get_player_input()
                player = self.get_current_player()
                if isinstance(player, Opponent):
                    self.add_opponent_status(moves)

                if max(moves) > len(player.hand) or min(moves) < 0:
                    raise ValueError

                if player.allowed_cards != []:
                    self.handle_effect_turn(player, moves)
                    break

                if len(moves) == 1 and moves[0] == len(player.hand):
                    self.handle_pass(player)
                    break

                if len(moves) > 1 and len(player.hand) in moves:
                    raise ValueError

                cards_to_put = [player.hand[move] for move in moves]

                if not self.stack.is_valid_combo(cards_to_put):
                    raise InvalidTopCardError

                self.handle_regular_turn(player, moves)
                break

            except ValueError:
                self.main_player.set_error_message('This is not '
                                                   'a valid option\n')
            except InvalidTopCardError:
                self.main_player.set_error_message('You cannot put this '
                                                   'card on top of the '
                                                   'card pile\n')
            except EmptyDeckError:
                self.main_player.set_error_message('The deck is empty\n')
                break

            except WrongCardIndexError:
                pass

            except InvalidStatusTransferError:
                self.main_player.set_error_message("You cannot play this "
                                                   "card this turn\n")
                pass

    def progress_turn(self, clear: bool = True):
        if clear:
            self.main_player.clear_special_message()
            self.main_player.clear_error_message()
        self.increment_turn()
        self.handle_turn()

    def handle_regular_turn(self, player, moves):
        prev_player = self.prev_player(player)
        next_player = self.next_player(player)
        self.stack.add_cards_on_top(player.remove_cards(moves),
                                    prev_player, next_player,
                                    self.players)

    def handle_pass(self, player: 'Player'):
        card = self.deck.draw_card()

        player.add_card(card)

    def handle_effect_turn(self, player: 'Player', moves):
        if len(moves) > 1 or moves[0] > len(player.hand):
            raise InvalidStatusTransferError

        if len(moves) == 1 and moves[0] == len(player.hand):
            return

        card = player.hand[moves[0]].value
        if card not in player.allowed_cards:
            raise InvalidStatusTransferError

        prev_player = self.prev_player(player)
        next_player = self.next_player(player)

        if player.status_effect == Status.DRAW5:
            if card.suit in [Suits.CLUBS, Suits.Diamonds]:
                player.remove_status_effect()
            else:
                if self.stack.top_card.suit == Suits.SPADES:
                    player.transfer_effect(next_player)
                else:
                    player.transfer_effect(prev_player)
        else:
            player.transfer_effect(next_player)
        self.stack.add_cards_on_top(player.remove_cards(moves),
                                    prev_player, next_player,
                                    self.players)

    def get_player_input(self) -> List[int]:
        if isinstance(self.get_current_player(), (MainPlayer)):
            sentence = self.ask_player_input()
            moves = [int(card) - 1 for card in input(sentence).split(' ')]
        else:
            moves = [self.get_current_player().get_optimal_card(self.stack)]
        return moves

    def ask_player_input(self):
        os.system('clear')
        player = self._main_player

        additional_information = (self._main_player.special_message
                                  + self._main_player.error_message)
        if self._main_player.special_message != '':
            additional_information += '\n'

        special_message = (' and draw a card' if
                           player.status_effect == Status.NOEFFECT else '')

        first_part = str(self.stack) + '\n'
        second_part = self.get_current_player().get_hand_description()
        third_part = (f'{len(player.hand)+1} '
                      f'- Pass your turn{special_message}\n')
        fourth_part = 'Your option is: '

        sentence = (additional_information + first_part + second_part +
                    third_part + fourth_part)

        return sentence

    def add_opponent_status(self, card_indexes) -> None:
        opponent = self.get_current_player()
        main_player = self._main_player
        if card_indexes[0] == len(opponent.hand):
            message = ''
            if opponent.allowed_cards == []:
                message = 'and draws a card '

            hand_size = len(opponent.hand)
            main_player.add_special_message(f'{opponent.name} passes '
                                            f'{message}'
                                            f'({hand_size} cards left)\n')
        else:
            cards = [opponent.hand[index] for index in card_indexes]

            cards_played = [str(card) for card in cards]

            cards_string = ''
            for index, card in enumerate(cards_played):
                cards_string += card
                if index < len(cards_played) - 1:
                    cards_string += ' and '

            hand_size = len(opponent.hand)
            main_player.add_special_message(f'{opponent.name} '
                                            f'played {cards_string}'
                                            f'({hand_size} cards left)\n')

    def prepare_special_turn(self):
        playing = self.get_current_player()
        if playing.status_effect == Status.BLOCKED:
            message = ('' if playing.blocked_turns == 1
                       else f' for {playing.blocked_turns} turns')

            extra_message = ('You can play a 4 to transfer it to the next player\n' # NOQA
                             if playing.blocked_turns == playing.total_blocked_turns # NOQA
                             else '')

            block_message = (f'{playing.name} was blocked{message}\n'
                             if isinstance(playing, Opponent)
                             else (f'You have been blocked{message}!\n'
                                   f'{extra_message}'))

            self.main_player.add_special_message(block_message)
            playing.set_allowed_cards([4])
        elif playing.status_effect == Status.DRAW2OR3:
            extra_message = 'You can play a 2 or a 3 to transfer it to the next player\n' # NOQA

            block_message = (f'{playing.name} is about to draw '
                             f'{playing.cards_to_draw} cards\n'
                             if isinstance(playing, Opponent)
                             else (f'You are about to draw '
                                   f'{playing.cards_to_draw} cards!\n'
                                   f'{extra_message}'))

            self.main_player.add_special_message(block_message)
            playing.set_allowed_cards([2, 3])
        elif playing.status_effect == Status.DRAW5:
            extra_message = 'You can play a King to either negate the effect or return it to sender\n' # NOQA

            block_message = (f'{playing.name} is about to draw '
                             f'{playing.cards_to_draw} cards\n'
                             if isinstance(playing, Opponent)
                             else (f'You are about to draw '
                                   f'{playing.cards_to_draw} cards!\n'
                                   f'{extra_message}'))

            self.main_player.add_special_message(block_message)
            playing.set_allowed_cards([13])
