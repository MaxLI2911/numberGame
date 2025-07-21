import json
from player import Player


def read_from_json(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
        gamers = []
        for obj in data:
            player = Player(
                id=obj["id"],
                name=obj["name"],
                num_of_games=obj["num_of_games"],
                average=obj["average"],
                max_points=obj["max_points"],
                points_per_day=obj["points_per_day"]
            )
            gamers.append(player)

        return gamers
    except json.JSONDecodeError:
        print("The file must have a JSON extension and JSON structure")
        return None
    except FileNotFoundError or FileExistsError:
        print(f"File {file_name} not found.")
        return None
    except PermissionError:
        print(f"No permission to read '{file_name}'.")
        return None


def write_to_json(file_name, players):

    if not file_name:
        file_name = "players"

    data = [player.to_dict() for player in players]

    try:
        with open(f"{file_name}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except IsADirectoryError:
        print(f"{file_name} is a directory.")
    except PermissionError:
        print(f"No permission to write to '{file_name}'.")
