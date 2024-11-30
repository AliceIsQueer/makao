from game import Game


while True:
    try:
        choice = int(input('1 - Display the rules\n2 - Start the game\n'))
        if choice == 1:
            print('aklsjdakljd')
        elif choice == 2:
            game = Game('Alice', 2)
        else:
            print('This it not a valid option')
    except ValueError:
        print('This is not a valid option')
