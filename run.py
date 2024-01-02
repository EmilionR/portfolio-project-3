# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
import random

# Scope of APIs to run
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Credentials file
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

# Google Spreadsheet
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('euroquiz-highscores')
high_scores = SHEET.worksheet('highscores')

username = ""
question_list = [] # List of questions
answer_list = [] # List of correct answers
question_selection = [] # Selected questions for this round
question_length = 7 # Determine how many lines to extract for each question
round_length = 15 # Number of questions per round of the game
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
    global username
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
    scores = get_high_scores()
    print("--HIGH SCORES--")
    for i in range(10): # Count to 10
        entry = "----" # Placeholder for empty entries
        if i < len(scores): # Check if i is within list bounds
            entry = f"{scores[i][0]}: {scores[i][1]}" # Write name and score if index is found
        print(f"{i+1}) {entry}")  # Printing i+1 to compensate for 0 index
    print("\n")

def select_questions():
    """
    Pick a random selection of questions for the game.
    I generate numbers in sequence and then shuffle them,
    rather than generating x random numbers.
    This is to ensure that numbers are unique and within range.
    """
    global question_selection
    question_selection = [] # Reset the question selection before each round
    amount = len(question_list) # Number of questions to choose from
    rand_questions = [] # List of random question selections
    for i in range(0, amount-1): # Generate numbers from 0 to last index of questions
        rand_questions.append(i) # Add the number to 
    random.shuffle(rand_questions) # Shuffle the order of numbers
    rand_questions = rand_questions[:round_length] # Cut list to match round length
    question_selection.extend(rand_questions) # Add rand_question indexes to question_selection

def start_round():
    """
    Begin the game
    """
    select_questions()
    request_name()
    ask_question()

def ask_question():
    """
    Present the next question and the alternatives for answers
    """
    print("Next question!\n")
    while True:
        # Select question using a random number from question_selection,
        # getting the index corresponding to the current question number
        print(f"Question number {current_question+1}")
        print(f"{question_list[question_selection[current_question]]}")
        answer = input("Your answer:\n").upper()
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
    point_or_points = ""
    # Check if the answer matches the answer in the [current_question]
    # index of question_selection list
    if answer == answer_list[question_selection[current_question]]:
        print("CORRECT!")
        score += 1
    else:
        print("WRONG!")
    if score == 1:
        point_or_points = "point"
    else:
        point_or_points = "points"
    print(f"You have {score} {point_or_points}!\n")
    current_question += 1 # Increment question counter to get next question
    input("Press ENTER to continue\n\n")
    if current_question >= round_length: # Check if this is the last question
        game_over()

def game_over():
    """
    Calculate final score and check if hi-score is achieved
    """
    print(f"GAME OVER!\n\nFinal score: {score}\n")
    compare_scores(score, get_high_scores())
    print("Play Again?\n")
    while True:
        choice = input("Y/N\n").upper()
        if choice == "N":
            print("Thank you for playing.\n")
            exit()
        elif choice == "Y":
            restart_game()
            break

def update_high_score(scoreboard):
    """
    Update high score list
    """
    for i in range(10): # Iterate through 10 indexes of scoreboard list
        high_scores.append_row(scoreboard[i])
        if i == (len(scoreboard) -1):
            break
    
def get_high_scores():
    """
    Read high scores from text file
    """
    scores = [] # List of names and scores
    with open('high-score.txt') as f: # Read from high-score.txt
        for line in f:
        # Append a pair of name and score to list,
        # Name is the current line, score is the next line cast to an integer
            scores.append([line.strip(), int(next(f).strip())])
    return scores

def compare_scores(score, scoreboard):
    """
    Compare score to scores in scoreboard
    """
    highscores = scoreboard
    highscores.append([username, score]) # Add score to list of highscores
    highscores.sort(key = lambda scr: scr[1], reverse = True) # Sort list by value of second index in sublist
    if len(highscores) < 10: # Check if list has more than 10 scores
        highscores = highscores[:10] # Trim list to a length of 10
    update_high_score(highscores)

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