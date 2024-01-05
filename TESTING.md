# EuroQuiz - TESTING

![Project-image]()

Visit live deployed site: [EuroQuiz](https://europe-quiz-pp3-b56221b33626.herokuapp.com/)

* [Validation](#validator-testing)
* [Manual Testing](#manual-testing)
  * [Testing User Stories](#testing-user-stories)
  * [Full Testing](#full-testing)

## Validation

I used PEP8 to validate the code. No errors were found, only minor remarks about spacing and line lenghts.
For example, some inline comments needed more indentation and some lines were too long (in the code, not in the actual program's output). I addressed all these and the reading now comes back completely clean.

## Manual Testing

### Testing User Stories

__First Time Visitors__

| Goals | How are they achieved? |
| --- | --- |


__Returning Visitors__

|  Goals | How are they achieved? |
| --- | --- |

### Full Testing

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |

### Solved Bugs

1. The game would sometimes crash when trying to load high scores if there were few or no entries in the list.
2. Names in the first place of the scoreboard would lose their first letter when loaded into the game.
3. Highscores would be reset when refreshing the page

### Unfixed Bugs

There is one annoying bug in this program, which lets impatient users input their answers while the program is still printing the questions. The program keeps the input buffered and handles it when the input prompt appears. I used a variety of solutions for this (some of which can be seen by looking at older deployments here at GitHub), but all had drawbacks that were ultimately worse than the original bug. For example, using getpass had a nearly ideal result except for the fact that it rendered all input invisible.

Proper solutions require multiple imports and dependencies which are system specific, and I'd need to make sure the dependencies come through to the deployed project at heroku. And some linux builds will completely reject any attempt to mess with inputs. There are so many factors that simply cannot be tested within the context of this small project made for a Code Institute assignment.

So, during my final mentoring session for the project, I was recommended to return the code to its original state and explain the nature of this bug here.