from game import Game, InvalidOppNumError


if __name__ == '__main__':
    choice = -1
    while choice != 3:
        try:
            choice = int(input('1 - Display the rules\n2 - Start the game\n3 - Exit\n'))
            if choice == 1:
                print(
                        'You play according to the rules of makao.\n'
                        'To play a card, simply type its index when prompted\n'
                        'To play multiple cards write them separated with spaces\n'
                        'When you want to say makao simply end your sequence with MAKAO\n'
                        'If you want to say stop makao end your sequence with STOP\n'
                        'For any further questions you can check the wikipedia page of makao\n'
                    )
            elif choice == 2:
                name = input('What is your name? ')
                player_num = int(input('Input the number of opponents (1-3): '))
                game = Game(name, player_num)
            elif choice != 3:
                print('This it not a valid option\n')
        except ValueError:
            print('This is not a valid option\n')
        except InvalidOppNumError:
            print('The number has to be between 1 and 3\n')
