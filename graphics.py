import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def plot_player_achievements(players, attr_name):
    players = sorted(
        players, key=lambda p: getattr(p, attr_name), reverse=True)
    names = [player.name for player in players]
    values = [getattr(player, attr_name) for player in players]

    plt.figure(figsize=(10, 5))
    plt.bar(names, values, color="blue", edgecolor="black")

    plt.xlabel("Players")
    plt.ylabel(attr_name.replace("_", " ").capitalize())
    plt.title(f"Comparison of players by {attr_name.replace('_', ' ')}")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.show()


def plot_points_per_day(data: dict, days_back: int, current_date, title="Points over Time"):
    if isinstance(current_date, str):
        current_date = datetime.strptime(current_date, "%Y-%m-%d").date()
    start_date = current_date-timedelta(days=days_back)

    parsed_data = {
        datetime.strptime(k, "%Y-%m-%d").date(): v for k, v in data.items()
        }

    date_range = []
    current = start_date
    while current <= current_date:
        date_range.append(current)
        current += timedelta(days=1)

    y = [parsed_data.get(d, 0) for d in date_range]
    x_labels = [d.strftime("%Y-%m-%d") for d in date_range]

    plt.figure(figsize=(12, 6))
    plt.plot(x_labels, y, marker='o', linestyle='-', color='b', label='Points')
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Points")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
