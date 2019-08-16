import numpy
import random
game_player = [[" " for x in range(11)] for x1 in range(9)]
game_computer = [[" " for y in range(11)] for y1 in range(9)]
game_player_2 = [[" " for z in range(11)] for z1 in range(9)]
ship_type, ship_type_c, Indicator, Indicator_c, statement = "", "", "", "", ""  # Setting global variables
Victory, allow_ship = True, True  # Setting global variables
shots = []
Checking_computer_hit = False
types_1 = ["C", "B", "S", "c", "D"]
types_2 = ["C", "B", "S", "c", "D"]  # Setting global variables
print("\n"+" "*20+"Welcome to the classical Battleship game\n")
rules = " "*34+"GAME RULES:\nYour placed ships are on the left screen where it says PLAYER. The other board on the right is your display.\n" \
               "When placing your ships type where you want to place when e.g. A1 A2 A3 A4 A5\n" \
               "Each ships is different length and the length is told by the number of hole e.g. 5 holes\n" \
               "If you need want you can type [rules] when taking a shot to show the game rules\n" \
               "\nOn the board these are the legends:\n" \
               "X - There's a ship or your ship has been shot\n" \
               "· - You or computer missed\n" \
               "C - Carrier ship (5 holes)\n" \
               "B - Battleship (4 holes)\n" \
               "S - Submarine (3 holes)\n" \
               "c - Cruiser (3 holes)\n" \
               "D - Destroyer (2 holes)\n"
print(rules)
input(" "*28+"Press ENTER to play\n")


def draw_board():
    for _ in range(30):
        print("\n")
    print("\n"+" "*12+"PLAYER"+" "*37+"COMPUTER")
    print(" "*6+"|A|B|C|D|E|F|G|H|I|J|K|"+" "*22+"|A|B|C|D|E|F|G|H|I|J|K|")
    for x in range(9):
        print(" "*5+(" "+"-"*23)+" "*22+("-"*23))
        print(" "*5+str(x+1)+("|" + "|".join(game_player[x]) + "|")+" "*21+str(x+1)+("|" + "|".join(game_player_2[x]) + "|"))
    print(" "*5+(" "+"-"*23)+" "*22+("-"*23)+"\n")


def check_placing(n, l, board):
    global allow_ship
    if board == game_player:
        n = [a-1 for a in n]
        l = [a-1 for a in l]
    for x, y_1 in zip(n, l):  # Checks if you can place a ship there (There's no ship in that place and ship can't be close to another ship)
        try:
            if board[x][y_1] == board[x+1][y_1] == board[abs(x-1)][y_1] == board[x][y_1+1] == board[x][abs(y_1-1)] == " ":  # UGLY CODE NEEDS FIXING
                allow_ship = True
            else:
                allow_ship = False
                break
        except IndexError:
            try:
                if board[x][y_1+1] == board[abs(x-1)][y_1] == board[x][abs(y_1-1)] == " ":  # UGLY CODE NEEDS FIXING
                    allow_ship = True
                else:
                    allow_ship = False
                    break
            except IndexError:
                try:
                    if board[x][abs(y_1-1)] == board[abs(x-1)][y_1] == " ":  # UGLY CODE NEEDS FIXING
                        allow_ship = True
                    else:
                        allow_ship = False
                        break
                except IndexError:
                    print("NOPE 7")
    return allow_ship


