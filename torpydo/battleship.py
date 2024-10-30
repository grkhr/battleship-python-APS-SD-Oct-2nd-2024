import random
import os
import colorama
import platform
import pickle
import json

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
                    888             888   888   888                888     d8b         
                    888             888   888   888                888     Y8P         
                    888             888   888   888                888                 
                    88888b.  8888b. 888888888888888 .d88b. .d8888b 88888b. 88888888b.  
                    888 "88b    "88b888   888   888d8P  Y8b88K     888 "88b888888 "88b 
                    888  888.d888888888   888   88888888888"Y8888b.888  888888888  888 
                    888 d88P888  888Y88b. Y88b. 888Y8b.         X88888  888888888 d88P 
                    88888P" "Y888888 "Y888 "Y888888 "Y8888  88888P'888  88888888888P"  
                                                                            888      
                                                                            888      
                                                                            888      
""" + Style.RESET_ALL)

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
                  ~.
           Ya...___|__..aab     .   .
            Y88a  Y88o  Y88a   (     )
             Y88b  Y88b  Y88b   `.oo'
             :888  :888  :888  ( (`-'
    .---.    d88P  d88P  d88P   `.`.
   / .-._)  d8P'"""|"""'-Y8P      `.`.
  ( (`._) .-.  .-. |.-.  .-.  .-.   ) )
   \ `---( O )( O )( O )( O )( O )-' /
    `.    `-'  `-'  `-'  `-'  `-'  .' CJ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ''' + Style.RESET_ALL)

    n = 1
    while True:
        print('----- Round', n, '------')
        print("Player, it's your turn")
        position = parse_position(
            input(Fore.WHITE+"Enter coordinates for your shot :"))
        if position is None:
            print(Fore.RED + "Invalid input. Please try again")
            continue

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
                print("Still alive: ", e.name, "HP:", e.hp)

        print(Fore.GREEN + "Yeah ! Nice hit ! " + ship.name +
              Style.RESET_ALL if is_hit else Fore.YELLOW + "Miss" + Style.RESET_ALL)

        # TelemetryClient.trackEvent('Player_ShootPosition', {'custom_dimensions': {
        #                            'Position': str(position), 'IsHit': is_hit}})

        position = get_random_position()
        is_hit = GameController.check_is_hit(myFleet, position)
        print('---')
        print(
            f"Computer shoot in {str(position)} and {Fore.RED + 'hit your ship!' if is_hit else Fore.GREEN + 'miss'}" + Style.RESET_ALL)
        # TelemetryClient.trackEvent('Computer_ShootPosition', {'custom_dimensions': {
        #                            'Position': str(position), 'IsHit': is_hit}})
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
            print(Fore.GREEN+"All enemies ships were destroyed! You win!")
            print(Fore.GREEN+r''' 
                   _..--""---.
          /           ".
          `            l
          |'._  ,._ l/"\
          |  _J<__/.v._/
           \( ,~._,,,,-)
            `-\' \`,,j|
               \_,____J
          .--.__)--(__.--.
         /  `-----..--'. j
         '.- '`--` `--' \\
        //  '`---'`  `-' \\
       //   '`----'`.-.-' \\
     _//     `--- -'   \' | \________
    |  |         ) (      `.__.---- -'\
     \7          \`-(               74\\\
     ||       _  /`-(               l|//7__
     |l    ('  `-)-/_.--.          f''` -.-"|
     |\     l\_  `-'    .'         |     |  |
     llJ   _ _)J--._.-('           |     |  l
     |||( ( '_)_  .l   ". _    ..__I     |  L
     ^\\\||`'   "   '"-. " )''`'---'     L.-'`-.._
          \ |           ) /.              ``'`-.._``-.
          l l          / / |                      |''|
           " \        / /   "-..__                |  |
           | |       / /          1       ,- t-...J_.'
           | |      / /           |       |  |
           J  \  /"  (            l       |  |
           | ().'`-()/            |       |  |
          _.-"_.____/             l       l.-l
      _.-"_.+"|                  /        \.  \
/"\.-"_.-"  | |                 /          \   \
\_   "      | |                1            | `'|
  |ll       | |                |            i   |
  \\\       |-\               \j ..          L,,'. `/
 __\\\     ( .-\           .--'    ``--../..'      '-..''' + Style.RESET_ALL)
            return

        killed = 0
        for f in myFleet:
            if f.hp <= 0:
                killed += 1
                continue

        if killed == len(myFleet):
            print(Fore.RED+"All your ships were destroyed. You lose")
            print(Fore.RED+r'''    _,_
  /7/Y/^\
  vuVV|C)|                        __ _
    \|^ /                       .'  Y '>,
    )| \)                      / _   _   \
   //)|\\                      )(_) (_)(|}
  / ^| \ \                     {  4A   } /
 //^| || \\                     \uLuJJ/\l
>//||| |\\\|                    |3    p)/
| """""  7/>l__ _____ ____      /nnm_n//
L>_   _-< 7/|_-__,__-)\,__)(".  \_>-<_/D
)D" Y "c)  9)       //V     \_"-._.__G G_c__.-__<"/ ( \
 | | |  |(|               < "-._"> _.G_.___)\   \7\
  \"=" // |              (,"-.__.|\ \<.__.-" )   \ \
   '---'  |              |,"-.__"| \!"-.__.-".\   \ \
     |_;._/              (_"-.__"'\ \"-.__.-".|    \_\
     )(" V                \"-.__"'|\ \-.__.-".)     \ \
        (                  "-.__'"\_\ \.__.-"./      \ l
         )                  ".__"">>G\ \__.-">        V )
                                ""  G<\ \_.-"        ./7
                                     G<\ \          ///
                                ___  GD'
                           /  /             )E_>"
                         _/  (             |  \()
                        / \ /              |  |
                        /\\|               |  |
                       / '((               |  |
                      /  / )\              \  |
                     /  y  \y              |Y |
                    /  /    (              |  |
                   L ."     |              |  /
                  | \(                     |  |
                   \_|                     |  |
                   |  \                    { "|
                   | ||                    |  |
                   |x||                    \_,/
                   } ||                    / \'
                   | ||                    |_/
                   | (|                    | }\
                   | ||                    } ||
                   | ||                    | ||
                   | ||                    |\||
                   / ||                    | ||
                   | ||                    ( |!
                   | |/                    ) ||
                 _/   \                    | }|
             _.-"_ ( )|   jjs              ! ||
          c_"-_-"_    )                    | ||
           c,-_-'_--""                     { ||
           "C(_/"                          \ /|
                                           (! )
                                           /| \
                                          /  |(
                                         /7||\\
                                        ()U cUu"''')
            return

        n += 1


def parse_position(input: str):
    if len(input) == 0:
        return None

    try:
        letter = Letter[input.upper()[:1]]
        number = int(input[1:])
    except:
        return None
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

    used_position = []
    for ship in myFleet:
        print()
        print(
            f"Please enter the positions for the {ship.name} (size: {ship.size})")

        for i in range(ship.size):
            while True:
                position_input = input(
                    Fore.WHITE+f"Enter position {i+1} of {ship.size} (i.e A3):")
                if len(position_input) == 0:
                    print(Fore.RED+"Invalid position. Please type valid one")
                    continue
                if position_input in used_position:
                    print(
                        Fore.RED+"The position is already used. Please type another position")
                    continue
                if ship.add_position(position_input) == -1:
                    print(Fore.RED+"Invalid position. Please type valid one")
                    continue
                used_position.append(position_input)
                # TelemetryClient.trackEvent('Player_PlaceShipPosition', {'custom_dimensions': {
                #     'Position': position_input, 'Ship': ship.name, 'PositionInShip': i}})
                break


def save_list(my_list, filename):
    """Save a list to a file using pickle."""
    with open(filename, 'w') as f:
        json.dump(my_list, f)


def load_list(filename):
    """Load a list from a file using pickle."""
    with open(filename, 'r') as f:
        return json.load(f)


def initialize_enemyFleet():
    global enemyFleet

    enemyFleet = GameController.initialize_ships()
    # randomize_ef_positions()
    closed_position = {}
    # for s in myFleet:
    #     for p in s.positions:
    #         val = closed_position.get(p.column.name)
    #         if val is None:
    #             val = []
    #             closed_position[p.column.name] = val

    #         val.append(p.row)

    positions = [Letter.A, Letter.B, Letter.C, Letter.D,
                 Letter.E, Letter.F, Letter.G, Letter.H]

    set_ships = []
    i = len(enemyFleet) - 1
    while i >= 0:
        curr_ship = enemyFleet[i]
        letter = positions[random.randint(1, len(positions))-1]
        closed_rows = closed_position.get(letter)
        if closed_rows is None:
            closed_rows = []
            closed_position[letter] = closed_rows

        is_set = False
        while True:
            cell = random.randint(1, 8-curr_ship.size)
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

    b = [[]]
    for e in set_ships:
        for p in e.positions:
            b.append([p.column.name, p.row])

    save_list(b, "enemy.json")
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
