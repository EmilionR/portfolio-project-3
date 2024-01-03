# Import google spread and authorization for Cloud API
import gspread
from google.oauth2.service_account import Credentials
# Import randomness generator to randomize questions
import random
# Import time for waiting
import time
# Colorama import for styling text
from colorama import init as colorama_init
from colorama import Fore, Style
colorama_init()

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

# Load ASCII art
ascii = open("assets/ascii.txt")

def load_ascii(begin, stop):
    """
    Read ascii art file line by line, setting colors to selected lines
    Takes arguments for which line to start and stop at
    """
    height = stop - begin # Calculate the height of the art
    lines_counted = 0
    logo = ""
    for i in range(begin,stop):
        if lines_counted <= height / 2.5 or lines_counted >= 0.6 * height:
            logo += f"{Fore.BLUE}{str(ascii.readline())}"
        else:
            logo += f"{Fore.YELLOW}{str(ascii.readline())}"
        lines_counted += 1
    return logo

# Load ASCII text logos    
game_logo = load_ascii(1,11)
thanks_for_playing = load_ascii(13,34)

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
    questions_file = open("assets/questions.txt", "r") # Load questions from text file
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
    print(game_logo)
    print(f"{Fore.YELLOW}                         Answer Questions about Europe                          "
          "\n"
          f"\n{Style.RESET_ALL}")
          
    while True: # Loop until valid input is given
        print("1. Start Game\n"
        "2. High Scores\n"
        "3. How to Play\n")
        choice = input(f"{Fore.CYAN}Please select(1, 2, or 3)\n\n{Fore.MAGENTA}")
        if choice == "1":
            clear_terminal()
            start_round()
            break
        elif choice == "2":
            clear_terminal()
            show_high_score()
            enter_to_continue()
        elif choice == "3":
            clear_terminal()
            how_to_play()
            enter_to_continue()
        else:
            print(f"\n{Fore.RED}ERROR: Invalid input.\n{Style.RESET_ALL}")

