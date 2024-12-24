import random
from tkinter import *
import os

CITY_FILES = {"New_York.gif": "New_York", "Helsinki.gif": "Helsinki", "Paris.gif": "Paris",
              "Moscow.gif": "Moscow", "London.gif": "London", "Tokyo.gif": "Tokyo", "Rome.gif": "Rome",
              "Berlin.gif": "Berlin", "Madrid.gif": "Madrid", "Stockholm.gif": "Stockholm"}

CITY_NAMES = ["New_York", "Helsinki", "Paris", "Moscow", "London", "Tokyo", "Rome", "Berlin", "Madrid", "Stockholm"]

class Game:
    def __init__(self):
        self.__main_window = Tk()
        self.__main_window.title("Guess the city")
        self.__total_score = 0
        self.__current_picture = None  # the current picture displayed on the city label
        self.__player_mode = "one player"  # the mode of the game: single player or two players
        self.__score = [None, None]  # the score of the two players for two players mode
        script_dir = os.path.dirname(os.path.abspath(__file__)) # the directory of the script

        self.__city_images = []
        for image_file in CITY_FILES:  # Adding the images to self.__city_images
            new_image = PhotoImage(file=os.path.join(script_dir, image_file))
            self.__city_images.append(new_image)

        self.__city_label = Label(self.__main_window, anchor=N)
        self.__city_label.grid(row=0, column=1, rowspan=3, padx=20, sticky=W + E + S + N)

        self.__end_image = PhotoImage(file=f"{script_dir}/end.gif")  # image displayed once the game has ended

        # Below are buttons and labels that are displayed in the start menu
        # ================================================================================================== #
        start = PhotoImage(file=f"{script_dir}/start.gif")  # start,
        info = PhotoImage(file=f"{script_dir}/info.gif")  # info,
        close = PhotoImage(file=f"{script_dir}/close.gif") # close
        self.__start_button = Button(self.__main_window, image=start, command=self.start)
        self.__info_button = Button(self.__main_window, image=info, command=self.info)
        self.__info_label = Label(self.__main_window, text="")
        self.__close_button = Button(self.__main_window, image=close, command=self.quit)
        self.__start_button.grid(row=0, column=0, sticky=N)
        self.__info_button.grid(row=1, column=0, sticky=E + W)
        self.__close_button.grid(row=2, column=0, sticky=E + W)
        # ================================================================================================== #

        self.__one_player_button = Button(self.__main_window, text="One player", command=self.one_player_mode, padx=25,
                                          pady=25, relief=RAISED, background="Teal")
        self.__two_players_button = Button(self.__main_window, text="Two players", command=self.two_player_mode,
                                           padx=25,
                                           pady=25, relief=RAISED, background="Orange")

        self.__player_turn_label = Label(self.__main_window, text="Player 1's turn", font=("Arial", 12, "bold"),
                                         background="orange", padx=25, pady=25)

        # Below are buttons and labels that are displayed during the game
        # ================================================================================================== #
        self.__choice1 = Button(self.__main_window, command=lambda number=1: self.choose(number))
        self.__choice2 = Button(self.__main_window, command=lambda number=2: self.choose(number))
        self.__choice3 = Button(self.__main_window, command=lambda number=3: self.choose(number))
        self.__choice4 = Button(self.__main_window, command=lambda number=4: self.choose(number))

        self.__new_game_button = Button(self.__main_window, text="New game", command=self.new_game, padx=25, pady=25,
                                        relief=RAISED, background="Aqua")
        self.__quit_button = Button(self.__main_window, text="Quit", command=self.quit, padx=25, pady=25, relief=RAISED,
                                    background="Red")
        self.__score_label = Label(self.__main_window, anchor=E, text=f"Score: {self.__total_score}",
                                   font=("Arial", 20))
        # ================================================================================================== #

        self.__main_window.mainloop()

    def assign_button(self):
        """
        Assigns random city names to the four choice buttons
        :return: a list of the four city names
        """
        current_cities = []
        copy_CITY_NAMES = CITY_NAMES.copy()  # I remove selected key/value so two choices won't have the same city name
        for i in range(4):
            city_index = random.randint(0, len(copy_CITY_NAMES) - 1)
            city_name = copy_CITY_NAMES.pop(city_index)
            if i == 0:
                self.__choice1.configure(text=city_name)
            elif i == 1:
                self.__choice2.configure(text=city_name)
            elif i == 2:
                self.__choice3.configure(text=city_name)
            elif i == 3:
                self.__choice4.configure(text=city_name)

            current_cities.append(city_name)

        return current_cities

    def assign_picture(self):
        """
        Assigns a random picture to the label
        Removes the picture from the list of pictures to avoid redundancy
        :return : none
        """
        try:
            current_pyimage = self.__city_images.pop(random.randint(0, len(self.__city_images) - 1))
            self.__city_label["image"] = current_pyimage
            self.__city_label.image = current_pyimage  # reference to avoid garbage collection
            self.__current_picture = current_pyimage["file"]
        except ValueError:
            if self.__player_mode == "one player":
                self.if_end_one_player()
            else:
                self.if_end_two_players()
            # if self.__city_label["image"] is empty randint() will raise a ValueError

    def is_valid(self):
        """
        checks if the picture's city name is in the choices otherwise the game won't have a correct answer.
        :return: True if the picture's city name is in the choices, False otherwise
        """
        current_cities = self.assign_button()
        current_pic = self.__current_picture
        if CITY_FILES[current_pic] in current_cities:
            return True
        else:
            return False

    def update(self):
        """
        Loops until the picture's city name is in the choices
        Assigns the choices and the picture
        :return: none
        """
        self.assign_picture()
        while not self.is_valid():
            self.assign_button()
            self.is_valid()

    def choose(self, number):
        """
        Updates the score and the picture once the user has chosen a city
        :param number: the number of the button clicked
        :return: none
        """
        city = None
        if number == 1:
            city = self.__choice1["text"]
        elif number == 2:
            city = self.__choice2["text"]
        elif number == 3:
            city = self.__choice3["text"]
        elif number == 4:
            city = self.__choice4["text"]

        if city == CITY_FILES[self.__current_picture]:
            self.__total_score += 1
            self.__score_label["text"] = f"Score: {self.__total_score}"
        else:
            self.__score_label["text"] = f"Score: {self.__total_score}"

        if self.__player_mode == "one player":
            self.if_end_one_player()
        else:
            self.if_end_two_players()

        self.update()

    def new_game(self):
        """
        Resets the current game and starts a new game
        Assigned to the new game button
        :return: none
        """
        if self.__player_mode == "two players":  # resets the game for two players exclusively
            self.__score = [None, None]
            self.__player_turn_label["text"] = "Player 1's turn"
            self.__player_turn_label.grid(row=3, column=0, sticky=W + E + S + N)

        self.__total_score = 0
        self.__choice1.configure(state=NORMAL)
        self.__choice2.configure(state=NORMAL)
        self.__choice3.configure(state=NORMAL)
        self.__choice4.configure(state=NORMAL)
        self.__score_label["text"] = f"Score: {self.__total_score}"

        if len(self.__city_images) == 0:  # if the user presses new game after the game has ended
            for image_file in CITY_FILES:
                new_image = PhotoImage(file=image_file)
                self.__city_images.append(new_image)
        else:
            self.__city_images = []  # if the user presses new game in the middle of the game
            for image_file in CITY_FILES:
                new_image = PhotoImage(file=image_file)
                self.__city_images.append(new_image)

        self.update()

    def one_player_mode(self):
        """
        Displays the buttons and labels of the game for the single player mode
        :return: none
        """
        self.__player_mode = "one player"

        self.__city_label.grid(row=0, column=1, columnspan=4, padx=70, pady=30, sticky=W + E + S + N)
        self.__back_button.grid(row=0, column=0, sticky=E + W)
        self.__new_game_button.grid(row=1, column=0, sticky=E + W)
        self.__quit_button.grid(row=2, column=0, sticky=E + W)
        self.__choice1.grid(row=3, column=2, sticky=E + W)
        self.__choice2.grid(row=3, column=3, sticky=E + W)
        self.__choice3.grid(row=4, column=2, sticky=E + W)
        self.__choice4.grid(row=4, column=3, sticky=E + W)
        self.__score_label.grid(row=5, column=0, columnspan=4, sticky=E + W)

        self.__one_player_button.grid_remove()
        self.__two_players_button.grid_remove()

        self.update()
        self.new_game()

    def two_player_mode(self):
        """
        Displays the buttons and labels of the game for the two players mode
        :return: none
        """

        self.__player_mode = "two players"
        self.__player_turn_label.grid(row=3, column=0, sticky=W + E + S + N)

        self.__city_label.grid(row=0, column=1, columnspan=4, padx=70, pady=30, sticky=W + E + S + N)
        self.__back_button.grid(row=0, column=0, sticky=E + W)
        self.__new_game_button.grid(row=1, column=0, sticky=E + W)
        self.__quit_button.grid(row=2, column=0, sticky=E + W)

        self.__choice1.grid(row=3, column=2, sticky=E + W)
        self.__choice2.grid(row=3, column=3, sticky=E + W)
        self.__choice3.grid(row=4, column=2, sticky=E + W)
        self.__choice4.grid(row=4, column=3, sticky=E + W)
        self.__score_label.grid(row=5, column=0, columnspan=4, sticky=E + W)

        self.__one_player_button.grid_remove()
        self.__two_players_button.grid_remove()

        self.update()
        self.new_game()

    def has_ended(self):
        """
        Checks if all the ten questions have been answered
        :return: True if the game has ended, False otherwise
        """

        if len(self.__city_images) == 0:
            return True
        else:
            return False

    def if_end_one_player(self):
        """
        Updates the score if the game has ended for the single player mode
        Disables the choice buttons if the game has ended to avoid errors
        """
        if self.has_ended():
            self.__score_label["text"] = f"Game Ended -- Total score: {self.__total_score} / 10"
            self.clean("end_single")

    def if_end_two_players(self):
        """
        Updates the score if the game has ended for the two players mode
        Disables the choice buttons if the game has ended to avoid errors
        """
        if self.has_ended():

            if self.__score[0] is None:  # if player 1 hasn't played yet

                self.__score[0] = self.__total_score  # updates player 1's score

                self.__total_score = 0  # resets the total score
                self.__score_label["text"] = f"Score: {self.__total_score}"
                self.__player_turn_label["text"] = f"Player 2's turn"

                for image_file in CITY_FILES:
                    new_image = PhotoImage(file=image_file)
                    self.__city_images.append(new_image)

            else:  # after the second player finished playing
                self.__score[1] = self.__total_score  # updates player 2's score

            #  Once both players have played, the winner is displayed
            if self.__score[0] is not None and self.__score[1] is not None:
                if self.__score[0] > self.__score[1]:
                    self.__score_label["text"] = (f"Player 1 total point: {self.__score[0]}\n"
                                                  f"Player 2 total point: {self.__score[1]}\n"
                                                  f"Player 1 wins with {self.__score[0]} / 10")
                elif self.__score[0] < self.__score[1]:
                    self.__score_label["text"] = (f"Player 1 total point: {self.__score[0]}\n"
                                                  f"Player 2 total point: {self.__score[1]}\n"
                                                  f"Player 2 wins with {self.__score[1]} / 10")
                else:
                    self.__score_label["text"] = (f"Player 1 total point: {self.__score[0]}\n"
                                                  f"Player 2 total point: {self.__score[1]}\n"
                                                  f"Game ends draw with {self.__score[0]} / 10")

                self.clean("end_two")

    def info(self):
        """
        Displays the game description
        Assigned to the info button
        """

        self.__info_label = Label(self.__main_window,
                                  text="The following game is a game where the user has to guess the city in the "
                                       "picture. The game has 10 questions. Each picture has four choices. The user "
                                       "has to choose the correct city name from the four choices. The user can "
                                       "choose to play again or quit after the game has ended. After the game has "
                                       "ended, the total score is displayed. The total score is the number of correct "
                                       "answers out of 10.\n\n"
                                       "Press Start to continue\n\n"
                                       "Press Close to quit", font=("Arial", 12), wraplength=500, foreground="blue",
                                  background="lightgrey", padx=50, pady=50)

        self.__info_label.grid(row=0, column=2, sticky=E + W, columnspan=2, rowspan=3)

    def start(self):
        """
        Starts the game which displays the buttons "one player", "two players", or "back" to return to the start menu
        Assigned to the start button
        :return: none
        """

        self.__one_player_button.grid(row=1, column=0, sticky=E + W)
        self.__two_players_button.grid(row=2, column=0, sticky=E + W)
        self.__back_button = Button(self.__main_window, text="Back", command=self.back, relief=RAISED,
                                    background="Purple", padx=25, pady=25)
        self.__back_button.grid(row=3, column=0, sticky=E + W)

        self.clean("start")

    def back(self):
        """
        Returns to the start menu
        """
        # self.new_game()
        self.__start_button.grid(row=0, column=0, sticky=N)
        self.__info_button.grid(row=1, column=0, sticky=E + W)
        self.__close_button.grid(row=2, column=0, sticky=E + W)

        self.clean()

    def clean(self, where="back"):
        """
        Cleans the window by removing the buttons and labels
        """
        if where == "back":
            self.__start_button.grid(row=0, column=0, sticky=N)
            self.__info_button.grid(row=1, column=0, sticky=E + W)
            self.__close_button.grid(row=2, column=0, sticky=E + W)

            self.__one_player_button.grid_remove()
            self.__back_button.grid_remove()
            self.__two_players_button.grid_remove()
            self.__choice1.grid_remove()
            self.__choice2.grid_remove()
            self.__choice3.grid_remove()
            self.__choice4.grid_remove()
            self.__score_label.grid_remove()
            self.__new_game_button.grid_remove()
            self.__quit_button.grid_remove()
            self.__city_label.grid_remove()
            self.__player_turn_label.grid_remove()
            self.__info_label.grid_remove()
            self.__score_label.grid_remove()

        if where == "start":
            self.__start_button.grid_remove()
            self.__info_button.grid_remove()
            self.__close_button.grid_remove()
            self.__info_label.grid_remove()

        if where == "end_two":
            self.__city_label["image"] = self.__end_image
            self.__choice1.configure(state=DISABLED)
            self.__choice2.configure(state=DISABLED)
            self.__choice3.configure(state=DISABLED)
            self.__choice4.configure(state=DISABLED)
            self.__player_turn_label.grid_remove()

        if where == "end_single":
            self.__city_label["image"] = self.__end_image
            self.__choice1.configure(state=DISABLED)
            self.__choice2.configure(state=DISABLED)
            self.__choice3.configure(state=DISABLED)
            self.__choice4.configure(state=DISABLED)

    def quit(self):
        """
        Quits the game
        Assigned to the quit button
        :return : none
        """

        self.__main_window.destroy()


def main():
    gui = Game()


if __name__ == "__main__":
    main()
