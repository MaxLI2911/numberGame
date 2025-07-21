import pytest
from numbers_game import check_input_num, enter_number, best_player, find_player, points
from player import Player
import json
from serialization import read_from_json, write_to_json



@pytest.mark.parametrize("input_value, expected", [
    ("10", 10),
    ("0", 0),
    ("-5", None),
    ("abc", None),
    ("5.5", None),
])
def test_check_input_num(input_value, expected):
    assert check_input_num(input_value) == expected


def test_enter_number(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "15")
    assert enter_number() == 15


def test_points():
    assert points(100, 1) == 101
    assert points(100, 5) > 0
    assert points(100, 10) == 0


def test_find_player():
    players = [
        Player(1, "Alice", 5, 10, 50),
        Player(2, "Bob", 3, 5, 30)
    ]
    assert find_player(players, "1", "Alice") == players[0]
    assert find_player(players, "2", "Bob") == players[1]
    assert find_player(players, "3", "Charlie") is None
    assert find_player(players, "abc", "Alice") is None


def test_read_from_json(tmp_path):
    test_file = tmp_path / "test.json"
    data = [
        {"id": 1, "name": "Alice", "num_of_games": 5, "average": 10, "max_points": 50, "points_per_day": {}}
        ]
    test_file.write_text(json.dumps(data))
    players = read_from_json(str(test_file))
    assert len(players) == 1
    assert players[0].name == "Alice"


def test_write_to_json(tmp_path):
    test_file = tmp_path / "players.json"
    players = [Player(1, "Alice", 5, 10, 50)]
    write_to_json(str(test_file).replace(".json", ""), players)
    with open(test_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert len(data) == 1
    assert data[0]["name"] == "Alice"


def test_best_player():
    player1 = Player(1, "m", 1, 10, 10)
    player2 = Player(2, "q", 3, 5, 5)
    player3 = Player(3, "t", 5, 2, 9)
    data = [player1, player2, player3]
    best_max, player_place_at_max = best_player(player1, data, "max_points")
    assert best_max == 10 and player_place_at_max == 1