def place_ship(size):
    global ship_type
    placing_ship = True
    while placing_ship:
        if size == 5:
            ship = input("Say where you want to put your 'Carrier'(5 holes): ")
            ship_type = "C"
        elif size == 4:
            ship = input("Say where you want to put your 'Battleship'(4 holes): ")
            ship_type = "B"
        elif size == 3.5:
            ship = input("Say where you want to put your 'Cruiser'(3 holes): ")
            ship_type = "c"
        elif size == 3:
            ship = input("Say where you want to put your 'Submarine'(3 holes): ")
            ship_type = "S"
        elif size == 2:
            ship = input("Say where you want to put your 'Destroyer'(2 holes): ")
            ship_type = "D"
        ship_a = ["".join(x) for x in ship]
        if ord(ship_a[0]) > 107 or ord(ship_a[len(ship_a)-2]) > 107:  # Checks if the letter is valid
            print("Choose a letter between A and K")
            continue
        ship_b = iter(ship_a)
        letters = []
        numbers = []
        for x in ship_a:  # Recycles numbers and letters
            if ord(x.lower()) > 57:
                letters.append(ord(x.lower()) - 96)
            elif ord(x.lower()) >= 49:
                numbers.append(int(x))
        if len(numbers) != int(size):  # Checks if size of the ship is correct
            print("Ship to small/big")
            continue
        numbers_n = [abs(x) for x in numpy.diff(numbers)]  # Makes negative numbers to positive in difference between numbers
        letters_n = [abs(x) for x in numpy.diff(letters)]
        check_placing(numbers, letters, game_player)
        for z in ship_b:
            if z == " ":  # Makes sure empty string doesn't go to a loop
                continue
            elif letters[1:] == letters[:-1] or numbers[1:] == numbers[:-1]:  # Check if the column or row is the same (Same letter or number)
                # Checks if the differences between the numbers or letters is 1 or -1
                if numbers_n[1:] == numbers_n[:-1] == [1 for _ in range(len(numbers_n)-1)] or letters_n[1:] == letters_n[:-1] == [1 for _ in range(len(letters_n)-1)]:
                    if allow_ship:  # Checks if no ship placed
                        game_player[int(next(ship_b))-1][ord(z.lower()) - 97] = ship_type
                    else:
                        print("Ship is already there")
                        break
                    placing_ship = False
                else:
                    print("Choose a number between 1 and 9")
                    break
            else:
                print("Nope")
                break


def computer_ship(size):
    global ship_type_c
    placing_ship = True
    if size == 5:
        ship_type_c = "C"
    elif size == 4:
        ship_type_c = "B"
    elif size == 3.5:
        ship_type_c = "c"
    elif size == 3:
        ship_type_c = "S"
    elif size == 2:
        ship_type_c = "D"
    while placing_ship:
        if random.randint(1, 2) % 2 == 0:  # Randomizes if a ship is horizontal or vertical
            x = random.randint(0, 11 - int(size))  # Makes sure that the ship won't be out of range of a list
            y = random.randint(0, 8)
            letters = list(range(x, x+int(size)))
            numbers = [random.randint(y, y) for _ in range(int(size))]  # Randomizes a number and puts it in a list for a size of a ship
            row = numbers[0]
            check_placing(numbers, letters, game_computer)
            for z in letters:
                if allow_ship:
                    game_computer[row][z] = ship_type_c
                    placing_ship = False
                else:
                    break  # If the ship can't be there it goes back to line 144(Vertical or horizontal) and randomizes again
        else:  # If a ship is vertical
            x = random.randint(0, 9 - int(size))
            y = random.randint(0, 10)
            numbers = list(range(x, x + int(size)))
            letters = [random.randint(y, y) for _ in range(int(size))]
            check_placing(numbers, letters, game_computer)
            column = letters[0]
            for z in numbers:
                if allow_ship:
                    game_computer[z][column] = ship_type_c
                    placing_ship = False
                else:
                    break


def check_winner(board):
    global Victory, types_1, types_2, statement
    statement = ""
    a = 0
    ships = []
    for x in board:
        for y in x:
            if y in ("C", "c", "B", "S", "D"):  # y in ("C", "c", "B", "S", "D")
                a += 1
                ships.append(y)
    if board == game_computer:
        types = types_1
    else:
        types = types_2
    for x in types:
        if x not in ships:
            statement = "\n"+" "*38+"Ship destroyed"  # Checks if the ship is destroyed
            types.remove(x)
    if a == 0:  # Checks if there are no ships in a list(board)
        Victory = False
    return Victory, statement