def how_to_play():
    print("\n"
          "\n"
          f"{Fore.BLUE}          #  # .###. #     #   ##### .###.   ###.  #    .###. #. .#            \n"
          f"{Fore.YELLOW}          #  # #' `# #  .  #     #   #   #   #  #  #    #   # '#.#'            \n"
          "          #### #   # #. # .#     #   #   #   ###   #    #####  '#'            \n"
          f"{Fore.BLUE}          #  # #. .# '## ##'     #   #   #   #'    #    #   #   #              \n"
          "          #  # `###`  #   #      #   `###`   #     #### #   #   #              \n"
          "\n"
          f"\n{Style.RESET_ALL}"
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
    time.sleep(0.75)
    print("Welcome to the Europe Quiz!")
    while(True): #Keep requesting name until a valid name is given
        time.sleep(0.75)
        username = input(f"What's your name?\n\n{Fore.MAGENTA}")
        print(f"{Style.RESET_ALL}")
        if username == "" or username.isspace(): #Check if name is left blank
            print("\nSilence, huh... Surely, you must have a name.")
        elif username.isnumeric(): #Check if username only contains numbers
            print(f"{username}... Please enter a name, not your number.")
        elif len(username) > 16: #Check if username is too long
            print("\nI'm sorry, that's quite long and hard to pronounce.\nPlease give me the short version.")
        elif not username.isalnum(): #Check if username contains invalid symbols
            print("\nHmm, names should not include non-alphanumeric symbols.")
        else: #Accept username and continue
            time.sleep(0.75)
            print(f"\nWelcome, {username}!")
            time.sleep(0.75)
            print("\nLet's get started.\n")
            time.sleep(1.5)
            clear_terminal()
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
    while True:
        # Select question using a random number from question_selection,
        # getting the index corresponding to the current question number
        print(f"{Fore.YELLOW}Question number {current_question+1}\n{Style.RESET_ALL}")
        time.sleep(0.5)
        print(f"{question_list[question_selection[current_question]]}")
        time.sleep(1)
        answer = input(f"{Fore.CYAN}Your answer:\n\n{Fore.MAGENTA}").upper()
        if answer != "A" and answer != "B" and answer != "C" and answer != "D":
            print(f"\n{Fore.RED}ERROR: Invalid input.\n{Style.RESET_ALL}")
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
        print(f"{Fore.GREEN}CORRECT!{Style.RESET_ALL}")
        score += 1
    else:
        print(f"{Fore.RED}WRONG!{Style.RESET_ALL}")
    if score == 1:
        point_or_points = "point"
    else:
        point_or_points = "points"
    print(f"You have {score} {point_or_points}!\n")
    current_question += 1 # Increment question counter to get next question
    enter_to_continue()
    if current_question >= round_length: # Check if this is the last question
        game_over()

def game_over():
    """
    Calculate final score and check if hi-score is achieved
    """
    game_over_message()
    compare_scores(score, get_high_scores())
    while True: # Ask about restarting until given valid input
        time.sleep(0.5)
        print(f"{Fore.CYAN}Play Again?\n")
        time.sleep(0.5)
        choice = input(f"Y/N\n\n{Fore.MAGENTA}").upper()
        if choice == "N": # Display thank you message and stop the program
            clear_terminal()
            print(thanks_for_playing)
            exit()
        elif choice == "Y": # Start another round of the game
            clear_terminal()
            restart_game()
            break
        else:
            print(f"\n{Fore.RED}ERROR: Invalid input.\n{Style.RESET_ALL}")

def game_over_message():
    time.sleep(0.5)
    print(f"{Fore.YELLOW}GAME OVER!\n\n")
    time.sleep(0.5)
    print(f"Final score: {score}\n\n{Style.RESET_ALL}")
    time.sleep(0.75)
    if score > 15:
        print("This score is not possible without cheating...\n\n")
    elif score == 15:
        print("WOOHOO! Full score!")
        time.sleep(0.3)
        print("That's incredible!\n\n")
    elif score > 10:
        print("You did really well.\n\n")
    elif score > 7:
        print("Not too shabby.\n\n")
    elif score > 0:
        print("...")
        time.sleep(0.2)
        print("Better luck next time.\n\n")
    else:
        print(f"I see...")
        time.sleep(0.3)
        print("You're American, aren't you?\n\n")
    time.sleep(0.75)

def update_high_score(scoreboard):
    """
    Update high score list in external google sheet
    Create list of cells to update, loop through scores
    and add their values to the cells list, then update
    the document using the list of cells to update
    """
    cells_to_update = []
    class Cell: # Holds the coordinates and value for a cell to update
        def __init__(self, r, c, val):
            self.row = r
            self.col = c
            self.value = val

    for i in range(10): # Iterate through 10 indexes of scoreboard list
        # Add each name and score value to its own row
        # Rows are designated as i+2 because sheet cells start at 1
        # and because the first row holds headings
        cells_to_update.append(Cell(i+2, 1, scoreboard[i][0]))
        cells_to_update.append(Cell(i+2, 2, scoreboard[i][1]))
        if i == (len(scoreboard) -1):
            break
    high_scores.update_cells(cells_to_update)
    show_high_score()

def get_high_scores():
    """
    Read high scores from gspread file
    """
    results = []
    # Extract each name and score value from corresponding columns, skipping the first row
    names = [value for value in high_scores.col_values(1)[1:] if value]
    scores = [value for value in high_scores.col_values(2)[1:] if value]
    # Add each name-score pair to the results list
    for i in range(len(names)):
        results.append([names[i], int(scores[i])])
    return results

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

def clear_terminal():
    """
    Clear all text from the terminal to reduce clutter
    and improve aesthetics/formatting
    """
    print("\033c") # Print an escape character to clear terminal

def enter_to_continue():
    """
    Ask user to press enter
    Any input works
    """
    time.sleep(0.5)
    input(f"{Fore.CYAN}Press ENTER to continue\n\n{Fore.MAGENTA}")
    clear_terminal()

def main():
    create_questions()
    intro_message()

main()