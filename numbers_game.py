from random import randint
from serialization import read_from_json, write_to_json
from player import Player
from graphics import plot_player_achievements, plot_points_per_day
import datetime


def main():
    data = read_from_json("lab1/players.json")
    if data is None:
        exit()
    print("Hi, this game is guess the number.")
    while True:
        print(
            "Are you a new player?"
        )
        answer = input("Y/N\n").strip().lower()
        if answer == "n":
            name = input("Enter your name\n")
            id = input("Enter your id\n")
            player = find_player(data, id, name)
            if player is None:
                print("There is no such player in the database")
            else:
                break
        else:
            print("We are happy to welcome a new player")
            name = input("Enter your name\n")
            id = len(data)+1
            player = Player(id, name, 0, 0, 0)
            data.append(player)
            print(f"Your id is {player.id}, remember it")
            break
    play = True
    while play is True:
        number, limit = start()
        play = playing(number, limit, player)
        print("\nYour statistics:")
        print(player.statistics())
        players_statistick(player, data)
    make_graph(data, player)
    write_to_json("players", data)
    print("\nThanks for playing")


def start():
    while True:
        limit = check_input_num(input(
            "Enter the upper limit of numbers.\n"
            "The game involves numbers from 0 to.."
            ))
        if limit == 0:
            print("Try another limit")
        elif limit:
            break
    return randint(0, limit), limit


def enter_number():
    while True:
        number = check_input_num(input("Enter the number\n"))
        if number is not None:
            break
    return number


def playing(number, limit, player: Player):
    current_date = datetime.date.today().isoformat()
    num_of_try = 1
    while True:
        user_num = enter_number()
        if user_num == number:
            point = points(limit, num_of_try)
            player.new_average(point)
            player.num_of_games += 1
            player.new_max_points(point)
            player.add_or_update_points_date(current_date, point)
            print(f"You guessed right on the {num_of_try}th try.")
            if point == 0:
                print("Too many guesses.\nYou lose")
            else:
                print("Amazing!\nYou are a winner!")
            print(f"You get {point} points")
            print("Do you want to continue the game?")
            answer = input("Y/N\n").strip().lower()
            if answer == "y":
                return True
            elif answer == "n":
                return False
            else:
                print('This is interpreted as no')
                return False
        elif user_num > number:
            num_of_try += 1
            print("Try a lower number")
        elif user_num < number:
            num_of_try += 1
            print("Try a greater number")


def check_input_num(number):
    try:
        number = int(number)
        if number < 0:
            print("The number must be positive.")
            return None
        else:
            return number
    except ValueError:
        print('This is not an integer number')
        return None


def points(limit, num_of_try):
    point = (1/(2**(num_of_try-1)/(limit+1)))
    if point > 1:
        return point
    else:
        return 0


def find_player(players: list, player_id: int = None, name: str = None):
    try:
        player_id = int(player_id)
    except Exception:
        return None
    for player in players:
        if (player.id == player_id) and (player.name == name):
            return player
    return None


def players_statistick(player: Player, data: list):
    print_statistick("points", best_player(player, data, "max_points"))
    print_statistick("average", best_player(player, data, "average"))
    print_statistick(
        "number of games", best_player(player, data, "num_of_games"))


def best_player(player: Player, data: list, attr_name):
    max_points = []
    for gamer in data:
        max_points.append(getattr(gamer, attr_name))
    max_points.sort(reverse=True)
    return max_points[0], max_points.index(getattr(player, attr_name))+1


def print_statistick(kind: str, data: list):
    print(f"\nMaximum of {kind} received among players: {data[0]}")
    print(f"Your place is {data[1]}")
    if data[1] == 1:
        print("Congratulations, you are the best!")


def make_graph(data, player: Player):
    while True:
        print("\nPerhaps you would like to see a graph?")
        print("press:")
        print("1 - graph of max points")
        print("2 - graph of average")
        print("3 - graph of number of games")
        print("4 - graph of points per day")
        print("another key - if you don't want")
        answer = input().strip()
        if answer == "1":
            plot_player_achievements(data, "max_points")
        elif answer == "2":
            plot_player_achievements(data, "average")
        elif answer == "3":
            plot_player_achievements(data, "num_of_games")
        elif answer == "4":
            if_plot_points_per_day(player.points_per_day)
        else:
            break


def if_plot_points_per_day(data: dict):
    current_date = datetime.date.today().isoformat()
    while True:
        number = check_input_num(input(
            "Enter the number of days for which you want to see the graph\n"
            ))
        if number is not None:
            break
    plot_points_per_day(data, number, current_date)


if __name__ == "__main__":
    main()
