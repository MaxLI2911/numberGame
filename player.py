from dataclasses import dataclass, field


@dataclass
class Player:
    id: int
    name: str
    num_of_games: int
    average: float
    max_points: float
    points_per_day: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "num_of_games": self.num_of_games,
            "average": self.average,
            "max_points": self.max_points,
            "points_per_day": self.points_per_day
         }

    def statistics(self):
        return (
            f"Name {self.name}\n"
            f"Number of games {self.num_of_games}\n"
            f"Average score {self.average}\n"
            f"Maximum points received {self.max_points}"
        )

    def new_average(self, points: int):
        self.average = (
            (self.average*self.num_of_games+points)/(self.num_of_games+1)
        )

    def new_max_points(self, points: int):
        if points > self.max_points:
            self.max_points = points

    def add_or_update_points_date(self, key: str, value: int):
        self.points_per_day[key] = self.points_per_day.get(key, 0) + value
