# PP3

![Project-image]()

[View the website here]()

## Contents

* [How to Play](#how-to-play)

* [Development Process](#development-process)

* [Features](#Features)
  * [Existing Features](#existing-features)
  * [Future Implementations](#future-implementations)

* [User Experience](#User-Experience)
  * [User Stories](#User-Stories)

* [Deployment](#Deployment)

* [Design](#Design)

* [Technologies Used](#Technologies-Used)
  * [Languages Used](#Languages-Used)
  * [Frameworks & Libraries](#frameworks--libraries)
  * [Other Programs](#other-programs)

* [Testing](#Testing)
  * [Solved Bugs](#solved-bugs)
  * [Known Bugs](#unfixed-bugs)
  
* [Credits](#Credits)
  * [Content](#Content)
  * [Media](#Media)
  * [Tutorials & Code Used](#tutorials--code-used)

## How to Play

The quiz game is quite straightforward. The game presents a question and four alternatives to choose from. The player inputs their selection, and the game checks if it is correct. If it is correct, the game increments the player's score. Otherwise, the player is told that the answer is incorrect.

WHen the game is over, the player can choose to start over from the beginning or quit. If their score is good enough, it will appear on the list of high scores.

## Development Process

Before I began building the project, I made a flowchart to visualize how the program will operate. This flowchart not only helped to determine the order of operations for the program itself, but also gave myself clear directions on where to start and the general sequence of building it.

![Concept Flowchart](documentation/flowchart.png)

From there, I built the core flow of the game function by function until the game could be played properly and repeatedly. Most of this revolves around taking user input and validating it to make sure that the input is correct and cannot cause any problems with the code. Also, I made the program convert all answer inputs to uppercase so that the game can accept it with a single line of code regardless of case.

The other aspect of the building process was getting the computer to read questions from a separate file and organizing questions and correct answers in a neat and reliable manner. As soon as the game itself was working, I started implementing the high score functionality using the same principles of reading and writing to a text file.

At one point, when all the functional code was about finished, I discovered that the scoreboard could not function as intended due to the way the deployment to Heroku works. Since the app could not make persistent overwrites to its text files and thereby save high scores between sessions, I decided to change the code to use an externally hosted spreadsheet.

This was achieved by using gspread through a Google Cloud API setup. The program now reads and writes to dedicated cells in a worksheet hosted on Google docs, within a limited scope that will never overflow.

## Features

### Existing Features

__GAME__

The game features a fairly wide selection of questions. Each round randomizes which questions are used.
This way, each round is unique and players can't cheat the game by simply restarting and memorizing a letter sequence.
Each round has 15 questions before the final score is achieved and displayed.

__QUESTIONS__

The questions are stored in a text file and extracted via a function that reads a certain number of lines at a time and stores that collection of lines as a variable in a list. The same function also extracts the correct answer and stores it together with the question in the list, so that each index in the list holds both a question and its answer.

At the start of each round, the program generates a sequence of numbers, shuffles the numbers, and then uses this sequence to access questions from the list. The result is a differenct selection of questions for each round of the game. This number sequence hold as many numbers as there are questions in a round of the game. No duplicate numbers occurr, and numbers never exceed the number of available questions.

__SCOREBOARD__

The game saves high scores, and players can view the scoreboard from the main menu. High scores are also on display at the end of each round. At the start of each game, the player gets to write their name. This name is what will go to the scoreboard if they get a good score. Only 10 scores are on display, and new high scores knock old ones down the list or delete them if they're no longer good enough.

__SCORE SHEET__

The score sheet is a simple worksheet with two columns, one for the name and one for the score. The program only uses 10 rows, with one additional row for the headings. When scores are compared, the program extracts all high scores from the sheet into a list. After appending the current player's score to that list, the list is then sorted by score in descending order and trimmed to a maximum length of 10. Then, the program overwrites the cells in the worksheet.

__INSTRUCTIONS__

The player can also view information on how to play from the starting screen of the game.

### Future Implementations

If I continue developing this game, I will add more questions. I would also have the game keep track of each time someone gets the right or wrong answer, and then use this data to calculate the perceived difficulty of each question. This would then be used to equalize the overall difficulty of each round, making the game both more interesting and more fair. This could also allow for harder questions to give an extra point.

## User Experience

### Main Goal

My goals with this project is to:

* Create a plain python game that is simple yet compelling
* Make the game interesting despite its plain text-only terminal nature
* Give the game replay value and variety

### User stories

__First-time visitor goals__

* The game should be easy to understand
* All instructions should be clear and simple
* I should be able to mess around without breaking the program
* I should always know what input is expected and why my input gets rejected

__Returning visitor goals__

* The game should not be a mere repetition of a set sequence of questions
* The game should keep track of results and let me look at the scoreboard
* Program feedback should not be dull and boring

## Technologies Used

### Languages Used

Python

### Frameworks & Libraries

gspread - For interacting with a google spreadsheet

oauthlib - For authorization/credentials when using gspread

random - For random number generation

time - For time handling, I use it to delay prints for a line-by-line output

texttable - For making a neat table of input, used for the highscore display

colorama - For outputting text in different colors

### Other Programs

VSCode - Used for all the coding.

Git - For version control.

GitHub - To store files and commit history.

Heroku - To deploy a live site.

Lucidchart - For the flowchart

## Deployment

### Heroku
The Application has been deployed from GitHub to Heroku following the steps:

1. Sign in or sign up at heroku.com
2. Create a new app with a unique app name and select your region
3. Click "Create app"
4. Click "Settings" and then "Config Vars", add a key called "PORT" with the value "8000" and (when making an app like this using an external worksheet) add another key with private API credentials in the value area.
5. Add any required buildpacks. This project uses Python and Node.js, with the latter being used for the terminal display and not the program itself.
6. Go to the "Deploy" tab and, under "Deployment method", select "GitHub." 
7. Insert the GitHub repository link or the name of the repository and click "Search" followed by "Connect" to deploy the GitHub repo to Heroku.
8. Next, you must select a branch of the repository for building the project, in this case "main."
9. Click "Deploy Branch" to deploy, or use "Enable Automatic Deploys" to make automatic deployments when the repo is updated.
10. You'll see a message saying “App was successfully deployed” when it's ready, and you click the "View" button to view the deployed project.

### GitHub

#### How to Fork the repository

1. Sign in to GitHub.
2. Go to the repository for this project, [EmilionR/card-battle-pp2](https://github.com/EmilionR/card-battle-pp2/commits/main/)
3. Click the Fork button in the top right corner.

#### How to Clone the repository

1. Log in (or sign up) to GitHub.
2. Go to the repository for this project, [EmilionR/card-battle-pp2](https://github.com/EmilionR/card-battle-pp2/commits/main/)
3. Click on the code button, select whether you would like to clone with HTTPS, SSH or GitHub CLI and copy the link shown.
4. Open the terminal in your code editor and change the current working directory to the location you want to use for the cloned directory.
5. Type 'git clone' into the terminal and then paste the link you copied in step 3. Press enter.

## Design

While this is a simple command line-based application, I wanted to make the design feel more interesting and also distinguish between different elements of the text output.
For example, anything typed by the user will appear in a magenta color, while prompts for input appear in cyan. The questions and commentary come in plain white text with an indentation, while general infomration is yellow and centered.

I also made much of the text appear line-by-line to make things more interesting and also let the user take things in at some points.

## Testing

Please refer to [TESTING.md](TESTING.md) for testing documentation.

## Credits

### Tutorials & Code Used

I learned the use of gspread and oauth from lessons by Code Institute.
Other libraries and implementations were learned from official documentation and the examples found within them, as seen in the links below.

[string.center()](https://www.w3schools.com/python/ref_string_center.asp)

[time](https://docs.python.org/3/library/time.html)

[texttable](https://pypi.org/project/texttable/)

I learned about the terminal clearing special character from [this post on fullstack](https://stackoverflow.com/questions/2084508/clear-terminal-in-python)