def player_shoot():
    global Indicator, Indicator_c, Checking_computer_hit, rules, ship_destroyed
    playing = True
    same_shot = False
    while playing:
        check_winner(game_computer)
        if not Victory:
            draw_board()
            print("Game over\nPlayer wins")
            input("Press any key to close")
            break
        if Indicator == " "*40+"It's a hit!" and not same_shot:  # Checks if the player hits and prints only hit if player hits
            print(Indicator, statement)  # Prints how the shot went
        elif Checking_computer_hit and not same_shot:
            if not ship_destroyed:
                print(Indicator, "\n"+" "*39+"Computer HITS\n")
            else:
                print(Indicator, "\n"+" "*39+"Computer HITS\n", " "*38+"Ship destroyed")
        elif not same_shot:
            print(Indicator, Indicator_c, statement)
        shot = list(input("Say where you want to shoot: "))  # ________________
        if "".join(shot).lower() == "rules":  # Prints the rules of the game again (Maybe put a hint)
            print(rules)
            continue
        elif "".join(shot).lower() == "exit":
            print("Thanks for playing")
            input("Press any key to close")
            break
        shot_a = [x for x in shot if x != " "]  # Makes sure empty string doesn't go to a shot (A 5 makes A5)
        shot_b = iter(shot_a)
        if len(shot_a) != 2:  # Checks if the shot is valid
            print("Invalid shot")
        elif ord(shot_a[0]) > 96 and ord(shot_a[1]) > 96:
            print("Two letters")
        elif ord(shot_a[0]) < 96 and ord(shot_a[1]) < 96:
            print("Two numbers")
        elif (ord(shot_a[0]) or shot_a[1]) > 107:
            print("Say a letter between 'A' and 'K'")
        else:
            for boom in shot_b:
                if ord(boom) >= 97:
                    column = ord(boom.lower()) - 97
                    row = int(next(shot_b))
                    if game_player_2[row-1][column] != " ":
                        print("You've already shot there")
                        same_shot = True
                        break
                    elif game_computer[row-1][column] != " ":
                        game_computer[row-1][column] = " "
                        game_player_2[row-1][column] = "X"
                        Indicator = " "*40+"It's a hit!"
                        draw_board()
                    else:
                        game_player_2[row-1][column] = "+"  # Using this [•] in www.repl.it but here the board gets curvy
                        playing = False
                        Indicator = " "*41+"You missed"
                        computer_shoot()
                else:
                    print("Please put letter first, then a number")
                    break


def computer_shoot():
    global shots, Victory, Indicator_c, Checking_computer_hit, ship_destroyed
    ship_destroyed = False
    Checking_computer_hit = False
    shooting = True
    while shooting:
        row = random.randint(0, 8)  # 0, 8  Randomizes a shot
        column = random.randint(0, 10)  # 0, 10
        shot = "".join(str(row) + str(column))
        if shot not in shots:  # Checks if the shot is not already taken
            shots.append(shot)
            if Indicator_c == "\n"+" "*38+"Computer hits\n":
                Checking_computer_hit = True

            check_winner(game_player)
            if not Victory:
                draw_board()
                print("Game over\nComputer wins")
                input("Press any key to close")
                break
            elif game_player[row][column] != " ":
                game_player[row][column] = "X"
                Indicator_c = "\n"+" "*38+"Computer hits\n"
            else:
                Indicator_c = "\n"+" "*38+"Computer misses\n"
                game_player[row][column] = "+"  # Indicating there it was shot
                shooting = False
                if statement == "\n"+" "*38+"Ship destroyed":
                    ship_destroyed = True
                draw_board()
                player_shoot()


if __name__ == "__main__":
    draw_board()
    for y in [5, 4, 3.5, 3, 2]:
        computer_ship(y)

    for x in [5, 4, 3.5, 3, 2]:  # [5, 4, 3.5, 3, 2]
        place_ship(x)
        draw_board()

    player_shoot()