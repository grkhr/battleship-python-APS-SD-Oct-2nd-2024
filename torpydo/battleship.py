import random
import os
import colorama
import platform

from colorama import Fore, Back, Style
from torpydo.ship import Color, Letter, Position, Ship
from torpydo.game_controller import GameController
from torpydo.telemetryclient import TelemetryClient

print("Starting")

myFleet = []
enemyFleet = []


def main():
    TelemetryClient.init()
    TelemetryClient.trackEvent('ApplicationStarted', {
                               'custom_dimensions': {'Technology': 'Python'}})
    colorama.init()
    print(Fore.YELLOW + r"""
                                    |__
                                    |\/
                                    ---
                                    / | [
                             !      | |||
                           _/|     _/|-++'
                       +  +--|    |--|--|_ |-
                     { /|__|  |/\__|  |--- |||__/
                    +---------------___[}-_===_.'____                 /\
                ____`-' ||___-{]_| _[}-  |     |_[___\==--            \/   _
 __..._____--==/___]_|__|_____________________________[___\==--____,------' .7
|                        Welcome to Battleship                         BB-61/
 \_________________________________________________________________________|""" + Style.RESET_ALL)

    initialize_game()

    start_game()


def start_game():
    global myFleet, enemyFleet
    # clear the screen
    if (platform.system().lower() == "windows"):
        cmd = 'cls'
    else:
        cmd = 'clear'
    os.system(cmd)
    print(Fore.CYAN + r'''
                  __
                 /  \
           .-.  |    |
   *    _.-'  \  \__/
    \.-'       \
   /          _/
   |      _  /
   |     /_\
    \    \_/
     """"""""''' + Style.RESET_ALL)

    n = 1
    while True:
        print('----- Round', n, '------')
        print("Player, it's your turn")
        position = parse_position(input("Enter coordinates for your shot :"))
        if not position_valid(position):
            print(
                Fore.RED + f"!!! Invalid position {position.column.name}{position.row}, try again\n" + Style.RESET_ALL)
            continue
        is_hit, ship = GameController.check_is_hit(enemyFleet, position)
        if is_hit:
            print(Fore.GREEN + r'''
                \          .  ./
              \   .:"";'.:..""   /
                 (M^^.^~~:.'"").
            -   (/  .    . . \ \)  -
               ((| :. ~ ^  :. .|))
            -   (\- |  \ /  |  /)  -
                 -\  \     /  /-
                   \  \   /  /''' + Style.RESET_ALL)

        for e in enemyFleet:
            if e.hp == 0:
                print("You killed: ", e.name, e.positions)

            else:
                print("Still alive: ", e.name)

        print(Fore.GREEN + "Yeah ! Nice hit ! " + ship.name +
              Style.RESET_ALL if is_hit else Fore.YELLOW + "Miss" + Style.RESET_ALL)

        TelemetryClient.trackEvent('Player_ShootPosition', {'custom_dimensions': {
                                   'Position': str(position), 'IsHit': is_hit}})

        position = get_random_position()
        is_hit = GameController.check_is_hit(myFleet, position)
        print('---')
        print(
            f"Computer shoot in {str(position)} and {Fore.RED + 'hit your ship!' if is_hit else Fore.GREEN + 'miss'}" + Style.RESET_ALL)
        TelemetryClient.trackEvent('Computer_ShootPosition', {'custom_dimensions': {
                                   'Position': str(position), 'IsHit': is_hit}})
        if is_hit:
            print(Fore.RED + r'''
                \          .  ./
              \   .:"";'.:..""   /
                 (M^^.^~~:.'"").
            -   (/  .    . . \ \)  -
               ((| :. ~ ^  :. .|))
            -   (\- |  \ /  |  /)  -
                 -\  \     /  /-
                   \  \   /  /''' + Style.RESET_ALL)
        print('\n')

        killed = 0
        for f in enemyFleet:
            if f.hp <= 0:
                killed += 1
                continue
        print("killed:", killed)
        if killed == len(enemyFleet):
            print("All enemies ships were destroyed! You win!")
            return

        killed = 0
        for f in myFleet:
            if f.hp <= 0:
                killed += 1
                continue

        if killed == len(myFleet):
            print("All your ships were destroyed. You lose")
            return

        n += 1


