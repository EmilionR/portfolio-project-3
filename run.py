# Write your code to expect a terminal of 80 characters wide and 24 rows high

username = ""
question_list = []
answer_list = []
question_length = 7 # Determine how many lines to extract for each question
current_question = 0
score = 0

def initialize_game():
    """
    Initialize game state and relevant variables
    """

def create_questions():
    """
    Load questions from file and loop through it,
    grouping a certain number of lines at a time,
    then append each group (which is one question with answer options) to a list.
    The first line of each chunk is the correct anser, which gets
    assigned to a separate list and then cleared
    """
    global question_list # List of questions
    global answer_list #List of correct answers
    global question_length
    question_lines = "" # Temporary container for question+answers broken into lines
    questions_file = open("questions.txt", "r") # Load questions from text file
    lines_counted = 0 # Counter used for breaking file into even chunks
    for line in questions_file:
        if lines_counted == 0: # Check for first line of chunk, containing the answer
            answer_list.append(line[0]) # Append the answer to the list of correct answers
            line = "" # Clear the line so that it does not appear in the question
        question_lines += line # Add line to question
        lines_counted += 1
        if lines_counted == question_length: # If all lines for the current question have been read
            question_list.append(question_lines) # Add processed question to list of questions
            question_lines = "" # Clear the temporary list
            lines_counted = 0 # Reset the line counter to start new chunk of lines

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
          
    while True: # Loop until valid input is given
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
        username = input("What's your name?\n\n")
        if username == "" or username.isspace(): #Check if name is left blank
            print("\nSilence, huh... Surely, you must have a name.")
        elif username.isnumeric(): #Check if username only contains numbers
            print(f"{username}... Please enter a name, not your number.")
        elif len(username) > 16: #Check if username is too long
            print("\nI'm sorry, that's quite long and hard to pronounce.\nPlease give me the short version.")
        elif not username.isalnum(): #Check if username contains invalid symbols
            print("\nHmm, names should not include non-alphanumeric symbols.")
        else: #Accept username and continue
            print(f"\nWelcome, {username}!\nLet's get started.\n")
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
    print("Next question!\n")
    while True:
        print(f"{question_list[current_question]}")
        answer = input("Your answer: \n").upper()
        if answer != "A" and answer != "B" and answer != "C" and answer != "D":
            print("Invalid input.\n")
        else:
            check_if_correct(answer)

def check_if_correct(answer):
    """
    Check if the answer given is correct,
    display result and award points if correct
    """
    global current_question
    global score
    if answer == answer_list[current_question]:
        print("CORRECT!")
        score += 1
    else:
        print("WRONG!")
    print(f"You have {score} points!\n")
    current_question += 1 # Increment question counter to get next question
    input("Press ENTER to continue\n\n")
    if current_question >= len(question_list):
        game_over()

def game_over():
    """
    Calculate final score and check if hi-score is achieved
    """
    print("GAME OVER!\n\nPlay Again?\n")
    while True:
        choice = input("Y/N\n").upper()
        if choice == "N":
            print("Thank you for playing.\n")
            break
        elif choice == "Y":
            restart_game()
            break

def update_high_score():
    """
    Update high score list
    """

def restart_game():
    """
    Start a new round of the quiz
    """
    global current_question
    global score
    current_question = 0 # Reset question counter
    score = 0 # Reset score counter
    start_round() # Start a new round of the game

def main():
    create_questions()
    intro_message()

main()