# Write your code to expect a terminal of 80 characters wide and 24 rows high

username = ""

def initialize_game():
    """
    Initialize game state and relevant variables
    """

def create_questions():
    """
    Load questions from file
    """

def intro_message():
    """
    Displays game logo and welcome message
    """
    print("\n"
          "\n"
          "                                  Europe  Quiz                                  "
          "\n"
          "\n"
          "                         Answer Questions about Europe                          "
          "\n"
          "\n"
          "1. Start Game"
          "2. High Scores"
          "3. How to Play")

def request_name():
    """
    Request player name input
    """
    print("Welcome to the Europe Quiz!")
    while(True): #Keep requesting name until a valid name is given
        username = input("What's your name?")
        if username == "" or username.isspace(): #Check if name is left blank
            print("Surely, you must have a name.")
        elif username.isnumeric(): #Check if username only contains numbers
            print(f"{username}... Please enter a name, not your number.")
        elif len(username) > 16: #Check if username is too long
            print("I'm sorry, that's quite long and hard to pronounce.\nDo you have a nickname?")
        elif not username.isalnum(): #Check if username contains invalid symbols
            print("Hmm, names should not include non-alphanumeric symbols.")
        else: #Accept username and continue
            print(f"Welcome, {username}!\nLet's get started.")
            break

def show_high_score():
    """
    Show list of high scores
    """

def start_round():
    """
    Begin the game
    """

def ask_question():
    """
    Present the next question and the alternatives for answers
    """

def player_answer():
    """
    Player inputs their answer
    """

def check_if_correct():
    """
    Check if the answer given is correct,
    display result and award points if correct
    """

def game_over():
    """
    Calculate final score and check if hi-score is achieved
    """

def update_high_score():
    """
    Update high score list
    """

def restart_game():
    """
    Start a new round of the quiz
    """

def main():
    intro_message()
    request_name()
main()