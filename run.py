# Write your code to expect a terminal of 80 characters wide and 24 rows high

username = ""
question_list = []

def initialize_game():
    """
    Initialize game state and relevant variables
    """

def create_questions():
    """
    Load questions from file
    """
    global question_list # List of questions
    question_lines = "" # Temporary container for question+answers broken into lines
    questions_file = open("questions.txt", "r") # Load questions from text file
    lines_counted = 0 # Counter used for breaking file into even chunks
    for line in questions_file:
        question_lines += line # Add line to question
        lines_counted += 1
        if lines_counted == 6: # If all lines for the current question have been read
            question_list.append(question_lines) # Add processed question to list of questions
            question_lines = [] # Clear the temporary list
            lines_counted = 0 # Reset the counter

def intro_message():
    """
    Displays game logo and welcome message
    """
    choice = ""
    print("\n"
          "\n"
          "                                  Europe  Quiz                                  "
          "\n"
          "\n"
          "                         Answer Questions about Europe                          "
          "\n"
          "\n")
          
    while True:
        print("1. Start Game\n"
        "2. High Scores\n"
        "3. How to Play\n")
        choice = input("Please select(1, 2, or 3)\n")
        if choice == "1":
            start_round()
            break
        elif choice == "2":
            show_high_score()
        elif choice == "3":
            how_to_play()
        else:
            print("Invalid option.")

def how_to_play():
    print("\n"
          "\n"
          "                                  How to Play                                   "
          "\n"
          "\n"
          "\n"
          "Each question comes with four potential answers : A, B, C, and D.\n"
          "Choose one by typing in the corresponding letter.\n"
          "Each correct answer gives you one point.\n"
          "See if you can get them all right and get your name on the scoreboard.\n"
          )

def request_name():
    """
    Request player name input
    """
    print("Welcome to the Europe Quiz!")
    while(True): #Keep requesting name until a valid name is given
        username = input("What's your name?\n")
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
    request_name()
    ask_question()

def ask_question():
    """
    Present the next question and the alternatives for answers
    """
    print(question_list[0])

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
    create_questions()
    intro_message()

main()