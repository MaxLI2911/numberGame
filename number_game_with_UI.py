import tkinter as tk
from tkinter import messagebox
from random import randint
from serialization import read_from_json, write_to_json
from player import Player
from graphics import plot_player_achievements, plot_points_per_day
import datetime


class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess the Number Game")
        self.data = read_from_json("/home/hhhhhhh/PIPR/pipr_25l/lab1/players.json")
        if self.data is None:
            messagebox.showerror("Error", "Could not load players data.")
            exit()
        self.player = None
        self.number = None
        self.limit = None
        self.num_of_try = 1
        self.setup_ui()
        self.ask_if_new_player()

    def setup_ui(self):
        self.text = tk.Text(self.root, height=30, width=80, state='disabled')
        self.text.pack(padx=10, pady=10)
        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=5)
        self.button = tk.Button(self.root, text="Submit", command=self.process_input)
        self.button.pack(pady=5)
        self.root.bind('<Return>', self.process_input_event)
        self.state = None
        self.graph_buttons_frame = tk.Frame(self.root)

        self.button_max = tk.Button(self.graph_buttons_frame, text="Max Points", command=self.plot_max)
        self.button_avg = tk.Button(self.graph_buttons_frame, text="Average", command=self.plot_avg)
        self.button_games = tk.Button(self.graph_buttons_frame, text="Num of Games", command=self.plot_games)
        self.button_days = tk.Button(self.graph_buttons_frame, text="Points per Day", command=self.ask_days_for_graph)

        self.yn_buttons_frame = tk.Frame(self.root)
        self.yes_button = tk.Button(self.yn_buttons_frame, text="Yes", width=10, command=self.yes_clicked)
        self.no_button = tk.Button(self.yn_buttons_frame, text="No", width=10, command=self.no_clicked)

        self.yes_button.pack(side=tk.LEFT, padx=10)
        self.no_button.pack(side=tk.LEFT, padx=10)

        self.back_button = tk.Button(self.root, text="← Back to Game", command=self.back_to_game)

        self.arrow_canvas = tk.Canvas(self.text, width=100, height=100, bg="white", highlightthickness=0)
        self.arrow_id = None

    def log(self, message):
        self.text.config(state='normal')
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
        self.text.config(state='disabled')

    def ask_if_new_player(self):
        self.state = "new_player"
        self.log("Hi, this game is guess the number.")
        self.log("Are you a new player?")
        self.show_yn_buttons()

    def process_input_event(self, event):
        self.process_input()

    def process_input(self):
        user_input = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        if self.state == "new_player":
            self.new_player(user_input)

        elif self.state == "enter_name":
            self.enter_name(user_input)

        elif self.state == "enter_id":
            self.enter_id(user_input)

        elif self.state == "create_name":
            self.create_name(user_input)

        elif self.state == "set_limit":
            self.set_limit(user_input)

        elif self.state == "guessing":
            return self.guessing(user_input)

        elif self.state == "graph_days":
            self.graph_days(user_input)

    def graph_days(self, user_input):
        num_days = check_input_num(user_input)
        if num_days is not None:
            current_date = datetime.date.today().isoformat()
            plot_points_per_day(self.player.points_per_day, num_days, current_date)
        self.show_graph_options()

    def guessing(self, user_input):
        guess = check_input_num(user_input)
        if guess is None:
            return
        if guess == self.number:
            self.clear_arrow()
            point = points(self.limit, self.num_of_try)
            current_date = datetime.date.today().isoformat()
            self.player.new_average(point)
            self.player.num_of_games += 1
            self.player.new_max_points(point)
            self.player.add_or_update_points_date(current_date, point)
            self.log(f"\nYou guessed right on the {self.num_of_try}th try.")
            self.log(f"You get {point:.2f} points.")
            if point == 0:
                self.log("Too many guesses. You lose.")
            else:
                self.log("Amazing! You are a winner!")

            self.show_statistics()
            self.state = "continue"
            self.log("\nDo you want to continue the game?")
            write_to_json("players", self.data)
            self.show_yn_buttons()

        elif guess < self.number:
            self.num_of_try += 1
            self.log("Try a greater number.")
            self.show_arrow_up()
        else:
            self.num_of_try += 1
            self.log("Try a lower number.")
            self.show_arrow_down()

    def set_limit(self, user_input):
        limit = check_input_num(user_input)
        if not limit:
            self.log("Invalid limit, try again:")
        else:
            self.limit = limit
            self.number = randint(0, limit)
            self.num_of_try = 1
            self.log(f"Limit is set. Guess the number from 0 to {self.limit}")
            self.state = "guessing"

    def create_name(self, user_input):
        id = len(self.data) + 1
        self.player = Player(id, user_input, 0, 0, 0)
        self.data.append(self.player)
        self.log(f"Your id is {self.player.id}, remember it.")
        self.start_game()

    def enter_id(self, user_input):
        player = find_player(self.data, user_input, self.temp_name)
        if player is None:
            self.log("There is no such player in the database.")
            self.ask_if_new_player()
        else:
            self.player = player
            self.start_game()

    def enter_name(self, user_input):
        self.temp_name = user_input
        self.state = "enter_id"
        self.log("Enter your ID:")

    def new_player(self, user_input):
        if user_input.lower() == 'n':
            self.state = "enter_name"
            self.log("Enter your name:")
        else:
            self.state = "create_name"
            self.log("Welcome, new player! Enter your name:")

    def start_game(self):
        self.state = "set_limit"
        self.log("Enter the upper limit of numbers:")
        self.clear_arrow()

    def show_statistics(self):
        self.log("\nYour statistics:")
        self.log(self.player.statistics())
        players_statistick(self.player, self.data)

    def show_graph_options(self):
        self.state = "graph"
        self.log("\nIf you want - choose a graph to display:")

        self.entry.pack_forget()
        self.button.pack_forget()

        self.graph_buttons_frame.pack(pady=5)
        self.button_max.pack(side=tk.LEFT, padx=5)
        self.button_avg.pack(side=tk.LEFT, padx=5)
        self.button_games.pack(side=tk.LEFT, padx=5)
        self.button_days.pack(side=tk.LEFT, padx=5)

        self.back_button.pack(pady=10)

    def hide_graph_buttons(self):
        self.graph_buttons_frame.pack_forget()
        for widget in self.graph_buttons_frame.winfo_children():
            widget.pack_forget()
        self.back_button.pack_forget()

    def show_yn_buttons(self):
        self.entry.pack_forget()
        self.button.pack_forget()
        self.yn_buttons_frame.pack(pady=5)

    def hide_yn_buttons(self):
        self.yn_buttons_frame.pack_forget()
        self.entry.pack()
        self.button.pack()

    def yes_clicked(self):
        if self.state == "new_player":
            self.state = "create_name"
            self.hide_yn_buttons()
            self.log("Welcome, new player! Enter your name:")
        elif self.state == "continue":
            self.state = "set_limit"
            self.hide_yn_buttons()
            self.log("Enter the upper limit of numbers:")

    def no_clicked(self):
        if self.state == "new_player":
            self.state = "enter_name"
            self.hide_yn_buttons()
            self.log("Enter your name:")
        elif self.state == "continue":
            self.state = "graph"
            self.hide_yn_buttons()
            self.show_graph_options()

    def back_to_game(self):
        self.hide_graph_buttons()
        self.entry.pack()
        self.button.pack()
        self.state = "set_limit"
        self.log("Enter the upper limit of numbers:")

    def plot_max(self):
        plot_player_achievements(self.data, "max_points")
        self.show_graph_options()

    def plot_avg(self):
        plot_player_achievements(self.data, "average")
        self.show_graph_options()

    def plot_games(self):
        plot_player_achievements(self.data, "num_of_games")
        self.show_graph_options()

    def ask_days_for_graph(self):
        self.state = "graph_days"
        self.hide_graph_buttons()
        self.entry.pack()
        self.button.pack()
        self.log("Enter number of days for graph:")

    def show_arrow_up(self):
        self.clear_arrow()
        self.arrow_canvas.place(relx=1.0, rely=0.3, anchor='ne')
        self.arrow_id = self.arrow_canvas.create_polygon(45, 15, 75, 75, 15, 75, fill="blue")
        self.arrow_id = self.arrow_canvas.create_rectangle(30, 100, 60, 50, fill="blue", outline="blue")

    def show_arrow_down(self):
        self.clear_arrow()
        self.arrow_canvas.place(relx=1.0, rely=0.3, anchor='ne')
        self.arrow_id = self.arrow_canvas.create_polygon(15, 25, 75, 25, 45, 85, fill="blue")
        self.arrow_id = self.arrow_canvas.create_rectangle(30, 40, 60, 0, fill="blue", outline="blue")

    def clear_arrow(self):
        self.arrow_canvas.delete("all")
        self.arrow_canvas.place_forget()


def check_input_num(number):
    try:
        number = int(number)
        if number < 0:
            return None
        else:
            return number
    except ValueError:
        return None


def points(limit, num_of_try):
    point = (1/(2**(num_of_try-1)/(limit+1)))
    return point if point > 1 else 0


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
    print_statistick("number of games", best_player(player, data, "num_of_games"))


def best_player(player: Player, data: list, attr_name):
    max_points = [getattr(gamer, attr_name) for gamer in data]
    max_points.sort(reverse=True)
    return max_points[0], max_points.index(getattr(player, attr_name)) + 1


def print_statistick(kind: str, data: list):
    msg = f"\nMaximum of {kind} among players: {data[0]}\nYour place: {data[1]}"
    if data[1] == 1:
        msg += "\nCongratulations, you are the best!"
    app.log(msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()