def parse_position(input: str):
    letter = Letter[input.upper()[:1]]
    number = int(input[1:])
    position = Position(letter, number)

    return Position(letter, number)


def position_valid(obj: Position):
    return obj.column in Letter and obj.row >= 1 and obj.row <= 8


def get_random_position():
    rows = 8
    lines = 8

    letter = Letter(random.randint(1, lines))
    number = random.randint(1, rows)
    position = Position(letter, number)

    return position


def initialize_game():
    initialize_myFleet()

    initialize_enemyFleet()


def initialize_myFleet():
    global myFleet

    myFleet = GameController.initialize_ships()

    print("Please position your fleet (Game board has size from A to H and 1 to 8) :")

    for ship in myFleet:
        print()
        print(
            f"Please enter the positions for the {ship.name} (size: {ship.size})")

        for i in range(ship.size):
            position_input = input(
                f"Enter position {i+1} of {ship.size} (i.e A3):")
            ship.add_position(position_input)
            TelemetryClient.trackEvent('Player_PlaceShipPosition', {'custom_dimensions': {
                                       'Position': position_input, 'Ship': ship.name, 'PositionInShip': i}})
            

# def randomize_ef_positions():

def initialize_enemyFleet():
    global enemyFleet
    
    enemyFleet = GameController.initialize_ships()
    # randomize_ef_positions()
    closed_position = {}
    for s in myFleet:
        for p in s.positions:
            val = closed_position.get(p.column.name)
            if val is None:
                val = []
                closed_position[p.column.name] = val

            val.append(p.row)

    positions = [Letter.A, Letter.B, Letter.C, Letter.D,
                 Letter.E, Letter.F, Letter.G, Letter.H]

    set_ships = []
    i = len(enemyFleet) - 1
    print("enemy shils:", enemyFleet)
    print("len", len(enemyFleet))
    while i >= 0:
        print("curr index:", i)
        curr_ship = enemyFleet[i]
        letter = positions[random.randint(1, len(positions))-1]
        closed_rows = closed_position.get(letter)
        if closed_rows is None:
            closed_rows = []
            closed_position[letter] = closed_rows

        is_set = False
        while True:
            cell = random.randint(1, 8)
            end_cell = cell + curr_ship.size
            if (cell not in closed_rows) and (end_cell not in closed_rows):
                for k in range(cell, end_cell):
                    curr_ship.positions.append(Position(letter, k))
                    closed_rows.append(k)
                set_ships.append(curr_ship)
                is_set = True
                break
        if is_set:
            i -= 1
    
    enemyFleet = set_ships

    # enemyFleet[0].positions.append(Position(Letter.B, 4))
    # enemyFleet[0].positions.append(Position(Letter.B, 5))
    # enemyFleet[0].positions.append(Position(Letter.B, 6))
    # enemyFleet[0].positions.append(Position(Letter.B, 7))
    # enemyFleet[0].positions.append(Position(Letter.B, 8))

    # enemyFleet[1].positions.append(Position(Letter.E, 6))
    # enemyFleet[1].positions.append(Position(Letter.E, 7))
    # enemyFleet[1].positions.append(Position(Letter.E, 8))
    # enemyFleet[1].positions.append(Position(Letter.E, 9))

    # enemyFleet[2].positions.append(Position(Letter.A, 3))
    # enemyFleet[2].positions.append(Position(Letter.B, 3))
    # enemyFleet[2].positions.append(Position(Letter.C, 3))

    # enemyFleet[3].positions.append(Position(Letter.F, 8))
    # enemyFleet[3].positions.append(Position(Letter.G, 8))
    # enemyFleet[3].positions.append(Position(Letter.H, 8))

    # enemyFleet[4].positions.append(Position(Letter.C, 5))
    # enemyFleet[4].positions.append(Position(Letter.C, 6))



if __name__ == '__main__':
    main()
