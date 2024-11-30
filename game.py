from card_stack import CardStack
from card import Card
from card_stack import KingOfSpadesException, AceException, JackException
from opponent import Opponent
from player import Player, Status, WrongCardIndexError
from main_player import MainPlayer
from deck import Deck, EmptyDeckError
from typing import List
from card import Suits
from colorama import Fore, Style
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

        self._winners = []

        self._turn_num = 0
        self.handle_turn()

    @property
    def players(self) -> List['Player']:
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

    @property
    def winners(self):
        return self._winners

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
        while prev.status_effect == Status.BLOCKED or prev.won:
            index = self.players.index(prev)
            prev = self.players[(index - 1) % len(self.players)]
        return prev

    def right_of_player(self, player: 'Player') -> 'Player':
        player_index = self.get_player_index(player)
        return self.players[(player_index+1) % len(self.players)]

    def next_player(self, player: 'Player'):
        next = self.right_of_player(player)
        while next.status_effect == Status.BLOCKED or next.won:
            index = self.players.index(next)
            next = self.players[(index + 1) % len(self.players)]
        return next

    def handle_turn(self) -> None:
        if len(self.winners) == len(self.players) - 1:
            self.finish_game()
            return

        player = self.get_current_player()

        if player.won:
            self.progress_turn(False)
            return

        clear_messages = False
        if player.status_effect != Status.NOEFFECT:
            self.prepare_special_turn(player)

        if isinstance(player, MainPlayer):
            clear_messages = True

        self.handle_player_turn(player)

        if (self.stack.top_card.suit == Suits.SPADES and
           self.stack.top_card.value == 13):
            clear_messages = False

        if player.blocked_turns > 0:
            player.decrement_block()

        if player.cards_to_draw > 0:
            self.main_player.add_special_message(f'{player} drew {player.cards_to_draw} cards') # NOQA
            for _ in range(player.cards_to_draw):
                player.add_card(self.deck.draw_card())
            self.main_player.add_special_message(f' (at {len(player.hand)} cards) \n') # NOQA
            player.remove_status_effect()

        if player.status_effect == Status.FORCESUIT and not player.played_jack:
            player.remove_status_effect()
            self.check_stack_forced_value()

        player.set_played_jack(False)

        self.progress_turn(clear_messages)

    def handle_player_turn(self, player) -> None:
        while True:
            try:
                moves = self.get_player_input(player)

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
                
                hand = [player.hand[move] for move in moves]

                if not self.stack.is_valid_combo(hand):
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

    def handle_regular_turn(self, player: 'Player', moves, prev_player=None, next_player=None):
        if prev_player is None:
            prev_player = self.prev_player(player)
        if next_player is None:
            next_player = self.next_player(player)

        try:
            cards = [player.hand[move] for move in moves]
            self.stack.add_cards_on_top(player.remove_cards(moves),
                                        prev_player, next_player,
                                        self.players)
            self.add_opponent_status(player, cards)

        except KingOfSpadesException:
            self.add_opponent_status(player, cards)
            self.special_king_of_spades_interaction(prev_player)

        except AceException:
            self.add_opponent_status(player, cards)
            new_suit = self.get_player_ace_suit(player)
            self.stack.set_forced_suit(new_suit)

        except JackException:
            self.add_opponent_status(player, cards)
            new_value = self.get_player_jack_card(player)
            player.set_played_jack(True)
            self.stack.set_forced_value(new_value)
            for play in self.players:
                play.set_allowed_cards([new_value])
        if len(player.hand) == 0:
            self.get_winner(player)

    def handle_pass(self, player: 'Player'):
        card = self.deck.draw_card()
        player.add_card(card)

        if self.first_save(player, card):
            self.handle_regular_turn(player, [len(player.hand)-1])
            # self.stack.add_cards_on_top([card])
            # self.stack.trigger_top_effect(self.prev_player(player),
            #                               self.next_player(player),
            #                               self.players)
        if isinstance(player, Opponent):
            self.add_opponent_status(player, -1)

    def first_save(self, player: 'Player', card: 'Card'):
        # if player.status_effect == 
        if self.stack.is_valid_combo([card]):
            decision = self.get_player_first_save_input(player, card)
            if decision == 1:
                return True
        return False

    def get_player_first_save_input(self, player, card):
        if isinstance(player, MainPlayer):
            ans = input(f'You drew a {card}. Play it? (y/n): ')
            return 1 if ans == 'y' else 0
        else:
            return 1

    def handle_effect_turn(self, player: 'Player', moves):
        if len(moves) > 1 or moves[0] > len(player.hand):
            raise InvalidStatusTransferError

        if len(moves) == 1 and moves[0] == len(player.hand):
            if player.status_effect == Status.FORCESUIT:
                self.handle_pass(player)
            return

        card = player.hand[moves[0]]
        if card.value not in player.allowed_cards:
            if card.value != 11 or player.status_effect != Status.FORCESUIT:
                raise InvalidStatusTransferError

        prev_player = self.prev_player(player)
        next_player = self.next_player(player)

        if player.status_effect == Status.DRAW5:
            if card.suit in [Suits.CLUBS, Suits.DIAMONDS]:
                player.remove_status_effect()
            else:
                if self.stack.top_card.suit == Suits.SPADES:
                    player.transfer_effect(next_player)
                else:
                    player.transfer_effect(prev_player)
        else:
            player.transfer_effect(next_player)
        
        self.handle_regular_turn(player, moves, prev_player, next_player)
        # try:
        #     cards = [player.hand[move] for move in moves]
        #     if isinstance(player, Opponent):
        #         self.add_opponent_status(player, cards)
        #     self.stack.add_cards_on_top(player.remove_cards(moves),
        #                                 prev_player, next_player,
        #                                 self.players)
        # except JackException:
        #     new_value = self.get_player_jack_card(player)
        #     self.stack.set_forced_value(new_value)
        #     for play in self.players:
        #         play.set_allowed_cards([new_value])
        # except KingOfSpadesException:
        #     pass
        # if len(player.hand) == 0:
        #     self.get_winner(player)

    def get_player_input(self, player) -> List[int]:
        if isinstance(player, MainPlayer):
            sentence = self.ask_player_input(player)
            moves = [int(card) - 1 for card in input(sentence).split(' ')]
        else:
            moves = [player.get_optimal_card(self.stack)]
        return moves

    def ask_player_input(self, player):
        os.system('clear')

        additional_information = (self._main_player.special_message
                                  + self._main_player.error_message)
        if self._main_player.special_message != '':
            additional_information += '\n'

        special_message = ''
        if player.status_effect in [Status.NOEFFECT, Status.FORCESUIT]:
            special_message = ' and draw a card'

        first_part = str(self.stack) + '\n'
        second_part = player.get_hand_description()
        third_part = (f'{len(player.hand)+1} '
                      f'- Pass your turn{special_message}\n')
        fourth_part = 'Your option is: '

        sentence = (additional_information + first_part + second_part +
                    third_part + fourth_part)

        return sentence

    def add_opponent_status(self, opponent, cards) -> None:
        main_player = self._main_player
        if cards == -1:
            message = ''
            if opponent.allowed_cards == [] or 11 in opponent.allowed_cards:
                message = 'and draws a card '

            hand_size = len(opponent.hand)
            main_player.add_special_message(f'{opponent.name} passes '
                                            f'{message}'
                                            f'({hand_size} cards left)\n')
        else:
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

    def prepare_special_turn(self, playing):
        if playing.status_effect == Status.BLOCKED:
            message = ('' if playing.blocked_turns == 1
                       else f' for {playing.blocked_turns} turns')

            extra_message = ('You can play a 4 to transfer it to the next player\n' # NOQA
                             if playing.blocked_turns == playing.total_blocked_turns # NOQA
                             else '')

            block_message = (f'{playing.name} was blocked{message}\n'
                             if isinstance(playing, Opponent)
                             else (f'{Fore.RED}You have been blocked{message}!\n' # NOQA
                                   f'{extra_message}{Style.RESET_ALL}'))

            self.main_player.add_special_message(block_message)
            playing.set_allowed_cards([4])
        elif playing.status_effect == Status.DRAW2OR3:
            extra_message = 'You can play a 2 or a 3 to transfer it to the next player\n' # NOQA

            block_message = (f'{playing.name} is about to draw '
                             f'{playing.cards_to_draw} cards\n'
                             if isinstance(playing, Opponent)
                             else (f'{Fore.RED}You are about to draw '
                                   f'{playing.cards_to_draw} cards!\n'
                                   f'{extra_message}{Style.RESET_ALL}'))

            self.main_player.add_special_message(block_message)
            playing.set_allowed_cards([2, 3])
        elif playing.status_effect == Status.DRAW5:
            extra_message = 'You can play a King to either negate the effect or return it to sender\n' # NOQA

            block_message = (f'{playing.name} is about to draw '
                             f'{playing.cards_to_draw} cards\n'
                             if isinstance(playing, Opponent)
                             else (f'{Fore.RED}You are about to draw '
                                   f'{playing.cards_to_draw} cards!\n'
                                   f'{extra_message}{Style.RESET_ALL}'))

            self.main_player.add_special_message(block_message)
            playing.set_allowed_cards([13])

    def special_king_of_spades_interaction(self, player):
        self.prepare_special_turn(player)
        moves = self.get_player_input(player)
        self.handle_effect_turn(player, moves)
        if player.cards_to_draw > 0:
            self.main_player.add_special_message(f'{player} drew {player.cards_to_draw} cards') # NOQA
            for _ in range(player.cards_to_draw):
                player.add_card(self.deck.draw_card())
            self.main_player.add_special_message(f' (at {len(player.hand)} cards) \n') # NOQA
            player.remove_status_effect()
            print(self.ask_player_input(self.main_player))

    def get_player_ace_suit(self, player):
        suits = ['\u2660', '\u2666', '\u2663', '\u2665']
        if isinstance(player, MainPlayer):
            suits_string = ''
            for index, suit in enumerate(suits):
                color = Fore.BLACK if index % 2 == 0 else Fore.RED
                suits_string += (f'{index+1} - '
                                 f'{color + suit + Style.RESET_ALL}\n')
            suit = int(input((f'Pick a suit: \n{suits_string}')))
            return suit
        elif isinstance(player, Opponent):
            suit = player.get_optimal_suit()
            self.main_player.add_special_message(f'{Fore.RED}{player} has '
                                                 f'picked {suits[suit-1]} '
                                                 f'as the new suit{Style.RESET_ALL}\n') # NOQA
            return suit

    def get_player_jack_card(self, player):
        if isinstance(player, MainPlayer):
            value = int(input('Pick a value to force (from 5 to 10): '))
            return value
        elif isinstance(player, Opponent):
            value = player.get_optimal_value()
            self.main_player.add_special_message(f'{Fore.RED}{player} has picked {value} ' # NOQA
                                                 f'as the forced card{Style.RESET_ALL}\n') # NOQA
            return value

    def check_stack_forced_value(self):
        for player in self.players:
            if (player.status_effect == Status.FORCESUIT and not player.won):
                return
        self.stack.reset_forced_value()

    def get_winner(self, player: 'Player'):
        player.win_game()
        if player not in self.winners:
            self._winners.append(player)

    def finish_game(self):
        os.system('clear')
        self.main_player.clear_error_message()
        self.main_player.clear_special_message()
        ends = ['st', 'nd', 'rd', 'th']
        print('The game is finished!\n')
        for place, player in enumerate(self.winners):
            print(f'{place+1}{ends[place]} place - {player}')

        for player in self.players:
            if player not in self.winners:
                print(f'{player} lost :( \n')

        return
