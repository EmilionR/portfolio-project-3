# Import google spread and authorization for Cloud API
import gspread
from google.oauth2.service_account import Credentials
# Import randomness generator to randomize questions
import random
# Import time for waiting
import time
# Texttable for highscore table
from texttable import Texttable
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


# Custom exception for try blocks
class InvalidChoiceError(Exception):
    "Raised when an unintented input is given."
    pass


# Global variables
username = ""
question_list = []  # List of questions
answer_list = []  # List of correct answers
question_selection = []  # Selected questions for this round
question_length = 8  # Determine how many lines to extract for each question
round_length = 15  # Number of questions per round of the game
current_question = 0
score = 0

# Load ASCII art
ascii = open("assets/ascii.txt")


def load_ascii(begin, stop):
    """
    Read ascii art file line by line, setting colors to selected lines
    Takes arguments for which line to start and stop at
    """
    height = stop - begin  # Calculate the height of the art
    lines_counted = 0
    logo = ""
    for i in range(begin, stop):
        if lines_counted <= height / 2.5 or lines_counted >= 0.6 * height:
            logo += f"{Fore.BLUE}{str(ascii.readline())}"
        else:
            logo += f"{Fore.YELLOW}{str(ascii.readline())}"
        lines_counted += 1
    return logo


# Load ASCII text logos
game_logo = load_ascii(1, 11)
thanks_for_playing = load_ascii(13, 34)
how_play = load_ascii(30, 42)


def create_questions():
    """
    Load questions from file and loop through it,
    grouping a certain number of lines at a time, then append
    each group (which is one question with answer options) to a list.
    The first line of each chunk is the correct anser, which gets
    assigned to a separate list and then cleared
    """
    global question_list  # List of questions
    global answer_list  # List of correct answers
    global question_length
    question_lines = ""  # Temporary list of Q+A broken into lines
    questions_file = open("assets/questions.txt", "r")  # Load questions
    lines_counted = 0  # Counter used for breaking file into even chunks
    for line in questions_file:
        if lines_counted == 0:  # Check for first line of chunk (the answer)
            answer_list.append(line[0])  # Append the answer to list
            line = ""  # Clear the line so it doesn't appear in the question
        question_lines += line  # Add line to question
        lines_counted += 1
        #  If all lines for the current question have been read
        if lines_counted == question_length:
            # Add processed question to list of questions
            question_list.append(question_lines)
            question_lines = ""  # Clear the temporary list
            lines_counted = 0  # Reset the line counter to start new question


def intro_screen():
    """
    Displays game logo and main menu
    """
    choice = ""

    while True:  # Loop until valid input is given
        line_by_line(game_logo, 0.01, "none")
        print(Fore.YELLOW + "\n")
        print("Answer Questions about Europe".center(80, '-'),
              f"\n\n{Style.RESET_ALL}")
        menu_options = "1. Start Game\n2. High Scores\n3. How to Play\n\n"
        line_by_line(menu_options, 0.04, "center")
        try:
            select_message = "Please select (1, 2, 3)\n\n"
            choice = input(f"{Fore.CYAN}{select_message}{Fore.MAGENTA}")
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
                raise InvalidChoiceError

        except ValueError:
            print(f"{Fore.RED}\n", "Invalid input. Please choose 1, 2, or 3",
                  f"\n{Style.RESET_ALL}")

        except InvalidChoiceError:
            print(f"{Fore.RED}\n", "Invalid input. Please choose 1, 2, or 3",
                  f"\n{Style.RESET_ALL}")
            time.sleep(0.4)

        except KeyboardInterrupt:
            print(f"{Fore.RED}\n", "Control+C interrupted operation.",
                  f"\n{Style.RESET_ALL}")


def how_to_play():
    line_by_line(how_play, 0.03, "center")
    instructions = """
        You must answer 15 questions.
        Each question has four potential answers : A, B, C, and D.
        Choose one by typing in the corresponding letter.
        Each correct answer gives you one point.
        Try to get them all right and reach the top of the scoreboard."""
    print(f"{Style.RESET_ALL}")
    line_by_line(instructions, 0.05, "none")


def request_name():
    """
    Request player name input
    """
    global username
    time.sleep(0.2)
    print("        Welcome to the Europe Quiz!\n")
    while True:  # Keep requesting name until a valid name is given
        time.sleep(0.3)
        username = input(f"        What's your name?\n\n{Fore.MAGENTA}")
        print(f"{Style.RESET_ALL}")
        if username == "" or username.isspace():  # Check if name is left blank
            print("        Silence, huh... Surely, you must have a name.")
        elif len(username) > 16:  # Check if username is too long
            line_by_line("""That's quite long and hard to pronounce.
            Please give me the short version.
                         """, (0.3), "indent")
        elif username.isnumeric():  # Check if username only contains numbers
            print(f"        {username}? Please enter a name, not your number.")
        # Check if username contains invalid symbols
        elif not username.isalnum():
            print("        Names don't consist of non-alphanumeric symbols.")
        else:  # Accept username and continue
            time.sleep(0.5)
            print(f"\n        Welcome, {username}!")
            time.sleep(0.3)
            print("\n        Let's get started.\n")
            time.sleep(0.8)
            clear_terminal()
            break


def show_high_score():
    """
    Show list of high scores
    Scores are read from a worksheet in a separate function
    This function then creates a table and prints it out
    """
    scores = get_high_scores()
    print(f"{Fore.YELLOW}", "--HIGH SCORES--".center(80), f"{Style.RESET_ALL}")
    if len(scores) < 10:  # If score list is not full
        for i in range(10 - len(scores)):
            scores.append(["----", "----"])  # Add blank entries to list
    scores.insert(0, ["Name", "Score"])
    score_tab = Texttable()  # Make a text table
    # Set style of the table to remove dividing lines
    score_tab.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)
    score_tab.add_rows(scores)  # Write name and score to rows of text table
    score_tab.set_cols_align(["c", "c"])  # Center text within table cells
    output = score_tab.draw()  # Turn the table into a string
    line_by_line(output, 0.03, "center")


def select_questions():
    """
    Pick a random selection of questions for the game.
    I generate numbers in sequence and then shuffle them,
    rather than generating x random numbers.
    This is to ensure that numbers are unique and within range.
    """
    global question_selection
    question_selection = []  # Reset the question selection before each round
    amount = len(question_list)  # Number of questions to choose from
    rand_questions = []  # List of random question selections
    # Generate numbers from 0 to last index of questions
    for i in range(0, amount-1):
        rand_questions.append(i)  # Add the number to
    random.shuffle(rand_questions)  # Shuffle the order of numbers
    # Cut list to match round length
    rand_questions = rand_questions[:round_length]
    # Add rand_question indexes to question_selection
    question_selection.extend(rand_questions)


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
        print(f"{Fore.YELLOW}Question number {current_question+1}")
        print(f"{Style.RESET_ALL}")
        question = question_list[question_selection[current_question]]
        time.sleep(0.3)
        line_by_line(f"{question}", 0.05, "indent")
        time.sleep(0.2)
        answer_question()


def answer_question():
    """
    Input and validate input
    """
    answer = ""
    try:
        answer = input(f"{Fore.CYAN}Your answer:\n\n{Fore.MAGENTA}").upper()
        if answer == "A" or answer == "B" or answer == "C" or answer == "D":
            check_if_correct(answer)
        else:
            raise InvalidChoiceError

    except ValueError:
        print(f"{Fore.RED}\n", "Invalid input. Please answer A, B, C, or D",
              f"\n{Style.RESET_ALL}")

    except InvalidChoiceError:
        print(f"{Fore.RED}\n", "Invalid input. Please answer A, B, C, or D",
              f"\n{Style.RESET_ALL}")

    except KeyboardInterrupt:
        print(f"{Fore.RED}\n", "Control+C interrupted operation.",
              f"\n{Style.RESET_ALL}")


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
        chatter("right")
        score += 1
    else:
        chatter("wrong")
    if score == 1:
        point_or_points = "point"
    else:
        point_or_points = "points"
    time.sleep(0.2)
    print(f"{Fore.YELLOW}")
    print(f"You have _{score}_ {point_or_points}!".center(80, '.'), "\n")
    current_question += 1  # Increment question counter to get next question
    enter_to_continue()
    if current_question >= round_length:  # Check if this is the last question
        game_over()


def chatter(right_or_wrong):
    """
    Provide different feedback about the answer
    """
    outcome = ""
    right = ["RIGHT", "CORRECT"]
    wrong = ["WRONG", "INCORRECT"]
    # Randomizer for different responses
    rand1 = random.randint(0, 3)
    # Randomizer for rigt/wrong vs correct/incorrect
    rand2 = random.randint(0, 1)

    if right_or_wrong == "right":
        outcome = f"{Fore.GREEN}{right[rand2]}{Style.RESET_ALL}"
    else:
        outcome = f"{Fore.RED}{wrong[rand2]}{Style.RESET_ALL}"
    print(f"{Style.RESET_ALL}")
    # Reply with one of these remarks
    if rand1 == 0:
        print("        That is...")
        time.sleep(0.5)
        print(f"        {outcome}!")
    elif rand1 == 1:
        print(f"        {username}...")
        time.sleep(0.5)
        print(f"        That's {outcome}!")
    elif rand1 == 2:
        print(f"        Ooooo...")
        time.sleep(0.2)
        print(f"        {outcome} answer!")
    elif rand1 == 3:
        print(f"        {outcome}!")
    else:
        print(f"        Yeah, that's {outcome}")


def game_over():
    """
    Calculate final score and check if hi-score is achieved
    """
    game_over_message()
    compare_scores(score, get_high_scores())
    while True:  # Ask about restarting until given valid input
        time.sleep(0.5)
        print(Fore.CYAN + "\n")
        print(f"Play Again?".center(80, "="), "\n")
        time.sleep(0.5)
        try:
            choice = input(f"Y/N\n\n{Fore.MAGENTA}").upper()
            if choice == "N":  # Display thank you message and stop the program
                clear_terminal()
                line_by_line(thanks_for_playing, 0.02, "none")
                exit()
            elif choice == "Y":  # Start another round of the game
                clear_terminal()
                restart_game()
                break
            else:
                print(f"\n{Fore.RED}ERROR: Invalid input.\n{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"{Fore.RED}\n", "Control+C interrupted operation.",
                  f"\n{Style.RESET_ALL}")


def game_over_message():
    """
    Present final score and gameover message
    Messages differ depending on score
    """
    print(f"{Fore.YELLOW}")
    time.sleep(0.5)
    print(f"GAME OVER!".center(80, "~"))
    time.sleep(0.5)
    print(f"Final score: {score}\n\n{Style.RESET_ALL}".center(80))
    time.sleep(0.5)
    if score > 15:
        print("        This score is not possible without cheating...\n\n")
    elif score == 15:
        print("        WOOHOO! Full score!")
        time.sleep(0.3)
        print("        That's incredible!\n\n")
    elif score > 10:
        print("        You did really well.\n\n")
    elif score > 7:
        print("        Not too shabby.\n\n")
    elif score > 0:
        print("        Better luck next time.\n\n")
    else:
        print(f"       I see...")
        time.sleep(0.3)
        print("        You're American, aren't you?\n\n")
    time.sleep(0.75)


def update_high_score(scoreboard):
    """
    Update high score list in external google sheet
    Create list of cells to update, loop through scores
    and add their values to the cells list, then update
    the document using the list of cells to update
    """
    cells_to_update = []

    class Cell:  # Holds the coordinates and value for a cell to update
        def __init__(self, r, c, val):
            self.row = r
            self.col = c
            self.value = val

    for i in range(10):  # Iterate through 10 indexes of scoreboard list
        """Add each name and score value to its own row
        Rows are designated as i+2 because sheet cells start at 1
        and because the first row holds headings"""
        cells_to_update.append(Cell(i+2, 1, scoreboard[i][0]))
        cells_to_update.append(Cell(i+2, 2, scoreboard[i][1]))
        if i == (len(scoreboard) - 1):
            break
    high_scores.update_cells(cells_to_update)
    show_high_score()


def get_high_scores():
    """
    Read high scores from gspread file
    """
    results = []
    # Extract name and score value from columns, skipping the first row
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
    highscores.append([username, score])  # Add score to list of highscores
    # Sort list by value of second index in sublist
    highscores.sort(key=lambda scr: scr[1], reverse=True)
    if len(highscores) < 10:  # Check if list has more than 10 scores
        highscores = highscores[:10]  # Trim list to a length of 10
    update_high_score(highscores)


def restart_game():
    """
    Start a new round of the quiz
    """
    global current_question
    global score
    current_question = 0  # Reset question counter
    score = 0  # Reset score counter
    start_round()  # Start a new round of the game


def clear_terminal():
    """
    Clear all text from the terminal to reduce clutter
    and improve aesthetics/formatting
    """
    print("\033c")  # Print an escape character to clear terminal


def enter_to_continue():
    """
    Ask user to press enter
    Any input works
    """
    enter_message = "[Press ENTER to continue]"
    time.sleep(0.3)
    input(f"{Fore.CYAN}\n{enter_message.center(80)}\n\n{Fore.MAGENTA}")
    clear_terminal()


def line_by_line(text, delay, style):
    """
    Split string into lines and print one by one
    with chosen time delay between lines
    """
    for line in text.splitlines():
        time.sleep(delay)
        if style == "indent":
            print(f"        {line}")
        elif style == "center":
            print(f"{line.center(80)}")
        else:
            print(line)


def main():
    create_questions()
    intro_screen()


main()
